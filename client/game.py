import sdl2
import sdl2.ext

class Game:
    def __init__(self, client, events, renderer):
        self.client = client
        self.events = events
        self.renderer = renderer

    def start(self):
        # Place the windows
        while True:
            self.events.poll()
            if self.events.has_num():
                for numkey in self.events.get_nums():
                    renderer.maximise_window(numkey)
            if self.events.has_return():
                break
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
        # TODO: set the renderer offset
        # Run the game loop
        self.loop()

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
