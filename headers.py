from parse import *

# Header Message: base header containing only the main message
class HeaderM:
    # returns msg wrapped with a HeaderM
    @staticmethod
    def add(msg):
        return "Message: " + msg

    # returns tuple of msg
    @staticmethod
    def extract(msg):
        return parse("Message: {}", msg)

    # returns true if msg is a HeaderM
    @staticmethod
    def is_m(msg):
        if HeaderM.extract(msg):
            return True
        else:
            return False

# Header Forward: tells a node where to forward the message that uses the specified nonce
class HeaderF:
    @staticmethod
    def add(nonce, port, ip):
        return "Nonce: " + nonce + "\nPort: " + port + "\nIP: " + ip

    @staticmethod
    def extract(msg):
        return parse("Nonce: {}\nPort: {}\nIP: {}", msg)

    @staticmethod
    def is_f(msg):
        if HeaderF.extract(msg):
            return True
        else:
            return False

# Header Encrypted (x3) Message + Nonce 
#        + the Encrypted (x3) Public Key of the sender (split into 2 parts)
class HeaderE:
    @staticmethod
    def add(enc, nonce, pk1, pk2):
        return r"Enc: " + enc + "\nNonce: " + nonce + "\nPK1: " + pk1 + "\nPK2: " + pk2

    @staticmethod
    def extract(msg):
        return parse("Enc: {}\nNonce: {}\nPK1: {}\nPK2: {}", msg)

    @staticmethod
    def is_e(msg):
        if HeaderE.extract(msg):
            return True
        else:
            return False

# Header Nonce: for querying the server with nonce-related requests
class HeaderN:
    @staticmethod
    def add(nonce):
        return "Nonce: " + nonce

    @staticmethod
    def extract(msg):
        return parse("Nonce: {}", msg)

    @staticmethod
    def is_n(msg):
        if HeaderN.extract(msg):
            return True
        else:
            return False

# Header Port: for sending the server the listening port and the public key
class HeaderP:
    @staticmethod
    def add(port, key):
        return "Port: " + port + "\nKey: " + key

    @staticmethod
    def extract(msg):
        return parse("Port: {}\nKey: {}", msg)

    @staticmethod
    def is_p(msg):
        if HeaderP.extract(msg):
            return True
        else:
            return False

# Header Port Broadcast: for broadcasting list of ports
class HeaderPB:
    @staticmethod
    def add(ports):
        return "Ports: " + ports

    @staticmethod
    def extract(msg):
        return parse("Ports: {}", msg)

    @staticmethod
    def is_pb(msg):
        if HeaderPB.extract(msg):
            return True
        else:
            return False
