from parse import *

# Header Message
class HeaderM:
    # returns header containing key + msg
    @staticmethod
    def add(msg):
        return "Message: " + msg

    # returns tuple of key and msg
    @staticmethod
    def extract(self, msg):
        return parse("Message: {}", msg)

    @staticmethod
    def is_m(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

# Header Key
class HeaderK:
    # returns header containing key + msg
    @staticmethod
    def add(self, key, msg):
        return "Key: " + key + "\nMessage: " + msg

    # returns tuple of key and msg
    @staticmethod
    def extract(self, msg):
        return parse("Key: {}\nMessage: {}", msg)

    @staticmethod
    def is_k(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

# Header R-something
class HeaderR:
    # returns header containing IP address & port of next hop + msg
    @staticmethod
    def add(self, ip, port, msg):
        return "IP: " + ip + "\nPort: " + port + "\nMessage: " + msg

    # returns tuple of IP, port, and msg
    @staticmethod
    def extract(self, msg):
        return parse("IP: {}\nPort: {}\nMessage: {}", msg)

    @staticmethod
    def is_r(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

# Header Forward: tells a node where to forward the nonce-message
class HeaderF:
    # returns header containing key + msg
    @staticmethod
    def add(self, nonce, port, ip):
        return "Nonce: " + nonce + "\nPort: " + port + "\nIP: " + ip

    # returns tuple of key and msg
    @staticmethod
    def extract(self, msg):
        return parse("Nonce: {}\nPort: {}\nIP: {}", msg)

    @staticmethod
    def is_f(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

# Header Encrypted (x3) Message + Nonce
class HeaderE:
    # returns header containing key + msg
    @staticmethod
    def add(self, enc, nonce):
        return "Enc: " + enc + "\nNonce: " + nonce

    # returns tuple of key and msg
    @staticmethod
    def extract(self, msg):
        return parse("Enc: {}\nNonce: {}", msg)

    @staticmethod
    def is_e(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

# Header Nonce: for querying the server for an unused nonce
class HeaderN:
    # returns header containing key + msg
    @staticmethod
    def add(self, nonce):
        return "Nonce: " + nonce

    # returns tuple of key and msg
    @staticmethod
    def extract(self, msg):
        return parse("Nonce: {}", msg)

    @staticmethod
    def is_n(self, msg):
        if self.extract(msg):
            return True
        else:
            return False