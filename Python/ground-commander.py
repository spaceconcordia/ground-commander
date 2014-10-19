#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Shawn <shawn dot bulger at spaceconcordia dot ca>
#
# Distributed under terms of the MIT license.

"""
This is a prototype of the ground station commander in Python to simulate certain commands 
st - settime    set the satellite time
gt - gettime    get the satellite time
ud - update     update a binary on the satellite
gl - getlog     get a log file from the satellite
rb - reboot     reboot the satellite
dc - decode
dl - deletelog  delete a log from the satellite
tt - timetag    timetag a command on the satellite
q  - exit       and close all other ground station applications
"""

import os

settime   = bytearray.fromhex('30 21');
gettime   = bytearray.fromhex('31 21');
update    = bytearray.fromhex('32 21');
getlog    = bytearray.fromhex('33 21');
reboot    = bytearray.fromhex('34 21');
decode    = bytearray.fromhex('35 21');
deletelog = bytearray.fromhex('36 21');
timetag   = bytearray.fromhex('37 21');


def usage():
    print(globals()['__doc__'])

usage()
