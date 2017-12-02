# longpong

longpong is a game of Pong that spans multiple screens and computers.

## Starting a game of longpong

First, start a server:

    node server/server.js <port>

Now start one client on each computer:

    python3 client/longpong.py <server_ip> <server_port> <index> <num_windows>

- `<index>` is the client's index in the list of clients, starting at 0, from left to right.
- `<num_windows>` is the number of windows that this client should have.

In each client, position the windows as desired, typing the window's number (see its title) to make it fullscreen on its current screen. Press `return` when the windows are positioned.

When all of the clients are ready, press `space` on one of the clients to tell the server that the clients are all ready to start. The game then begins.

Control your paddle with the up and down arrow keys.

## Dependencies

- `python3`
- `PySDL2`
