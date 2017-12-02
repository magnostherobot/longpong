import sdl2
import sdl2.ext

class Events:
    def __init__(self):
        self.keys = set()

    def poll(self):
        self.events = []
        for event in sdl2.ext.get_events():
            self.update_keys(event)
            self.events.append(event)

    def update_keys(self, event):
        if event.type == sdl2.SDL_KEYDOWN:
            self.keys.add(event.key.keysym.sym)
        elif event.type == sdl2.SDL_KEYUP:
            self.keys.remove(event.key.keysym.sym)

    def matching(self, pred):
        return list(filter(pred, self.events))

    def has(self, pred):
        return len(self.matching(pred)) > 0

    def is_quit(self, event):
        return event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == sdl2.SDLK_ESCAPE

    def has_quit(self):
        return self.has(self.is_quit)

    def is_space(self, event):
        return event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == sdl2.SDLK_SPACE

    def has_space(self):
        return self.has(self.is_space)

    def is_return(self, event):
        return event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == sdl2.SDLK_RETURN

    def has_return(self):
        return self.has(self.is_return)

    def is_num(self, event):
        is_keyup = event.type == sdl2.SDL_KEYUP
        lower_bound = sdl2.SDLK_0
        upper_bound = sdl2.SDLK_9
        keysym = event.key.keysym.sym
        return keysym >= lower_bound and keysym <= upper_bound

    def get_num(self, event):
        is_keyup = event.type == sdl2.SDL_KEYUP
        lower_bound = sdl2.SDLK_0
        upper_bound = sdl2.SDLK_9
        keysym = event.key.keysym.sym
        if keysym >= lower_bound and keysym <= upper_bound:
            return keysym - lower_bound

    def has_num(self):
        return self.has(self.is_num)

    def is_n(self, event):
        return event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == sdl2.SDLK_n

    def has_n(self):
        return self.has(self.is_n)

    def get_nums(self):
        return list(map(self.get_num, self.matching(self.is_num)))

    def has_key(self, keysym):
        return keysym in self.keys
