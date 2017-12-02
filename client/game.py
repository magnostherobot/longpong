import time
import sdl2
import sdl2.ext

class Rect:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Ball:
    def __init__(self, pos, vel, size):
        self.pos = pos
        self.vel = vel
        self.size = size

    def move(self, dt):
        self.pos = (
                self.pos[0] + (self.vel[0] * dt),
                self.pos[1] + (self.vel[1] * dt)
                )

    def is_touching_paddle(self, paddle):
        return not (
                self.pos[0] > paddle.pos[0] + paddle.size[0] or
                self.pos[1] > paddle.pos[1] + paddle.size[1] or
                self.pos[0] + self.size[0] < paddle.pos[0] or
                self.pos[1] + self.size[1] < paddle.pos[1]
                )

class Paddle:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size 
        
class Game:
    def __init__(self, client, events, renderer):
        self.client = client
        self.events = events
        self.renderer = renderer
        self.paddle_list = []
        self.ball_list = []

    def start(self):
        self.place_windows()
        # Tell the server how wide the screen is
        full_width = sum(self.renderer.get_screen_widths)
        self.client.send_init(full_width)
        # Wait for a start event
        while not self.client.has_started():
            self.client.listen()
            if self.client.has_started():
                msg = self.client.get_messages()
                self.renderer.set_offset(msg[0]['offset'])
                self.ball_list[msg[0]['ball_id']] = Ball(msg[0]['pos'],msg[0]['vel'],msg[0]['size'])
                if (msg[0]['offset'] == 0):
                    self.paddle_list.append(Paddle((0.1, 0.1), (0.01, 0.1)))
                elif (self.renderer.get_rightmost_edge() == msg[0]['total_w']):
                    self.paddle_list.append(Paddle((0.1, 0.1), (0.01, 0.1)))
                break
            # Tell the server to start if the spacebar is pressed
            self.events.poll()
            if self.events.has_space():
                self.client.send_start()
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
            if self.events.has_quit() or self.client.has_stopped():
                self.running = False
                break
            self.update(None)
            self.renderer.render(None, None)

    def update(self, time, p_time):
        deltaT = time - p_time
        msgs = self.client.get_messages
        touched = [False for x in ball_list]
        for msg in msgs:
            if (msg['command'] == 'bchange'):
                touched[msg['ball_id']] = True

                if vel in msg:
                    ball.vel = (msg['vel'][0], msg['vel'][1])
                if pos in msg:
                    ball.pos = (msg['pos'][0], msg['pos'][1])
                if size in msg:
                    ball.size = (msg['size'][0], msg['size'][1])

                l_deltaT = time - msg['time']
                ball.move(l_deltaT)
        for i, ball in enumerate(ball_list):
            # move the balls
            if not touched[i]:
                ball.move(deltaT)
            # bounce the balls off the walls
            if (ball.pos[1] <= 0):
                ball.vel[1] = -ball.vel[1]
            elif (ball.pos[1] + ball.size[1] >= 1):
                ball.vel[1] = -ball.vel[1]
            # bounce the balls off the paddles
            for paddle in paddle_list:
                if ball.is_touching(paddle):
                    ball.vel[0] = -1.1 * ball.vel[0]
                    ball.vel[1] = ball.vel[1] + 1 * ((paddle.pos[1] + (paddle.size[1] / 2)) - (ball.pos[1] + (ball.size[1] / 2)))
                    msg = {
                        'ball_id': i,
                        'vel': {
                            'x': ball.vel[0],
                            'y': ball.vel[1]
                        },
                        'pos': {
                            'x': ball.pos[0],
                            'y': ball.pos[1]
                        },
                        'time': time.time()
                    }
                    self.client.send_ballchange(msg)

