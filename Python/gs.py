#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Shawn <shawn dot bulger at spaceconcordia dot ca>
#
# Distributed under terms of the MIT license.

"""
This is a command-line interface to run the ground station interactively
exit - quit - q : close the program
help - menu - h : show this menu
"""

#import pexpect
import signal
import time
import sys

try:
    raw_input
except NameError:
    raw_input = input

GS_LOG_FILE = '/var/log/gs.log'

def usage():
    print(globals()['__doc__'])

def fail():
    sys.exit(1)

def exit():
    sys.exit(0)

def signal_handler(signal, frame):
  print '\r\nCaught Cntl+C!'
signal.signal(signal.SIGINT, signal_handler)

def command_line_interface():
  print 'Enter commands for the ground station below.\r\nType "menu" for predefined commands, and "exit" to quit'
  input=1
  while 1:
    input=raw_input( time.strftime("%H:%M:%S") + " >> " )
    if ((input == "exit") | (input == "q")):
      exit()    
    if ((input == "menu") | (input == "help") | (input == "h")):
      usage()

def main():
    usage()
    command_line_interface()
    # exit()

if __name__ == '__main__':
    main()
