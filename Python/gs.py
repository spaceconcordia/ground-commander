#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Shawn <shawn dot bulger at spaceconcordia dot ca>
#
# Distributed under terms of the MIT license.

"""
This is a command-line interface to run the ground station interactively
start   - on   - s : start the ground station for normal operation
mock    - mk   - m : start the mock satellite interaction locally (no radio)
exit    - quit - q : close the program
help    - menu - h : show this menu
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

GS_RUNNING      = False
GS_BIN_PATH = "/home/apps/gs";
GS_PATH = {
    "LOG"            : '/home/logs/gs.log',
    "INPUT_PIPE"     : '/home/pipes/gnd-input',
    "NETMAN"         : GS_BIN_PATH+'gnd',
    "DECODE_RB"      : GS_BIN_PATH+'decode-command.rb',
    "GETLOG_RB"      : GS_BIN_PATH+'getlog-command.rb',
    "GETTIME_RB"     : GS_BIN_PATH+'gettime-command.rb',
    "REBOOT_RB"      : GS_BIN_PATH+'reboot-command.rb',
    "UPDATE_RB"      : GS_BIN_PATH+'update-command.rb',
    "STEP2_RB"       : GS_BIN_PATH+'step2.rb'
}

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

def fail(error):
    print "\r\nFailed: "+error+" Aborting..."
    sys.exit(1)

def exit(exit_message):
    print "\r\nExiting: "+exit_message
    sys.exit(0)

def signal_handler(signal, frame):
  print '\r\nCaught Cntl+C!'
signal.signal(signal.SIGINT, signal_handler)

def check_requirements():
    for requirement in GS_PATH:
        if ( os.path.isfile(requirement) ):
            continue
        else : fail(requirement+" is not present!")
            
def start_ground_station():
  # start ground-netman
  ground_netman = subP(GS_NETMAN);
  print ground_netman.communicate()

  # test local radio

  # ping satellite

  # start ground-commmander and drop to shell
  start_ground_commander()
#end def

def start_mock_interaction():
  mock_satellite = subP(GS_NETMAN);
  print ground_commander.communicate()

def start_ground_commander(): 
  ground_commander = subprocess.Popen(['python', 'ground-commander.py'], shell=False, stdout=subprocess.PIPE)
  print ground_commander.communicate()

def command_line_interface():
  print 'Enter commands for the ground station below.\r\nType "menu" for predefined commands, and "exit" to quit'
  input=1
  while 1:
    gs_running_led = "GO >> " if GS_RUNNING else "NOGO >> "
    input=raw_input( gs_running_led + time.strftime("%H:%M:%S") + " >> " )
    if ((input == "exit") | (input == "q")):
      exit()    
    if ((input == "menu") | (input == "help") | (input == "h")):
      usage()
    if ((input == "start") | (input == "on") | (input == "s")):
      start_ground_station()
    if ((input == "mock") | (input == "mk") | (input == "m")):
      start_mock_interaction()

def main():
    # TODO not working #location = whereis('echo')
    #if location is not None:
    #    print location
    #subShell(['echo', 'hello space'])
    #process = subprocess.Popen(['echo', 'Hello World!'], shell=False, stdout=subprocess.PIPE)
    #print process.communicate()
    usage()
    check_requirements()
    command_line_interface()

    # off

    # exit()

if __name__ == '__main__':
    main()
