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
import requests
from headers import *
from netaddr import *
from parse import *
from Crypto.PublicKey import RSA

buffer_size = 8192
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
        self.IP = (sys.argv)[3]
        self.lport = (sys.argv)[1]
        self.port = port

        try:
            self.client.connect((self.IP, self.port)) ##### CHANGE
        except socket.error:
            print "Cannot connect to server"
            sys.exit()

        msg = HeaderP.add(str((sys.argv)[1]), public_key.exportKey('PEM'))

        try:
            self.client.sendall(msg) # tell the server what port the Client Server is listening on
        except socket.error:
            print "Server has disconnected"
            sys.exit()

    def main_loop(self):
        while 1:
            msg = sys.stdin.readline()
            self.create_path(msg)

    # select a transmission path from all connected clients, then send data on path
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
        self.send_msg(data, path)


    # given data and a three node path, send the data along that path with encryption
    def send_msg(self, data, path):
        if len(path) < 3:
            print "Not enough clients connected; cannot send message for security purposes"
        else:
            # send HeaderN with -1 to indicate need for new nonce
            msg = HeaderN.add("-1")
            #### CHANGE
            self.response = self.temp_connection_with_response(self.IP, self.port, msg)
            nonce = HeaderN.extract(self.response)[0]

            n1 = path[0]
            n2 = path[1]
            n3 = path[2]
            n1_key = RSA.importKey(n1[2])
            n2_key = RSA.importKey(n2[2])
            n3_key = RSA.importKey(n3[2])
            exp_key = public_key.exportKey('PEM')
            half1, half2 = exp_key[:len(exp_key)/2], exp_key[len(exp_key)/2:]

            # do all of the encryption before sending
            m1to2 = n1_key.encrypt(HeaderF.add(nonce, str(n2[1]), str(n2[0])), 32)[0]
            m2to3 = n2_key.encrypt(HeaderF.add(nonce, str(n3[1]), str(n3[0])), 32)[0]
            enc_msg = n3_key.encrypt(HeaderM.add(data), 32)[0]
            enc_key1 = n3_key.encrypt(half1, 32)[0]
            enc_key2 = n3_key.encrypt(half2, 32)[0]
            enc_msg = n2_key.encrypt(enc_msg, 32)[0]
            enc_key1 = n2_key.encrypt(enc_key1, 32)[0]
            enc_key2 = n2_key.encrypt(enc_key2, 32)[0]
            enc_msg = n1_key.encrypt(enc_msg, 32)[0]
            enc_key1 = n1_key.encrypt(enc_key1, 32)[0]
            enc_key2 = n1_key.encrypt(enc_key2, 32)[0]
            enc_msg = HeaderE.add(enc_msg, nonce, enc_key1, enc_key2)

            # send all three messages
            self.temp_connection_no_response(n2[0], n2[1], str(m2to3))
            self.temp_connection_no_response(n1[0], n1[1], str(m1to2))
            self.response = self.temp_connection_with_response(n1[0], n1[1], str(enc_msg))
            #self.response = key.decrypt((self.response,))
            print self.decode_response()
            self.temp_connection_no_response(self.IP, self.port, HeaderN.add(nonce))

    def decode_response(self):
        try:
            resl = ast.literal_eval(str(self.response))
        except:
            return "Timeout: data unable to be entirely recovered."
        dec = []
        for x in resl:
            dec.append(key.decrypt((x,)))
        response = "".join(dec)
        return response.decode('unicode-escape')
        
    # establish temporary connection to send message to server at (ip, port)
    def temp_connection_no_response(self, ip, port, msg):
        self.sender = socket.socket()  
        try:  
            self.sender.connect((ip, port))
            self.sender.sendall(msg)
        except socket.error:
            print "An essential node has disconnected. Cannot send message."
            sys.exit()
        self.sender.close()

    # establish temporary connection to send and receive a message from server at (ip, port)
    def temp_connection_with_response(self, ip, port, msg):
        timeout = 4
        self.sender = socket.socket()    
        try:  
            self.sender.connect((ip, port))
            self.sender.sendall(msg)
        except socket.error:
            print "An essential node has disconnected. Cannot send message."
            sys.exit()

        # source: http://www.binarytides.com/receive-full-data-with-the-recv-socket-function-in-python/
        self.sender.setblocking(0)
        total_data=[]
        data = ''

        begin = time.time()
        while 1:
            if total_data and time.time()-begin > timeout:
                break
            elif time.time()-begin > timeout*2:
                break
            try:
                data = self.sender.recv(buffer_size)
                if data:
                    total_data.append(data)
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass
        return ''.join(total_data)

