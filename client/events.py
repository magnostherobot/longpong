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

    def is_quit(event):
        return event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == sdl2.SDLK_ESCAPE

    def has_quit(self):
        return self.has(is_quit)

    def is_space(event):
        return event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == sdl2.SDLK_SPACE

    def has_space(self):
        return self.has(is_space)

    def is_return(event):
        return event.type == sdl2.SDL_KEYUP and event.key.keysym.sym == sdl2.SDLK_RETURN

    def has_return(self):
        return self.has(is_enter)

    def is_num(event):
        is_keyup = event.type == sdl2.SDL_KEYUP
        lower_bound = sdl2.SDLK_0
        upper_bound = sdl2.SDLK_9
        keysym = event.key.keysym.sym
        return keysym >= lower_bound and keysym <= upper_bound

    def get_num(event):
        is_keyup = event.type == sdl2.SDL_KEYUP
        lower_bound = sdl2.SDLK_0
        upper_bound = sdl2.SDLK_9
        keysym = event.key.keysym.sym
        if keysym >= lower_bound and keysym <= upper_bound:
            return keysym - lower_bound

    def has_num(self):
        return self.has(is_num)

    def get_nums(self):
        return list(map(get_num, self.matching(is_num)))

    def has_key(self, keysym):
        return keysym in self.keys
