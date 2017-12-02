import sdl2.ext
import sys

from client import Client
from events import Events
from game import Game
from render import Renderer

def main(args):
    sdl2.ext.init()

    ip = args[1]
    port = int(args[2])
    num = args[3]
    num_windows = int(args[4])

    client = Client(ip, port, num)
    events = Events()
    renderer = Renderer('looongpooong', (800, 600), num_windows)
    game = Game(client, events, renderer)
    game.start()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
