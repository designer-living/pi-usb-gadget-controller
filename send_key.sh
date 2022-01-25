#!/bin/bash

USAGE="Usage : $0 [HOME|SELECT|UP|DOWN|LEFT|RIGHT|PLAY|MUTE]"
if [ $# -lt 1 ]
then
        echo ${USAGE}
        exit
fi

DEVICE=/dev/hidg0

case "$1" in

HOME)  echo -ne "\x23\x02" > ${DEVICE}
    ;;
SELECT)  echo  -ne "\x41\x00" > /dev/hidg0
    ;;
UP)  echo  -ne "\x42\x00" > /dev/hidg0
    ;;
DOWN)  echo  -ne "\x43\x00" > /dev/hidg0
   ;;
LEFT)  echo  -ne "\x44\x00" > /dev/hidg0
   ;;
RIGHT)  echo  -ne "\x45\x00" > /dev/hidg0
   ;;
PLAY)  echo  -ne "\xcd\x00" > /dev/hidg0
   ;;
MUTE)  echo  -ne "\xe2\x00" > /dev/hidg0
   ;;
*) echo "Invalid command $1"
   echo ${USAGE}
   exit
   ;;
esac
echo -ne "\0\0" > /dev/hidg0
