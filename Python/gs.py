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
import os
import subprocess
import time
import sys

try:
    raw_input
except NameError:
    raw_input = input

GS_BIN_DIR      = '/usr/bin/'
GS_LOG_FILE     = '/var/log/gs.log'
GS_INPUT_PIPE   = '/home/pipes/gnd-input'
GS_NETMAN_PATH  = GS_BIN_DIR+'gnd'
GS_DECODE_RB    = GS_BIN_DIR+'decode-command.rb' 
GS_GETLOG_RB    = GS_BIN_DIR+'getlog-command.rb' 
GS_GETTIME_RB   = GS_BIN_DIR+'gettime-command.rb'
GS_REBOOT_RB    = GS_BIN_DIR+'reboot-command.rb'
GS_UPDATE_RB    = GS_BIN_DIR+'update-command.rb'
GS_STEP2_RB     = GS_BIN_DIR+'step2.rb'

KW_GETTIME  = "010001313337"    #0x01 0x00 0x01 0x31 0x33 0x37
KW_CONFIRM  = "02000121242b"    #0x02 0x00 0x01 0x21 0x24 0x2b
KW_ACK      = "31210052d5"      #0x31 0x21 0x00 0x52 0xd5

def subCustom(args):
    subprocess.Popen(args,bufsize=0,executable=None,stdin=None,stdout=None,stderr=None,preexec_fn=None,close_fds=False,shell=False,cwd=None,universal_newlines=False,startupinfo=None,creationflags=0,evn=None
    )

def subP(args):
    subprocess.Popen(args,shell=False,stdout=subprocess.PIPE)

def subShell(args):
    subprocess.Popen(args,shell=True,executable="/bin/bash")

def whereis(program):
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and \
            not os.path.isdir(os.path.join(path, program)):
                return os.path.join(path, program)
    return None

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
    # TODO not working #location = whereis('echo')
    #if location is not None:
    #    print location
    subShell(['echo', 'hello space'])
    process = subprocess.Popen(['echo', 'Hello World!'], shell=False, stdout=subprocess.PIPE)
    print process.communicate()
    usage()
    command_line_interface()
    # exit()

if __name__ == '__main__':
    main()
