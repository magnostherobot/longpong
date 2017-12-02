import time
import sdl2
import sdl2.ext
import sys

class Ball:
    def __init__(self, pos, vel, size):
        self.pos = (pos['x'], pos['y'])
        self.vel = (vel['x'], vel['y'])
        self.size = (size['x'], size['y'])

    def __str__(self):
        return str(self.pos) + str(self.vel) + str(self.size)

    def move(self, dt):
        self.pos = (
                self.pos[0] + (self.vel[0] * dt) / 5,
                self.pos[1] + (self.vel[1] * dt) / 5,
                )

    def is_touching(self, paddle):
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
        self.ball_list = {}

    def start(self):
        self.place_windows()
        # Tell the server how wide the screen is
        full_width = sum(self.renderer.get_screen_widths())
        self.client.send_init(full_width)
        # Wait for a start event
        while not self.client.has_started():
            self.client.listen()
            if self.client.has_started():
               
                msg = self.client.get_messages()
                print("message is "+ str(msg))
                if msg != []:
                    self.renderer.set_offset(msg[0]['info']['offset'])
                    self.ball_list[msg[0]['ball_id']] = Ball(msg[0]['pos'],msg[0]['vel'],msg[0]['size'])
                    print(self.ball_list)
                    if (msg[0]['info']['offset'] == 0):
                        self.paddle_list.append(Paddle((0.1, 0.1), (0.05, 0.2)))
                    rightmost_edge = self.renderer.get_rightmost_edge()
                    if (rightmost_edge == msg[0]['info']['total_w']):
                        self.paddle_list.append(Paddle((rightmost_edge - 0.05 - 0.1, 0.1), (0.05, 0.2)))
                    break
            # Tell the server to start if the spacebar is pressed
            self.events.poll()
            if self.events.has_quit():
                sys.exit(0)
            if self.events.has_space():
                self.client.send_start()
        # Run the game loop
        self.loop()

    def place_windows(self):
        while True:
            self.events.poll()
            if self.events.has_quit():
                sys.exit(0)
            if self.events.has_num():
                for numkey in self.events.get_nums():
                    self.renderer.maximise_window(numkey)
            if self.events.has_return():
                break

    def loop(self):
        self.running = True
        c_time = time.time()
        while self.running:
            self.client.listen()
            # Quit on quit input or when the server stops
            self.events.poll()
            if self.events.has_quit() or self.client.has_stopped():
                self.running = False
                break
            p_time = c_time
            c_time = time.time()
            self.update(c_time, p_time)
            self.renderer.render(self.ball_list.values(), self.paddle_list, (0, 0))

    def update(self, c_time, p_time):
        deltaT = c_time - p_time
        msgs = self.client.get_messages()
        touched = {x : False for x in self.ball_list}  
        for msg in msgs:
            if (msg['command'] == 'bchange'):
                touched[msg['ball_id']] = True
                ball = self.ball_list[msg['ball_id']]
                if 'vel' in msg:
                    ball.vel = (msg['vel']['x'], msg['vel']['y'])
                if 'pos' in msg:
                    ball.pos = (msg['pos']['x'], msg['pos']['y'])
                if 'size' in msg:
                    ball.size = (msg['size']['x'], msg['size']['y'])

                l_deltaT = c_time - msg['time']
                ball.move(l_deltaT)

        for i, ball in self.ball_list.items():
            if not touched[i]:
                ball.move(deltaT)
            # bounce the balls off the walls
            if (ball.pos[1] <= 0):
                ball.vel = (ball.vel[0], -ball.vel[1])
            elif (ball.pos[1] + ball.size[1] >= 1):
                ball.vel = (ball.vel[0], -ball.vel[1])
            # bounce the balls off the paddles
            for paddle in self.paddle_list:
                if ball.is_touching(paddle):
                    ball.vel = (-1.1 * ball.vel[0],
                            ball.vel[1] + 1 * ((paddle.pos[1] + (paddle.size[1] / 2)) - (ball.pos[1] + (ball.size[1] / 2))))
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
                        'time': c_time
                    }
                    self.client.send_ballchange(msg)

