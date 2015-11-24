#!/usr/bin/python           # This is client.py file

# GOALS FOR THE CLIENT:
#   

import socket               # Import socket module
import sys
import time
import select
import random
import threading
import ast
from headers import HeaderK, HeaderR
from netaddr import *
from parse import *

buffer_size = 4096
delay = 0.0001
ports = {}

class TheClient:
    IP = ''
    lport = 0

    def __init__(self, port):
        self.client = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        self.IP = socket.gethostbyname(host)
        self.lport = (sys.argv)[1]
        print host
        print port
        self.client.connect((host, port))
        self.client.sendall("PORT " + str((sys.argv)[1])) # tell the server what port the Client Server is listening on
        #s.close                     # Close the socket when done

    def main_loop(self):
        while 1:
            msg = sys.stdin.readline()
            #print msg
            self.create_path(msg)
            print self.client.recv(1024)

    def create_path(self, data):
        indexes = set(range(len(ports)))
        path = []
        i = 0

        #find random path of length three from existing clients
        while i < 3:
            if len(indexes) == 0:  # if we are out of nodes
                break
            node = random.choice(tuple(indexes))
            indexes.remove(node)
            print "From list: " + ports.values()[node][0] + "   Stored: " + self.IP
            print "From list: " + str(ports.values()[node][1]) + "   Stored: " + str(self.lport)
            if (str(ports.values()[node][0]) == str(self.IP)) and (str(ports.values()[node][1]) == str(self.lport)): # if node is that of transmitting client
                continue
            path.append(ports.values()[node])
            i = i + 1

        print path

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

class TheServer:
    input_list = []

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
        global ports
        data = self.data
        # here we can parse and/or modify the data before send forward
        if HeaderK.is_k(HeaderK(), data):
            key, msg = HeaderK.extract(HeaderK(), data)
            print "FINAL NODE"
            print msg
        elif HeaderR.is_r(HeaderR(), data):
            self.temp_connection(data)
        elif data[0:5] == "PORTS":
            ports = ast.literal_eval(data[5:])



    def temp_connection(self, data):
        ip, port, msg = HeaderR.extract(HeaderR(), data)
        self.client = socket.socket()         # Create a socket object
        self.client.connect((str(IPAddress(ip)), int(port)))
        self.client.sendall(msg) 
        self.client.close()                     # Close the socket when done
        

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