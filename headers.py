from parse import *

# Header Message
class HeaderM:
    # returns header containing key + msg
    def add(self, msg):
        return "Message: " + msg

    # returns tuple of key and msg
    def extract(self, msg):
        return parse("Message: {}", msg)

    def is_m(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

# Header Key
class HeaderK:
    # returns header containing key + msg
    def add(self, key, msg):
        return "Key: " + key + "\nMessage: " + msg

    # returns tuple of key and msg
    def extract(self, msg):
        return parse("Key: {}\nMessage: {}", msg)

    def is_k(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

# Header R-something
class HeaderR:
    # returns header containing IP address & port of next hop + msg
    def add(self, ip, port, msg):
        return "IP: " + ip + "\nPort: " + port + "\nMessage: " + msg

    # returns tuple of IP, port, and msg
    def extract(self, msg):
        return parse("IP: {}\nPort: {}\nMessage: {}", msg)

    def is_r(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

# Header Forward
class HeaderF:
    # returns header containing key + msg
    def add(self, nonce, port, ip):
        return "Nonce: " + nonce + "\nPort: " + port + "\nIP: " + ip

    # returns tuple of key and msg
    def extract(self, msg):
        return parse("Nonce: {}\nPort: {}\nIP: {}", msg)

    def is_f(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

class HeaderE:
    # returns header containing key + msg
    def add(self, enc, nonce):
        return "Enc: " + enc + "\nNonce: " + nonce

    # returns tuple of key and msg
    def extract(self, msg):
        return parse("Enc: {}\nNonce: {}", msg)

    def is_e(self, msg):
        if self.extract(msg):
            return True
        else:
            return False

class HeaderN:
    # returns header containing key + msg
    def add(self, nonce):
        return "Nonce: " + nonce

    # returns tuple of key and msg
    def extract(self, msg):
        return parse("Nonce: {}", msg)

    def is_n(self, msg):
        if self.extract(msg):
            return True
        else:
            return False