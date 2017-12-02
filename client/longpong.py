import sdl2.ext
import sys

import client
import events
import game
import render

def main(args):
    sdl2.ext.init()

    ip = args[1]
    port = args[2]
    num = args[3]
    num_windows = int(args[4])

    client = Client(ip, port, num)
    events = Events()
    renderer = Renderer('looongpooong', (800, 600), num_windows)
    game = Game(client, events, renderer)

    sdl2.ext.stop()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
