# References:
# https://www.docker.com/blog/cross-compiling-rust-code-for-multiple-architectures/
#
FROM rust:latest

RUN apt update && apt upgrade -y
RUN apt -y install g++-arm-linux-gnueabihf libc6-dev-armhf-cross
# RUN rustup target add 

RUN rustup target add armv7-unknown-linux-gnueabihf 
RUN rustup toolchain install stable-armv7-unknown-linux-gnueabihf

WORKDIR /app
# COPY .cargo ./.cargo
# COPY Cargo.toml Cargo.lock ./
# COPY src ./src
# COPY ./.cargo/config ./.cargo/config
ENV CARGO_TARGET_ARMV7_UNKNOWN_LINUX_GNUEABIHF_LINKER=arm-linux-gnueabihf-gcc CC_armv7_unknown_Linux_gnueabihf=arm-linux-gnueabihf-gcc CXX_armv7_unknown_linux_gnueabihf=arm-linux-gnueabihf-g++

CMD ["cargo", "build", "--release", "--target", "armv7-unknown-linux-gnueabihf"]
