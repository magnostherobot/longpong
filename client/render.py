import ctypes
import sdl2
import sdl2.ext

from bitfont import bitfont

class Screen:
    def __init__(self, title, counter, dimensions):
        self.window = sdl2.ext.Window(title + " " + str(counter + 1), dimensions, flags = sdl2.SDL_WINDOW_RESIZABLE)
        self.renderer = sdl2.ext.Renderer(self.window)

    @property
    def width(self):
        return self.window.size[0]

    @property
    def height(self):
        return self.window.size[1]

class Renderer:
    def __init__(self, title, dimensions, num_windows, fg = (255, 255, 255), bg = (0, 0, 0)):
        """
        Initialise the renderer with a foreground colour and a background colour
        and create an SDL2 window for drawing to. This assumes that SDL2 has
        already been initialised.

        Arguments:
        title -- the title to give the client windows
        dimensions -- the dimensions (in pixels) at which to start the windows
        num_windows -- the number of windows to run the client with

        Keyword arguments:
        fg -- the foreground colour to draw with (default (255, 255, 255))
        bg -- the background colour to draw with (default (0, 0, 0))
        """
        self.fg = fg
        self.bg = bg
        self.offset = 0
        self.screens = []
        for i in range(num_windows):
            screen = Screen(title, i, dimensions)
            self.screens.append(screen)
            screen.window.show()

    def set_offset(self, offset):
        """Set this client's offset in the full-sized screen made by all clients."""
        self.offset = offset

    def render(self, balls, paddles, score):
        offset = self.offset
        for screen in self.screens:
            # Clear the screen with the background colour
            screen.renderer.color = sdl2.ext.Color(self.bg[0], self.bg[1], self.bg[2], 255)
            sdl2.SDL_RenderClear(screen.renderer.sdlrenderer)
            # Set a muted foreground colour for drawing the score
            screen.renderer.color = sdl2.ext.Color(self.fg[0] / 3, self.fg[1] / 3, self.fg[2] / 3, 255)
            self.draw_score(screen, score)
            # Set the foreground colour for drawing
            screen.renderer.color = sdl2.ext.Color(self.fg[0], self.fg[1], self.fg[2], 255)
            # Draw the elements
            for ball in balls:
                self.draw_ball(screen, offset, ball)
            for paddle in paddles:
                self.draw_paddle(screen, offset, paddle)
            # Display this screen
            sdl2.SDL_RenderPresent(screen.renderer.sdlrenderer)
            # Increase the rendering offset
            offset += float(screen.width) / float(screen.height)

    def draw_ball(self, screen, offset, ball):
        if ball != None:
            rect = sdl2.SDL_Rect(int((ball.pos[0] - offset) * screen.height),
                    int(ball.pos[1] * screen.height),
                    int(ball.size[0] * screen.height),
                    int(ball.size[1] * screen.height))
            sdl2.SDL_RenderFillRect(screen.renderer.sdlrenderer, rect)

    def draw_paddle(self, screen, offset, paddle):
        if paddle != None:
            rect = sdl2.SDL_Rect(int((paddle.pos[0] - offset) * screen.height),
                    int(paddle.pos[1] * screen.height),
                    int(paddle.size[0] * screen.height),
                    int(paddle.size[1] * screen.height))
            sdl2.SDL_RenderFillRect(screen.renderer.sdlrenderer, rect)
    
    def draw_score(self, screen, scores):
        size = 20
        offset = 0
        for score in map(bitfont, scores):
            side = offset == 0
            offset = self.from_center(screen, len(score), size, side)
            for digit in score:
                offset_x = offset
                offset_y = size
                for i in range(len(digit)):
                    if i > 0 and i % 3 == 0:
                        offset_y += size
                        offset_x = offset
                    if digit[i]:
                        rect = sdl2.SDL_Rect(offset_x, offset_y, size, size)
                        sdl2.SDL_RenderFillRect(screen.renderer.sdlrenderer, rect)
                    offset_x += size
                offset = offset_x + size
            offset += 2 * size

    def from_center(self, screen, count, size, side):
        if side:
            return int(screen.width / 2 - count * size * 4 - 2 * size)
        else:
            return int(screen.width / 2 + 2 * size)

    def maximise_window(self, index):
        if index > 0 and index <= len(self.screens):
            window = self.screens[index - 1].window
            rect = sdl2.SDL_Rect()
            sdl2.SDL_GetDisplayBounds(index - 1, ctypes.byref(rect))
            sdl2.SDL_SetWindowSize(window.window, rect.w, rect.h)
            sdl2.SDL_SetWindowFullscreen(window.window, sdl2.SDL_WINDOW_FULLSCREEN)

    def get_rightmost_edge(self):
        """Get the relative coordinate of the rightmost edge."""
        return self.offset + sum(self.get_screen_widths())

    def get_screen_widths(self):
        """Get the relative screen widths in screen order."""
        # Window height is '1' between all clients, so divide the width by the height
        return list(map(lambda screen: float(screen.width) / float(screen.height), self.screens))
