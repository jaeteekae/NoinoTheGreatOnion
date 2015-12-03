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
from headers import *
from netaddr import *
from parse import *
from Crypto.PublicKey import RSA

buffer_size = 4096
delay = 0.0001
key = RSA.generate(2048)
public_key = key.publickey()

class TheClient:
    IP = ''
    lport = 0
    ports = {}
    host = 0
    port = 0

    def __init__(self, port):
        self.client = socket.socket()         # Create a socket object
        self.host = socket.gethostname() # Get local machine name
        self.IP = socket.gethostbyname(self.host)
        self.lport = (sys.argv)[1]
        self.port = port
        print self.host
        print self.port
        #print "---EXPORTED KEY---\n", self.public_key.exportKey('PEM')
        self.client.connect((self.host, self.port))
        # print "PUBLIC KEY: ",public_key.exportKey('PEM')
        msg = "PORT " + str((sys.argv)[1]) + "\n" + public_key.exportKey('PEM')
        #print msg
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
                # my_key = RSA.importKey(self.ports.values()[node][2])
                # enc_data = my_key.encrypt('abcdefgh', 32)
                # print "ENC : "
                # print enc_data
                # print "DECRYPTED : " + key.decrypt(enc_data)
                continue
            path.append(self.ports.values()[node])
            i = i + 1
        self.send_msg(data, path)


    def send_msg(self, data, path):
        msg = HeaderN.add("-1")
        self.response = self.temp_connection_with_response(self.host, self.port, msg)
        nonce = HeaderN.extract(self.response)[0]
        print nonce
        # enc_msg = HeaderE.add(HeaderE(), str(data) +)


            # print str(full)
            # step = path.pop()
            #print "----STEP 2----\n", step[2]
            # tmp_key = RSA.importKey(step[2])
            # print "TMP_KEY: ",step[2]
            # msg = tmp_key.encrypt(str(full), 32)
            # full = HeaderR.add(HeaderR(), str(step[0]), str(step[1]), msg[0])

        # print str(full)
        n1 = path[0]
        n2 = path[1]
        n3 = path[2]
        n1_key = RSA.importKey(n1[2])
        n2_key = RSA.importKey(n2[2])
        n3_key = RSA.importKey(n3[2])

        m1to2 = n1_key.encrypt(HeaderF.add(nonce, str(n2[1]), str(n2[0])), 32)[0]
        m2to3 = n2_key.encrypt(HeaderF.add(nonce, str(n3[1]), str(n3[0])), 32)[0]
        enc_msg = n3_key.encrypt(HeaderM.add(data), 32)[0]
        enc_key = n3_key.encrypt(public_key.exportKey('PEM'), 32)[0]
        enc_msg = n2_key.encrypt(enc_msg, 32)[0]
        enc_msg = n1_key.encrypt(enc_msg, 32)[0]
        enc_msg = HeaderE.add(enc_msg, nonce, enc_key)



        # tmp_key = RSA.importKey(step[2])
        # print "TMP_KEY: ",step[2]
        # msg = tmp_key.encrypt(str(full), 32)

        self.temp_connection_no_response(n2[0], n2[1], str(m2to3))
        self.temp_connection_no_response(n1[0], n1[1], str(m1to2))
        self.response = self.temp_connection_with_response(n1[0], n1[1], str(enc_msg))
        self.response = key.decrypt((self.response,))
        self.response = key.decrypt((self.response,))
        self.response = key.decrypt((self.response,))
        print str(self.response)
        self.temp_connection_no_response(self.host, self.port, HeaderN.add(nonce))
        
    def temp_connection_no_response(self, ip, port, msg):
        self.sender = socket.socket()    
        self.sender.connect((ip, port))
        self.sender.sendall(msg)
        self.sender.close()

    def temp_connection_with_response(self, ip, port, msg):
        self.sender = socket.socket()    
        self.sender.connect((ip, port))
        self.sender.sendall(msg)
        response = self.sender.recv(buffer_size)
        self.sender.close()
        return response

class TheServer:
    input_list = []
    ftable = {} # forwarding table: [nonce]=(ip, port)
    msgbuffer = {} # buffer for HeaderE messages: [nonce]=(encoded_msg, public_key)

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
            # if there are old messages in the buffer to send, send them
            self.forward_nonces()
            # accept new connections
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
        #print "ENC DATA:\n", self.data
        data = self.data
        # print "DATA: \n", data
        #TODO: DECRYPT HERE
        # here we can parse and/or modify the data before send forward
        if data[0:5] == "PORTS":
            self.client.ports = ast.literal_eval(data[5:])
        else:
            # print "ENC DATA:\n", self.data
            # data = key.decrypt(self.data)
            print "DATA: \n", data
            if HeaderE.is_e(data):
                encoded_msg, nonce, encoded_key = HeaderE.extract(data)
                decoded_msg = key.decrypt((encoded_msg,))
                decoded_key = key.decrypt((encoded_key,))
                if HeaderM.is_m(decoded_msg):
                    msg = HeaderM.extract(decoded_msg)[0]
                    print "FINAL NODE"
                    print msg
                    response = "message received"
                    pk = RSA.importKey(decoded_key)
                    encoded_response = pk.encrypt(response, 32)[0]
                    self.s.sendall(encoded_response)
                    #self.s.sendall("message received")
                else:
                    # add partially decoded message & key to the buffer table
                    self.msgbuffer[nonce] = (decoded_msg, decoded_key)
            else:
                decoded_msg = key.decrypt((data,))
                if HeaderF.is_f(decoded_msg):
                    # add nonce to the forwarding table
                    nonce, port, ip = HeaderF.extract(decoded_msg)
                    self.ftable[nonce] = (ip, port)
            

        self.on_close()

    def forward_nonces(self):
        # print "MSGBUFFER:\n", self.msgbuffer
        # print "FTABLE:\n", self.ftable
        sent = []
        for nonce in self.msgbuffer:
            if self.ftable[nonce]:
                # forward the message
                encoded_msg, encoded_key = self.msgbuffer[nonce]
                ip, port = self.ftable[nonce]
                msg_and_h = HeaderE.add(encoded_msg, nonce, encoded_key)
                self.temp_connection(ip, port, msg_and_h)
                # delete the entries for nonce in the tables
                sent.append(nonce)
        for nonce in sent:
            del self.msgbuffer[nonce]
            del self.ftable[nonce]

    def temp_connection(self, ip, port, msg):
        self.client = socket.socket()         # Create a socket object
        self.client.connect((str(IPAddress(ip)), int(port)))
        self.client.sendall(msg) 
        response = self.client.recv(buffer_size)
        #encoded_response = key.encrypt(response, 32)[0]
        #print str(response)
        self.s.sendall(response)
        self.s.sendall(encoded_response)
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