FROM gcc:latest
COPY . /hello_world
WORKDIR /hello_world
RUN g++ -o hello_world hello_world.cpp
CMD ["./hello_world"]