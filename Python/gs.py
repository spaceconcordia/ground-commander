#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Shawn <shawn dot bulger at spaceconcordia dot ca>
#
# Distributed under terms of the MIT license.

"""
This is a command-line interface to run the ground station interactively
start       - on   - s : start the ground station for normal operation
mock        - mk   - m : start the mock satellite interaction locally (no radio)
teardown    - td   - t : terminate all running ground station or mock satellite processes
exit        - quit - q : close the program
help        - menu - h : show this menu
"""

#import pexpect
import signal
import os
import stat
import subprocess
import time
import sys
import datetime # to return the current ISO date for selecting log files


try:
    raw_input
except NameError:
    raw_input = input

#-------------------------------------------------------------
# GLOBALS 
#-------------------------------------------------------------
iso_today = datetime.datetime.now().strftime("%Y%m%d")
ground_control = None
log_window = None

GS_BIN_PATH = "/usr/bin/"
GS_PATH = {
    "LOG"               : "/home/logs/gs.log",
    "INPUT_PIPE"        : "/home/pipes/gnd-input",
    "GROUND_NETMAN"     : GS_BIN_PATH+"gnd",
    "GROUND_COMMANDER"  : GS_BIN_PATH+"ground-commander",
    "MOCK_SAT_NM"       : GS_BIN_PATH+"mock_sat",
    "MOCK_SAT_CMDR"     : GS_BIN_PATH+"space-commander",
    "DECODE_RB"         : GS_BIN_PATH+"decode-command.rb",
    "GETLOG_RB"         : GS_BIN_PATH+"getlog-command.rb",
    "GETTIME_RB"        : GS_BIN_PATH+"gettime-command.rb",
    "REBOOT_RB"         : GS_BIN_PATH+"reboot-command.rb",
    "UPDATE_RB"         : GS_BIN_PATH+"update-command.rb",
    "STEP2_RB"          : GS_BIN_PATH+"step2.rb",
    "PCD"               : "/usr/sbin/pcd"
}

PCD_RULESET_PATH = "/home/vagrant/CONSAT1/space-pcd/pcd-1.1.6/rules/"
PCD_RULESET_EXT = ".pcd"
PCD_RULESET_LIST = {
    "GROUND_STATION"        : PCD_RULESET_PATH+"ground-station"+PCD_RULESET_EXT,
    "MOCK_SAT_INTERACTION"  : PCD_RULESET_PATH+"mock-satellite-interaction"+PCD_RULESET_EXT,
    "SATELLITE"             : PCD_RULESET_PATH+"satellite"+PCD_RULESET_EXT
}

GS_LOG_PATH = "/home/logs/"
GS_LOG_EXT = ".log"
SAT_LOG_FILES = {
    "MOCK_SAT_NM"       : GS_LOG_PATH+"NETMAN"+iso_today+GS_LOG_EXT,
    "MOCK_SAT_CMDR"     : GS_LOG_PATH+"COMMANDER"+iso_today+GS_LOG_EXT,
    "MOCK_SAT_RADIO"    : GS_LOG_PATH+"HE100"+iso_today+GS_LOG_EXT,
}
GND_LOG_FILES = {
    "GROUND_NETMAN"     : GS_LOG_PATH+"GROUND_NETMAN"+iso_today+GS_LOG_EXT,
    "GROUND_COMMANDER"  : GS_LOG_PATH+"GROUND_COMMANDER"+iso_today+GS_LOG_EXT,
    "GROUND_RADIO"      : GS_LOG_PATH+"GROUND_RADIO"+iso_today+GS_LOG_EXT,
}

KW_GETTIME  = "010001313337"    #0x01 0x00 0x01 0x31 0x33 0x37
KW_CONFIRM  = "02000121242b"    #0x02 0x00 0x01 0x21 0x24 0x2b
KW_ACK      = "31210052d5"      #0x31 0x21 0x00 0x52 0xd5

settime   = bytearray.fromhex('30 64 00 00 00 00');
gettime   = bytearray.fromhex('31');
update    = bytearray.fromhex('32');
getlog    = bytearray.fromhex('33');
reboot    = bytearray.fromhex('34');
decode    = bytearray.fromhex('35');
deletelog = bytearray.fromhex('36');
timetag   = bytearray.fromhex('37');
confirm   = bytearray.fromhex('21');

#-------------------------------------------------------------
# WRAPPER FUNCTIONS FOR SUBPROCESS 
#-------------------------------------------------------------

def subCustom(args):
    return subprocess.Popen(
            args,
            bufsize=0,
            executable=None,
            stdin=None,
            stdout=None,
            stderr=None,
            preexec_fn=None,
            close_fds=False,
            shell=False,
            cwd=None,
            universal_newlines=False,
            startupinfo=None,
            creationflags=0,
            evn=None
    )

def subP(args):
    return subprocess.Popen(
            args,
            shell=False,
            stdout=subprocess.PIPE
    )

def subShell(args):
    return subprocess.Popen(
            args,
            shell=True,
            executable="/bin/bash"
    )

#-------------------------------------------------------------
# VARIOUS SYSTEM WRAPPER FUNCTIONS 
#-------------------------------------------------------------
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

def exit(exit_message="No message"):
    print "\r\nExiting: "+exit_message
    sys.exit(1)

def signal_handler(signal, frame):
  print '\r\nCaught Cntl+C!'
signal.signal(signal.SIGINT, signal_handler)

def send_command(command):
    global confirm
    input_pipe = open(GS_PATH["INPUT_PIPE"],"w")
    input_pipe.write(command)
    input_pipe.close()

