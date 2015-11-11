#!/usr/bin/python           # This is client.py file

# GOALS FOR THE CLIENT:
#   

import socket               # Import socket module
import sys
import time
import select
import random
import threading

buffer_size = 4096
delay = 0.0001

class TheClient:
    def __init__(self, port):
        self.client = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        self.client.connect((host, port))
        #s.close                     # Close the socket when done

    def main_loop(self):
        while 1:
            msg = sys.stdin.readline()
            print msg
            #self.client.sendall(msg)
            #print self.client.recv(1024)


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
        self.input_list.remove(self.s)

    def on_recv(self, sockfd):
        data = self.data
        # here we can parse and/or modify the data before send forward
        print data

if __name__ == '__main__':
        server = TheServer('', int((sys.argv)[1]))
        client = TheClient(int((sys.argv)[2]))
        try:
            ts = threading.Thread(target=server.main_loop)
            tc = threading.Thread(target=client.main_loop)
            ts.start()
            tc.start()
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)