#!/usr/bin/env python3
import sys

NULL_CHAR = chr(0)

keys = {
    "UP": chr(66) + NULL_CHAR,
    "DOWN": chr(67)+NULL_CHAR,
    "LEFT": chr(68)+NULL_CHAR,
    "RIGHT": chr(69)+NULL_CHAR,
    "SELECT": chr(65)+NULL_CHAR,
    "HOME": chr(35)+chr(2),
    "BACK": chr(36)+chr(2),
    "PLAY": chr(205)+NULL_CHAR,
    "MUTE": chr(226)+NULL_CHAR,
}


def print_usage():
  print("Usage: ", sys.argv[0], " ", '|'.join(keys.keys()))
  sys.exit(-1)

def send_key(fd, key):
    fd.write(key.encode())

def press_key(key):
    with open('/dev/hidg0', 'rb+') as fd:
      key_down(key, fd)
      key_release(fd)

def key_down(key, fd):
    key = keys.get(key, None)
    if key is not None:
        send_key(fd, key)
    else:
        print_usage()

def key_release(fd):
    send_key(fd, NULL_CHAR * 2)


if len(sys.argv) != 2:
    print_usage()

press_key(sys.argv[1])
