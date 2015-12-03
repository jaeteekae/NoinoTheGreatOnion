from parse import *

# Header Message
class HeaderM:
    # returns header containing key + msg
    @staticmethod
    def add(msg):
        return "Message: " + msg

    # returns tuple of key and msg
    @staticmethod
    def extract(msg):
        return parse("Message: {}", msg)

    @staticmethod
    def is_m(msg):
        if HeaderM.extract(msg):
            return True
        else:
            return False

# Header Key
class HeaderK:
    # returns header containing key + msg
    @staticmethod
    def add(key, msg):
        return "Key: " + key + "\nMessage: " + msg

    # returns tuple of key and msg
    @staticmethod
    def extract(msg):
        return parse("Key: {}\nMessage: {}", msg)

    @staticmethod
    def is_k(msg):
        if HeaderK.extract(msg):
            return True
        else:
            return False

# Header R-something
class HeaderR:
    # returns header containing IP address & port of next hop + msg
    @staticmethod
    def add(ip, port, msg):
        return "IP: " + ip + "\nPort: " + port + "\nMessage: " + msg

    # returns tuple of IP, port, and msg
    @staticmethod
    def extract(msg):
        return parse("IP: {}\nPort: {}\nMessage: {}", msg)

    @staticmethod
    def is_r(msg):
        if HeaderR.extract(msg):
            return True
        else:
            return False

# Header Forward: tells a node where to forward the nonce-message
class HeaderF:
    # returns header containing key + msg
    @staticmethod
    def add(nonce, port, ip):
        return "Nonce: " + nonce + "\nPort: " + port + "\nIP: " + ip

    # returns tuple of key and msg
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
class HeaderE:
    # returns header containing key + msg
    @staticmethod
    def add(enc, nonce, pk1, pk2):
        return "Enc: " + enc + "\nNonce: " + nonce + "\nPK1: " + pk1 + "\nPK2: " + pk2

    # returns tuple of key and msg
    @staticmethod
    def extract(msg):
        return parse("Enc: {}\nNonce: {}\nPK1: {}\nPK2: {}", msg)

    @staticmethod
    def is_e(msg):
        if HeaderE.extract(msg):
            return True
        else:
            return False

# Header Nonce: for querying the server for an unused nonce
class HeaderN:
    # returns header containing key + msg
    @staticmethod
    def add(nonce):
        return "Nonce: " + nonce

    # returns tuple of key and msg
    @staticmethod
    def extract(msg):
        return parse("Nonce: {}", msg)

    @staticmethod
    def is_n(msg):
        if HeaderN.extract(msg):
            return True
        else:
            return False