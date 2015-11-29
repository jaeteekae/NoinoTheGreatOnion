
#!/usr/bin/python
# This is a simple port-forward / proxy, written using only the default python
# library. If you want to make a suggestion or fix something you can contact-me
# at voorloop_at_gmail.com
# Distributed over IDC(I Don't Care) license
import socket
import select
import time
import sys
import random

from headers import HeaderK
from headers import HeaderR
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001
forward_to = ('smtp.zaz.ufsk.br', 25)




class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

class TheServer:
    input_list = []
    ports = {}

    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv(self.s)

    def on_accept(self):
        clientsock, clientaddr = self.server.accept()
        print clientaddr, "has connected"
        self.input_list.append(clientsock)

    def on_close(self):
        print self.s.getpeername(), "has disconnected"
        self.input_list.remove(self.s)

    def on_recv(self, sockfd):
        data = self.data
        # here we can parse and/or modify the data before send forward
        print data
        #if request.command == "GET":
        if data[0:4] == "PORT":
            self.add_port(sockfd, int(data[5:]))
        else:
            self.create_path(data, sockfd)

    def add_port(self, sockfd, port):
            self.ports[str(sockfd)] = (sockfd.getsockname()[0], port)
            for client in self.ports.values():
                self.client = socket.socket()
                self.client.connect((client[0], client[1]))
                self.client.sendall("PORTS" + str(self.ports))
                self.client.close()

    def create_path(self, data, sockfd):
        self.client = socket.socket()
        self.client.connect((sockfd.getsockname()[0], self.ports[str(sockfd)][1]))
        self.client.sendall("PORTSMessage: " + data + "\nPorts: " + str(self.ports) + "\n")
        self.client.close()
        # indexes = set(range(len(self.ports)))
        # #indexes.remove(0)
        # path = []
        # i = 0
        # self.current_connections[sockfd.getsockname()[0] = random.randint(1, 100000)
        # print self.current_connections

        # # find random path of length three from existing clients
        # while i < 3:
        #     if len(indexes) == 0:  # if we are out of nodes
        #         break
        #     node = random.choice(tuple(indexes))
        #     indexes.remove(node)
        #     if self.ports.keys()[node] == sockfd: # if node is that of transmitting client
        #         continue
        #     path.append(self.ports.values()[node])
        #     i = i + 1


        # initial = HeaderK.add(HeaderK(), str(self.current_connections[sockfd.getsockname()[0]]), data)

        # if path:
        #     step = path.pop()
        #     full = HeaderR.add(HeaderR(), str(step[0]), str(step[1]), str(initial))
        #     while path:
        #         step = path.pop()
        #         full = HeaderR.add(HeaderR(), str(step[0]), str(step[1]), str(full))
        #     self.client = socket.socket()
        #     self.client.connect((step[0], step[1]))
        #     self.client.sendall(str(full))
        #     self.client.close()
        #     print str(full)
        # else:
        #     print str(initial)



        #print path


if __name__ == '__main__':
        server = TheServer('', 9099)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)