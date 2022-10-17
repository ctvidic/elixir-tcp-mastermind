# Mastermind the color game

This is a client-server implementation of the Mastermind color game.
See [How to play Mastermind](https://www.wikihow.com/Play-Mastermind)

## Rules of the game

One player (the server) will pick four different pins out of six
different colors that are hidden from the other player (the client).

The client player now presents a guess of four ordered colored pins to
the server and note that multiple pins can have the same color. The
server responds back with two values, the number of pins with the
correct color and how many of those are in the right place.

The client player now uses this response from the server to make
another (better?) guess until the response from the server is
four and four.

## Implementation and Protocol

The server starts by selecting a random list of four elements of six colors represented
as numbers `0..5`, i.e. `0423`. Then it begins to listen to TCP port 4321 for
inbound connections from a client.

Once a client connection comes in on the listen socket, the server accepts the
connection, parses the message from the client and sends a response, all while
continuing to listen for new connections on the listening socket. The server
can serve many clients at the same time.

A typical exchange between a server and a client is shown below, when the server
has chosen the colors `0432`.

| Client message | Server response | Remarks                                   |
|----------------|-----------------|-------------------------------------------|
| "1 2 3 4"      | "3 1\r\n"       | 2,3 and 4 are there, 3 in the right place |
| "0 2 4 3"      | "4 1\r\n"       | all right colors, 1 in the right place    |
| "0 4 3 2"      | "4 4\r\n"       | Solved!                                   |

**Note**: Colors in the client message should be separated by one space character
and can optionally be terminated with any combination of `\r` (carriage return) an
`\n` (line feed).

The server response will be two numbers `0..4` separated by one space and terminated
with `\r\n`. This allows for testing the server with a any Telnet program.

## Running the test server

Make sure you have Python 3 installed, then go into the Python directory in this
repo and run:

```shell
./mastermind_server 0.0.0.0 4321
```

You will see debug messages from the server in this terminal, including the random
colors it picked.

## Using a Telnet client

In a separate terminal run the telnet program to connect to the server:

```shell
telnet localhost 4321
```

Then simply enter your guess as a single line of four numbers separated by spaces
and the server will respond with a line of two numbers as described above. If you
guess right (or cheat by looking at the server log), the server will respond with
`4 4` and close the connection.

If you want to quit the telnet client you can hit `control-]` and type `quit` at the
telnet prompt.

## Using the test client

From the `Python` directory open a separate terminal to run the client:

```shell
./mastermind_client localhost 4321
```

Then enter your guess as a single line of four numbers separated by spaces
and the server will respond with a line of two numbers as described above. If you
guess right (or cheat by looking at the server log), the server will respond with
`4 4` and close the connection.

