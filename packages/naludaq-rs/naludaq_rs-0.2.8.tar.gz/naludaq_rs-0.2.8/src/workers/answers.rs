use std::time::Duration;

use flume::Receiver;
use futures::future::join_all;

use self::util::{set_command_id, Answers};
use crate::{
    connection::Connection,
    constants::{ANSWER_CACHE_SIZE, DUMMY_REGISTER_ID, REGISTER_READ_TIMEOUT},
    error::AnswerWorkerError,
    types::{RawAnswer, RawCommand},
};

/// Interface layer for the answer worker.
#[derive(Clone, Debug)]
pub struct AnswerWorker {
    /// Input channel for answers
    answers_rx: Receiver<Vec<u8>>,
    /// The answer cache
    answers: Answers,
}

impl AnswerWorker {
    /// Create a new connection worker.
    ///
    /// All data read from a connection is sent through the `from_board_tx` channel.
    ///
    /// The worker should be run with the [`ConnectionWorker::start`] method before
    /// performing any operations.
    pub fn new(answers_rx: Receiver<Vec<u8>>) -> Self {
        Self {
            answers_rx,
            answers: Answers::new(ANSWER_CACHE_SIZE),
        }
    }

    /// Runs the worker
    pub async fn start(&self) {
        let answers_rx = self.answers_rx.clone();
        let answers = self.answers.clone();
        tokio::spawn(async move {
            loop {
                match answers_rx.recv_async().await {
                    Ok(answer) => {
                        answers.insert(answer).await;
                    }
                    Err(_) => {
                        tracing::debug!("Stopping answer worker due to dropped channel");
                        break;
                    }
                }
            }
        });
    }

    /// Reset the received answers.
    pub async fn reset(&self) {
        self.answers.clear().await;
    }

    /// Send a read command to the given connection and wait for a response with a matching ID.
    ///
    /// # Errors
    /// - [`AnswerWorkerError::ReceiveTimeout`] if the response is not received within the timeout
    /// - [`AnswerWorkerError::SendFailed`] if the connection could not be sent
    pub async fn read(
        &self,
        connection: &Connection,
        command: RawCommand,
    ) -> Result<RawAnswer, AnswerWorkerError> {
        self.read_with_timeout(connection, command, REGISTER_READ_TIMEOUT)
            .await
    }

    /// Send multiple read commands to the board and wait for all responses.
    /// This is more efficient than calling [`Self::read`] sequentially.
    ///
    /// The length of the result is guaranteed to match the number of commands given.
    /// The order of the answers is also guaranteed to match the order of the given commands.
    ///
    /// # Errors
    /// If any of the individual read operations fail, the error variant is stored in the
    /// corresponding index of the returned vector. Errors match those of [`Self::read`].
    pub async fn read_all(
        &self,
        connection: &Connection,
        commands: impl AsRef<[RawCommand]>,
    ) -> Vec<Result<RawAnswer, AnswerWorkerError>> {
        let commands = commands.as_ref();
        // The timeout needs to be longer since we are sending multiple commands.
        // We can't wait forever though since it'll gum things up, so we need to have a ceiling.
        let timeout = Duration::from_millis(
            (REGISTER_READ_TIMEOUT.as_millis() as usize * std::cmp::min(commands.len(), 100)) as _,
        );
        let futs: Vec<_> = commands
            .iter()
            .map(|c| self.read_with_timeout(connection, c.clone(), timeout))
            .collect();
        join_all(futs).await
    }

