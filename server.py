
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

from headers import *
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from parse import *

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
    available_nonces = set(range(10000))

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
        # print clientaddr, "has connected"
        self.input_list.append(clientsock)

    def on_close(self):
        # print self.s.getpeername(), "has disconnected"
        self.input_list.remove(self.s)

    def on_recv(self, sockfd):
        data = self.data
        # here we can parse and/or modify the data before send forward
        print data
        #if request.command == "GET":
        if data[0:4] == "PORT":
            self.add_port(sockfd, data)
        elif HeaderN.is_n(data):
            code = HeaderN.extract(data)
            print "CODE: ", code[0]
            if code[0] == "-1":
                self.send_nonce(sockfd)
            else:
                self.nonce_returned(code[0])

    def add_port(self, sockfd, data):
            port_and_key = parse("PORT {}\n{}", data).fixed
            self.ports[str(sockfd)] = (sockfd.getsockname()[0], int(port_and_key[0]), port_and_key[1])
            for client in self.ports.values():
                self.client = socket.socket()
                self.client.connect((client[0], client[1]))
                self.client.sendall("PORTS" + str(self.ports))
                self.client.close()

    def send_nonce(self, sockfd):
            nonce = random.choice(tuple(self.available_nonces))
            self.available_nonces.remove(nonce)
            print str(nonce)
            msg = HeaderN.add(str(nonce))
            sockfd.sendall(msg)

    def nonce_returned(self, nonce):
            self.available_nonces.add(nonce)


if __name__ == '__main__':
        server = TheServer('', 9099)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)