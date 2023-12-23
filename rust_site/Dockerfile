FROM rust:latest as build

RUN USER=root cargo new --bin rust_site
WORKDIR /rust_site
COPY ./Cargo.lock ./Cargo.lock
COPY ./Cargo.toml ./Cargo.toml
RUN cargo build --release
#RUN cargo build --target aarch64-unknown-linux-musl --release
RUN rm src/*.rs

COPY ./src ./src
RUN rm ./target/release/deps/rust_site*
RUN cargo build --release
#RUN cargo build --target aarch64-unknown-linux-musl  --release
#RUN chmod +x ./target/release/rust_site

#FROM rust:slim
#FROM alpine:latest
FROM ubuntu:latest

#WORKDIR /src/static
COPY --from=build /rust_site/target/release/rust_site . 
#COPY --from=build /rust_site/target/release/rust_site ./src/static/rust_site
COPY ./src/static/index.html ./src/static/index.html	

#WORKDIR /src/static
CMD ["./rust_site"]
