from parse import *

class HeaderK:
    # returns msg + header containing key
    def add(self, msg, key):
        return "Key: " + key + "\nMessage: " + msg

    # returns tuple of key and msg
    def extract(self, msg):
        return parse("Key: {}\nMessage: {}", msg)