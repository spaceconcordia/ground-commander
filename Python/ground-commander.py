#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2014 Shawn <shawn dot bulger at spaceconcordia dot ca>
#
# Distributed under terms of the MIT license.

"""
This is a prototype of the ground station commander in Python to simulate certain commands 
"""

settime   = bytearray.fromhex('30 21');
gettime   = bytearray.fromhex('31 21');
update    = bytearray.fromhex('32 21');
getlog    = bytearray.fromhex('33 21');
reboot    = bytearray.fromhex('34 21');
decode    = bytearray.fromhex('35 21');
deletelog = bytearray.fromhex('36 21');
timetag   = bytearray.fromhex('37 21');

def GC_printMenu():
  print 'st - settime    set the satellite time\r'
  print 'gt - gettime    get the satellite time\r'
  print 'ud - update     update a binary on the satellite\r'
  print 'gl - getlog     get a log file from the satellite\r'
  print 'rb - reboot     reboot the satellite\r'
  print 'dc - decode\r'
  print 'dl - deletelog  delete a log from the satellite\r'
  print 'tt - timetag    timetag a command on the satellite\r'
  print 'q  - exit       and close all other ground station applications\r\n'

GC_printMenu()
