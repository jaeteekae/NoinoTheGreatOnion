from parse import *


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