#-------------------------------------------------------------
# COMMAND WRAPPERS AND TOOLS
#-------------------------------------------------------------

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_valid_time_t(s):
    if (len(s) >8 or len(s) < 4):
        return False
    return is_number(s)

def return_settime_command_buffer():
    print "Enter the time in seconds since epoc for which to set the time:"
    input=raw_input( go_no_go() + " >> " + time.strftime("%H:%M:%S") + " >> " )
    while( not is_valid_time_t(input) ):
        print "Try again, a valid number with at least 4 digits"
        input=raw_input( go_no_go() + " >> " + time.strftime("%H:%M:%S") + " >> " )
    return settime+input


#-------------------------------------------------------------
# GROUND STATION FUNCTIONS 
#-------------------------------------------------------------
def check_requirements():
    for key, requirement in GS_PATH.items():
        if ( os.path.isfile(requirement) ) or ( stat.S_ISFIFO(os.stat(requirement).st_mode) ):
            continue
        else : fail(key+" ("+requirement+") is not present! Try running 'MANAGE_CS1.sh -d'")

# TODO add args
# process = subP([GS_PATH[process_name], args])
def start_process(process_name):
  print "[NOTICE] "+process_name+" STARTING"
  process = subP(GS_PATH[process_name])
  if is_subprocess_running(process):
    print "[NOTICE] "+process_name+" IS RUNNING"
    return process
  else:
    print "[ERROR] "+process_name+" HAS STOPPED"

def start_pcd(pcd_ruleset):
  print "[NOTICE] "+pcd_ruleset+" STARTING"
  process = subP([GS_PATH['PCD'], '-vf', pcd_ruleset])
  if is_subprocess_running(process):
    print "[NOTICE] Ruleset: "+pcd_ruleset+" IS RUNNING"
    return process
  else:
    print "[ERROR] Ruleset:"+pcd_ruleset+" HAS STOPPED"

def is_subprocess_running(subprocess):
    if subprocess is None:
        return False
    if subprocess.poll() is None:
        return True
    else:
        return False

def tear_down() :
    print "[NOTICE] Tearing down all running processes"
    global ground_control
    global log_window
    if ( ground_control is not None ) and ( is_subprocess_running(ground_control) ) :
        subprocess.call([ 'kill', '-9', str(ground_control.pid) ]) # TODO BAD, not OS independent
        print "[NOTICE] Ground Control was terminated"
    if ( log_window is not None ) and ( is_subprocess_running(log_window) ) :
        log_window.terminate()
        print "[NOTICE] Log Window was terminated"
    subprocess.call([ 'killall', '-9','space-commander', 'ground-commander', 'mock_sat','gnd','pcd']) # TODO BAD, not OS independent

def start_ground_station():
  # test local radio

  global ground_control
  ground_control = start_pcd( PCD_RULESET_LIST["GROUND_STATION"] )

  # ping satellite

#end def


def start_mock_interaction():
  global ground_control
  ground_control = start_pcd( PCD_RULESET_LIST["MOCK_SAT_INTERACTION"] )

  global log_window
  log_window = open_log_window()

def open_log_window():
    sat_log_view_command = "tail -f"
    for key, logfile in SAT_LOG_FILES.items():
        if ( os.path.isfile(logfile) ):
            sat_log_view_command+=" "+logfile
        else : print key+" ("+logfile+") is not present!"
    gnd_log_view_command = "tail -f"
    for key, logfile in GND_LOG_FILES.items():
        if ( os.path.isfile(logfile) ):
            gnd_log_view_command+=" "+logfile
        else : print key+" ("+logfile+") is not present!"
    print "In a separate terminal window, run the following command"
    print sat_log_view_command
    print gnd_log_view_command
    #return subP(['xterm', '-e', log_view_command])
    #subprocess.call(['tmux', 'split-window', "'"+log_view_command+"'"])

def go_no_go():
  global ground_control
  return "GO" if is_subprocess_running(ground_control) is True else "NOGO"

def prompt():
    return go_no_go() + " >> " + time.strftime("%H:%M:%S") + " >> "

def command_line_interface():
  print 'Enter commands for the ground station below.\r\nType "menu" for predefined commands, and "exit" to quit'
  input=1
  while 1:
    input=raw_input( prompt() )
    if ((input == "exit") | (input == "q")):
      tear_down()
      exit("Because you asked to.")    
    if ((input == "menu") | (input == "help") | (input == "h")):
      usage()
    if ((input == "start") | (input == "on") | (input == "s")):
      start_ground_station()
    if ((input == "mock") | (input == "mk") | (input == "m")):
      start_mock_interaction()
    if ((input == "teardown") | (input == "td") | (input == "t")):
      tear_down()
    # TODO THIS IS BROKEN FOR SOME REASON
    #if ( is_subprocess_running(ground_control) ):
        print("This is a prototype of the ground station commander in Python to simulate certain commands\n gt - gettime    get the satellite time\n cf - confirm    prompt the satellite to go ahead with the previous command\n td - teardown    terminate all running ground station or mock satellite processes\n q  - exit       and close all other ground station applications");
    if (( input == "gt" ) | (input == "gettime")):
        send_command(gettime)
    if (( input == "st" ) | (input == "settime")):
        settime_command_buffer = return_settime_command_buffer() 
        send_command(settime_command_buffer)
    if (( input == "gl" ) | (input == "getlog")):
        input=raw_input("Please enter the")
        #isotoday
        send_command(gettime)
    if (( input == "cf" ) | (input == "confirm")):
        send_command(confirm)

#-------------------------------------------------------------
# GROUND STATION FUNCTIONS 
#-------------------------------------------------------------
def main():
    check_requirements()
    usage()
    command_line_interface()
    tear_down()
    exit("Reached end of main")

if __name__ == '__main__':
    main()
