import sdl2
import sdl2.ext

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Game:
    def __init__(self, client, events, renderer):
        self.client = client
        self.events = events
        self.renderer = renderer

    def start(self):
        self.place_windows()
        # Tell the server how wide the screen is
        full_width = sum(self.renderer.get_screen_widths)
        self.client.send_init(full_width)
        # Wait for a start event
        while not self.client.has_started():
            self.client.listen()
            if self.client.has_started():
                break
            # Tell the server to start if the spacebar is pressed
            self.events.poll()
            if self.events.has_space():
                self.client.send_start()
        self.renderer.set_offset(client.get_messages()[0]['screen_offset'])
        # Run the game loop
        self.loop()

    def place_windows(self):
        while True:
            self.events.poll()
            if self.events.has_num():
                for numkey in self.events.get_nums():
                    self.renderer.maximise_window(numkey)
            if self.events.has_return():
                break

    def loop(self):
        self.running = True
        while self.running:
            self.client.listen()
            # Quit on quit input or when the server stops
            self.events.poll()
            if self.events.is_quit() or self.client.has_stopped():
                self.running = False
                break
            self.update(None)
            self.renderer.render(None, None)

    def update(self, diff):
        pass