    /// Send a read command to the given connection and wait for a response with a matching ID.
    /// Takes a timeout parameter.
    ///
    /// # Errors
    /// - [`AnswerWorkerError::ReceiveTimeout`] if the response is not received within the timeout
    /// - [`AnswerWorkerError::SendFailed`] if the connection could not be sent
    async fn read_with_timeout(
        &self,
        connection: &Connection,
        mut command: RawCommand,
        timeout: Duration,
    ) -> Result<RawAnswer, AnswerWorkerError> {
        let id = set_command_id(&mut command).unwrap_or(DUMMY_REGISTER_ID);

        // need to remove BEFORE sending the command since an answer with the given command ID
        // might have been received at any point in the past, but was ignored. This is especially
        // likely if immediate readout was used previously, since junk data can be interpreted as
        // a valid answer.
        self.answers.remove(id).await;

        Self::send_command(&connection, command).await?;
        self.answers
            .wait_answer(id, timeout)
            .await
            .ok_or(AnswerWorkerError::ReceiveTimeout)
    }

    /// Assign an ID to the given command and send it to the board.
    ///
    /// Digital registers are always assigned and ID of `0`.
    ///
    /// # Errors
    /// - [`AnswerWorkerError::SendFailed`] if the command could not be sent
    async fn send_command(
        connection: &Connection,
        command: RawCommand,
    ) -> Result<(), AnswerWorkerError> {
        connection
            .send(&command)
            .await
            .and(Ok(()))
            .or(Err(AnswerWorkerError::SendFailed))
    }
}

mod util {
    use std::{
        collections::HashMap,
        fmt::Debug,
        hash::Hash,
        sync::{
            atomic::{AtomicU16, Ordering},
            Arc,
        },
        time::Duration,
    };

    use tokio::sync::RwLock;

    use crate::{
        constants::DUMMY_REGISTER_ID,
        types::{CommandId, RawAnswer, RawCommand},
    };

    /// A wrapper around a [`BoundedHashMap`] which provides functionality
    /// specific to dealing with commands and answers.
    ///
    /// Clones of this type point to the same underlying data structure. This allows
    /// for different threads to write/read the same data.
    #[derive(Clone, Debug)]
    pub struct Answers {
        answers: Arc<RwLock<BoundedHashMap<CommandId, RawAnswer>>>,
    }

    impl Answers {
        /// Create a new answer map with the given capacity.
        ///
        /// The capacity is the maximum number of answers that can be stored at any given time.
        /// If the capacity is reached, the oldest answer is removed first.
        pub fn new(capacity: usize) -> Self {
            Answers {
                answers: Arc::new(RwLock::new(BoundedHashMap::new(capacity))),
            }
        }

        /// Clear all answers from the map.
        pub async fn clear(&self) {
            let mut answers = self.answers.write().await;
            answers.clear();
        }

        /// Get the answer with the given ID.
        #[allow(unused)]
        pub async fn get(&self, id: CommandId) -> Option<RawAnswer> {
            let answers = self.answers.read().await;
            answers.get(&id).cloned()
        }

        /// Insert an answer into the map.
        pub async fn insert(&self, answer: RawAnswer) {
            let id = parse_answer_id(&answer).unwrap_or(DUMMY_REGISTER_ID);
            let mut answers = self.answers.write().await;
            answers.insert(id, answer);
        }

        /// Remove an answer from the map.
        #[allow(unused)]
        pub async fn remove(&self, id: CommandId) -> Option<RawAnswer> {
            let mut answers = self.answers.write().await;
            answers.remove(&id)
        }

        pub async fn wait_answer(&self, id: CommandId, timeout: Duration) -> Option<RawAnswer> {
            let answers = self.answers.clone();
            tokio::time::timeout(timeout.clone(), async {
                loop {
                    if answers.read().await.contains_key(&id) {
                        break answers.write().await.remove(&id).unwrap();
                    }
                    tokio::time::sleep(Duration::from_millis(1)).await;
                }
            })
            .await
            .ok()
        }
    }

    /// HashMap that implements LRU eviction once a given capacity is reached.
    #[derive(Clone, Debug)]
    struct BoundedHashMap<K: Eq + Hash + Clone + Debug, V: Debug> {
        /// The maximum number of elements that are allowed to be stored in the hashmap.
        capacity: usize,
        /// The internal hashmap.
        map: HashMap<K, V>,
        /// Tracks the order of insertion.
        ///
        /// A linked list is more efficient than a Vec, but `remove` is not available
        /// in stable Rust.
        order: Vec<K>,
    }

