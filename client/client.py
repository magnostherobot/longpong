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
            jsonMSG = json.loads(msg)
            print(jsonMSG)
            if 'command' in data:
                val = jsonMSG['command']
                if val == 'start':
                    self.started = True
                    self.startupMessage = jsonMSG
                elif val =='stop':
                        self.stopped = True
                        self.stoppedMessage = jsonMSG
                else:
                        msgs.append(jsonMSG)
            else:
                print("It really shouldn't be here")

        except socket.error as e:
            pass

    def get_messages(self):
        ret = self.msgs[:]
        self.msgs = []

    def send_init(self,screen):
        inp = {}
        inp['nValue'] = self.n;
        inp['screenSize'] = str(screen)
        self.sock.sendall(str(json.dumps(inp)).encode())

    def send_start(self):
        msg ={'command':'start'}
        jsonVal = json.dumps(msg)
        self.sock.sendall(str(jsonVal).encode())

    def send_stop(self):
        msg ={'command':'stop'}
        jsonVal = json.dumps(msg)
        self.sock.sendall(str(jsonVal).encode())

    def send_ballchange(self,message):
        msg['command'] = "bchange"
        jsonVal = json.dumps(msg)
        self.sock.sendall(str(jsonVal).encode())

    def has_started(self):
        return self.started

    def has_stopped(self):
        return self.stopped
