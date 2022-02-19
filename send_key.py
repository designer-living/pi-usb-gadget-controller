#!/usr/bin/env python3
import sys

#NULL_CHAR = chr(0)
NULL_CHAR = bytes((0,))


#keysold = {
#    "UP": chr(66) + NULL_CHAR,
#    "DOWN": chr(67)+NULL_CHAR,
#    "LEFT": chr(68)+NULL_CHAR,
#    "RIGHT": chr(69)+NULL_CHAR,
#    "SELECT": chr(65)+NULL_CHAR,
#    "HOME": chr(35)+chr(2),
#    "BACK": chr(36)+chr(2),
#    "PLAY": chr(205)+NULL_CHAR,
#    "MUTE": chr(226)+NULL_CHAR,
#}
keys = {
    "UP": bytes((66,)) + NULL_CHAR,
    "DOWN": bytes((67,))+NULL_CHAR,
    "LEFT": bytes((68,))+NULL_CHAR,
    "RIGHT": bytes((69,))+NULL_CHAR,
    "SELECT": bytes((65,))+NULL_CHAR,
    "HOME": bytes((35,))+bytes((2,)),
    "BACK": bytes((36,))+bytes((2,)),
    "PLAY": bytes((205,))+NULL_CHAR,
    "MUTE": bytes((226,))+NULL_CHAR,
    "MIC": bytes((207,))+NULL_CHAR,
}


def print_usage():
  print("Usage: ", sys.argv[0], " ", '|'.join(keys.keys()))
  sys.exit(-1)

def send_key(fd, key):
    fd.write(key)
#    fd.write(key.encode())

def send_key2(fd, key):
    fd.write(key)

def press_key(key):
    with open('/dev/hidg0', 'rb+') as fd:
      key_down(key, fd)
      key_release(fd)

def key_down(key, fd):
    key_code = keys.get(key, None)
    print("Sending: ", key, " code: ", key_code)
    if key_code is not None:
        send_key(fd, key_code)
#        key_code = b"0xe20x00"
#        send_key2(fd, key_code)
    else:
        print_usage()

def key_release(fd):
    send_key(fd, NULL_CHAR * 2)


if len(sys.argv) != 2:
    print_usage()

press_key(sys.argv[1])
print("Done")
