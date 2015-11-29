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
import time
from headers import HeaderK, HeaderR, HeaderM
from netaddr import *
from parse import *
from Crypto.PublicKey import RSA

buffer_size = 4096
delay = 0.0001
# ports = {}

class TheClient:
    IP = ''
    lport = 0
    ports = {}

    def __init__(self, port):
        self.client = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        self.IP = socket.gethostbyname(host)
        self.lport = (sys.argv)[1]
        self.key = RSA.generate(2048)
        self.public_key = self.key.publickey()
        print host
        print port
        #print self.public_key.exportKey('PEM')
        self.client.connect((host, port))
        msg = "PORT " + str((sys.argv)[1]) + "\n" + self.public_key.exportKey('PEM')
        print msg
        self.client.sendall(msg) # tell the server what port the Client Server is listening on
        #s.close                     # Close the socket when done

    def main_loop(self):
        while 1:
            msg = sys.stdin.readline()
            self.create_path(msg)
            # print self.client.recv(1024)

    def create_path(self, data):
        indexes = set(range(len(self.ports)))
        path = []
        i = 0

        #find random path of length three from existing clients
        while i < 3:
            if len(indexes) == 0:  # if we are out of nodes
                break
            node = random.choice(tuple(indexes))
            indexes.remove(node)
            if (str(self.ports.values()[node][0]) == str(self.IP)) and (str(self.ports.values()[node][1]) == str(self.lport)): # if node is that of transmitting client
                continue
            path.append(self.ports.values()[node])
            i = i + 1

        print path

        full = HeaderM.add(HeaderM(), str(data))

        while len(path) > 1:
            step = path.pop()
            full = HeaderR.add(HeaderR(), str(step[0]), str(step[1]), str(full))
        step = path.pop()
        self.sender = socket.socket()
        self.sender.connect((step[0], step[1]))
        self.sender.sendall(str(full))
        print str(full)
        self.response = self.sender.recv(buffer_size)
        print str(self.response)
        self.sender.close()
        

class TheServer:
    input_list = []

    def __init__(self, host, port, client):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)
        self.client = client

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
                    # self.on_close()
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
        # global ports
        data = self.data
        # here we can parse and/or modify the data before send forward

        if HeaderR.is_r(HeaderR(), data):
            self.temp_connection(data)
        elif data[0:5] == "PORTS":
            self.client.ports = ast.literal_eval(data[5:])
        elif HeaderM.is_m(HeaderM(), data):
            msg = HeaderM.extract(HeaderM(), data)
            print "FINAL NODE"
            print msg
            self.s.sendall("message received")

        self.on_close()


    def temp_connection(self, data):
        unencrypted_data = self.key.decrypt(data)
        ip, port, msg = HeaderR.extract(HeaderR(), unencrypted_data)
        self.client = socket.socket()         # Create a socket object
        self.client.connect((str(IPAddress(ip)), int(port)))
        self.client.sendall(msg) 
        response = self.client.recv(buffer_size)
        print str(response)
        #self.s.sendall(self.key.encrypt(response))
        self.client.close()                     # Close the socket when done

        

if __name__ == '__main__':
        client = TheClient(int((sys.argv)[2]))
        server = TheServer('', int((sys.argv)[1]), client)
        try:
            ts = threading.Thread(target=server.main_loop)
            ts.daemon = True
            tc = threading.Thread(target=client.main_loop)
            tc.daemon = True
            ts.start()
            tc.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print "Ctrl C - Stopping server"
            sys.exit(1)