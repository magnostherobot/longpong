import socket
import sys
import json

class Client:
    def __init__(self,ip,port,n):
        self.started = False
        self.stopped = False
        self.msgs =[]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip,port))
        self.n = n
        self.sock.setblocking(False)

    def listen(self):
        try:
            msg = self.sock.recv(4096)
            jsonMSG = json.loads(msg.decode())
            print(jsonMSG)
            if 'command' in jsonMSG:
                val = jsonMSG['command']
                if val == 'start':
                    self.started = True
                    self.startupMessage = jsonMSG
                    self.msgs.append(jsonMSG)
                elif val =='stop':
                        self.stopped = True
                        self.stoppedMessage = jsonMSG
                else:
                        self.msgs.append(jsonMSG)
            else:
                print("It really shouldn't be here")

        except socket.error as e:
            pass

    def get_messages(self):
        ret = self.msgs[:]
        self.msgs = []
        return ret

    def send_init(self,screen):
        inp = {}
        inp['info'] = {
                "scr_i":  self.n,
                "scr_w": screen
        }
        self.sock.sendall(str(json.dumps(inp)).encode())

    def send_start(self):
        msg ={'command':'start'}
        jsonVal = json.dumps(msg)
        self.sock.sendall(str(jsonVal).encode())

    def send_stop(self):
        msg ={'command':'stop'}
        jsonVal = json.dumps(msg)
        self.sock.sendall(str(jsonVal).encode())

    def send_ballchange(self, msg):
        msg['command'] = "bchange"
        jsonVal = json.dumps(msg)
        self.sock.sendall(str(jsonVal).encode())

    def has_started(self):
        return self.started

    def has_stopped(self):
        return self.stopped
