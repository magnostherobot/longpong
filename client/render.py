import sdl2
import sdl2.ext

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
        """
        self.fg = fg
        self.bg = bg
        self.screens = []
        for i in range(num_windows):
            screen = Screen(title, i, dimensions)
            self.screens.append(screen)
            screen.window.show()

    def render(self, ball, paddle):
        for screen in self.screens:
            # Clear the screen with the background colour
            screen.renderer.color = sdl2.ext.Color(self.bg[0], self.bg[1], self.bg[2], 255)
            sdl2.SDL_RenderClear(screen.renderer.sdlrenderer)
            # Set the foreground colour for drawing
            screen.renderer.color = sdl2.ext.Color(self.fg[0], self.fg[1], self.fg[2], 255)
            # Draw the elements
            self.draw_ball(screen.renderer, ball)
            self.draw_paddle(screen.renderer, paddle)
            # Display this screen
            sdl2.SDL_RenderPresent(screen.renderer.sdlrenderer)

    def draw_ball(self, renderer, ball):
        if ball != None:
            rect = sdl2.SDL_Rect(ball.x, ball.y, ball.width, ball.height)
            sdl2.SDL_RenderFillRect(renderer.sdlrenderer, rect)

    def draw_paddle(self, renderer, paddle):
        if paddle != None:
            rect = sdl2.SDL_Rect(paddle.x, paddle.y, paddle.width, paddle.height)
            sdl2.SDL_RenderFillRect(renderer.sdlrenderer, rect)

    def maximise_window(self, index):
        if index > 0 and index <= len(self.screens):
            window = self.screens[index - 1].window
            window.maximize()
            sdl2.SDL_SetWindowFullscreen(window.window, sdl2.SDL_WINDOW_FULLSCREEN)

    def get_screen_widths(self):
        """
        Get the relative screen widths in screen order.
        """
        # Window height is '1' between all clients, so divide the width by the height
        return list(map(lambda screen: float(screen.width) / float(screen.height), self.screens))