class TheServer:
    input_list = [] # for keeping track of connections
    ftable = {}     # forwarding table: [nonce]=(ip, port)
    msgbuffer = {}  # buffer for HeaderE messages: [nonce]=(encoded_msg, pk1, pk2)

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
        self.input_list.append(clientsock)

    def on_close(self):
        self.input_list.remove(self.s)

    def on_recv(self, sockfd):
        data = self.data
        # PORT message: add the new client
        if HeaderPB.is_pb(data):
            str_ports = HeaderPB.extract(data)[0]
            self.client.ports = ast.literal_eval(str_ports)
        # HeaderE message: decrypt one layer off the message
        elif HeaderE.is_e(data):
            encoded_msg, nonce, encoded_key1, encoded_key2 = HeaderE.extract(data)
            decoded_msg = key.decrypt((encoded_msg,))
            decoded_key1 = key.decrypt((encoded_key1,))
            decoded_key2 = key.decrypt((encoded_key2,))

            # HeaderM message: this node is the last in the path
            if HeaderM.is_m(decoded_msg):
                msg = HeaderM.extract(decoded_msg)[0]
                response = self.http_response(msg)
                pk = RSA.importKey(decoded_key1 + decoded_key2)
                encoded_response = self.split_response(response, pk)
                self.s.sendall(encoded_response)
            else:
                # add partially decoded message & key to the buffer table
                self.msgbuffer[nonce] = (decoded_msg, decoded_key1, decoded_key2)
        else:
            # HeaderF message: keep track of where to forward nonce for future use
            decoded_msg = key.decrypt((data,))
            if HeaderF.is_f(decoded_msg):
                # add nonce to the forwarding table
                nonce, port, ip = HeaderF.extract(decoded_msg)
                self.ftable[nonce] = (ip, port)
        self.on_close()

    def forward_nonces(self):
        sent = []
        # forward all messages with forwarding information
        for nonce in self.msgbuffer:
            if nonce in self.ftable:
                encoded_msg, encoded_key1, encoded_key2 = self.msgbuffer[nonce]
                ip, port = self.ftable[nonce]
                msg_and_h = HeaderE.add(encoded_msg, nonce, encoded_key1, encoded_key2)
                self.temp_connection(ip, port, msg_and_h)
                sent.append(nonce)
        # delete the entries for sent nonces in the tables
        for nonce in sent:
            del self.msgbuffer[nonce]
            del self.ftable[nonce]

    def temp_connection(self, ip, port, msg):
        # send msg forward
        self.client = socket.socket()         # Create a socket object
        self.client.connect((str(IPAddress(ip)), int(port)))
        self.client.sendall(msg) 

        # return the response on the same socket
        response = self.client.recv(buffer_size)
        self.s.sendall(response)
        self.client.close()                     # Close the socket when done

    def http_response(self, req):
        r = requests.get(req)
        return r.text

    def split_response(self, text, pk):
        chunks, chunk_size = len(text), 250
        split_plain = [ str(text)[i:i+chunk_size] for i in range (0, chunks, chunk_size) ]
        split_enc = []
        for x in split_plain:
            split_enc.append(pk.encrypt(x, 32)[0])
        return str(split_enc)



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