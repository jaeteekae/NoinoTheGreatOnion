
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



class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception, e:
            print e
            return False

class TheServer:
    input_list = []
    channel = {}

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
        #remove objects from input_list
        self.input_list.remove(self.s)
        #self.input_list.remove(self.channel[self.s])
        #out = self.channel[self.s]
        # close the connection with client
        #self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        #self.channel[self.s].close()
        # delete both objects from channel dict
        #del self.channel[out]
        #del self.channel[self.s]

    def on_recv(self, sockfd):
        data = self.data
        # here we can parse and/or modify the data before send forward
        request = HTTPRequest(data)
        print data
        if request.command == "GET":
            self.create_path(data, sockfd)

    def create_path(self, data, sockfd):
        indexes = set(range(len(self.input_list)))
        bob = indexes.remove(random.choice(list(indexes)))
        print bob

        print sockfd


if __name__ == '__main__':
        server = TheServer('', 9099)
        try:
            server.main_loop()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)