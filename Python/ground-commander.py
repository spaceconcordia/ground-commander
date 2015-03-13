#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Shawn <shawn dot bulger at spaceconcordia dot ca>
#
# Distributed under terms of the MIT license.

#st - settime    set the satellite time
#ud - update     update a binary on the satellite
#gl - getlog     get a log file from the satellite
#rb - reboot     reboot the satellite
#dc - decode
#dl - deletelog  delete a log from the satellite
#tt - timetag    timetag a command on the satellite

def prompt():
    return go_no_go() + " >> " + time.strftime("%H:%M:%S") + " >> "



"""
This is a prototype of the ground station commander in Python to simulate certain commands 
gt - gettime    get the satellite time
cf - confirm    prompt the satellite to go ahead with the previous command
q  - exit       and close all other ground station applications
"""

import os

settime   = bytearray.fromhex('30');
gettime   = bytearray.fromhex('31');
update    = bytearray.fromhex('32');
getlog    = bytearray.fromhex('33');
reboot    = bytearray.fromhex('34');
decode    = bytearray.fromhex('35');
deletelog = bytearray.fromhex('36');
timetag   = bytearray.fromhex('37');
confirm   = bytearray.fromhex('21');

def usage():
    print(globals()['__doc__'])


usage()