    impl<K: Eq + Hash + Clone + Debug, V: Debug> BoundedHashMap<K, V> {
        pub fn new(capacity: usize) -> Self {
            Self {
                capacity,
                map: HashMap::with_capacity(capacity),
                order: Vec::with_capacity(capacity),
            }
        }

        pub fn contains_key(&self, k: &K) -> bool {
            self.map.contains_key(k)
        }

        pub fn len(&self) -> usize {
            self.map.len()
        }

        pub fn get(&self, key: &K) -> Option<&V> {
            self.map.get(key)
        }

        pub fn insert(&mut self, k: K, value: V) {
            self.touch(&k);
            self.map.insert(k, value);
        }

        pub fn remove(&mut self, k: &K) -> Option<V> {
            self.order.retain(|e| e != k);
            self.map.remove(k)
        }

        pub fn clear(&mut self) {
            self.map.clear();
            self.order.clear();
        }

        fn drop_oldest(&mut self) {
            let k = self.order.pop().unwrap();
            self.map.remove(&k);
        }

        fn touch(&mut self, k: &K) {
            if let Some(pos) = self.order.iter().position(|x| x == k) {
                self.order.remove(pos);
            } else if self.len() >= self.capacity {
                self.drop_oldest();
            }
            self.order.insert(0, k.clone());
        }
    }

    /// Parse the ID from an answer. Since this only works for control registers,
    /// this function will return `None` for other types.
    #[must_use]
    fn parse_answer_id(answer: &RawAnswer) -> Option<CommandId> {
        const REQUIRED_FIRST_BYTE: u8 = 0xAD;
        const ID_START: usize = 4;
        const ID_END: usize = ID_START + std::mem::size_of::<CommandId>();
        match answer.len() {
            n if n < ID_END => None,
            _ if answer[0] != REQUIRED_FIRST_BYTE => None,
            _ => {
                // SAFETY: indexing is safe since the length of `answer` is checked above.
                // SAFETY: `unwrap()` is safe since the length of the slice is
                // guaranteed to be the correct length for `CommandId`.
                let id_bytes = answer[ID_START..ID_END].try_into().unwrap();
                Some(CommandId::from_be_bytes(id_bytes))
            }
        }
    }

    /// Set the ID for a command.
    ///
    /// If the ID for the command can be set, the command is modified and the
    /// same ID is returned. If the ID cannot be set, the command is left
    /// unmodified and `None` is returned.
    #[must_use]
    pub(super) fn set_command_id(command: &mut RawCommand) -> Option<CommandId> {
        let id = next_command_id();
        const REQUIRED_FIRST_BYTE: u8 = 0xAD;
        const ID_START: usize = 2;
        const ID_END: usize = ID_START + std::mem::size_of::<CommandId>();
        match command.len() {
            n if n < ID_END => None,
            _ if command[0] != REQUIRED_FIRST_BYTE => None,
            _ => {
                command[ID_START..ID_END].copy_from_slice(&id.to_be_bytes());
                Some(id)
            }
        }
    }

    /// Generate a new command ID. Each time this function is called, the command ID increments by 1.
    /// This function is free of race conditions; parallel calls will never return identical IDs.
    ///
    /// The command IDs start at 1 rather than 0 since 0 is a common command ID.
    /// When the maximum command ID is reached, the IDs will roll over to 1.
    fn next_command_id() -> CommandId {
        static COUNTER: AtomicU16 = AtomicU16::new(1);
        let mut id = COUNTER.fetch_add(1, Ordering::Relaxed);
        // The zero ID is reserved for commands that cannot be assigned an ID.
        if id == 0 {
            id = COUNTER.fetch_add(1, Ordering::Relaxed);
        }
        id
    }
}
