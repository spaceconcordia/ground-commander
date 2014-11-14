#ifndef GND_COMMANDS_H_
#define GND_COMMANDS_H_

//  This file describes how command frames are built and sent to the satellite

#include <inttypes.h>
#include <stdbool.h>

#include <unistd.h>
#include "gnd_cdh.h"

// These functions will generate the proper bytes to be transceived depending on the command

bool cmd_get_time();
bool cmd_set_time(uint32_t time);

// This function retrieves n bytes from a log file for a given subsystem
// TODO: Get log command currently consumes n bytes from a log file. We want to obtain the whole file, not just the logs
/*
5 bytes for the get log command:
0x33: get log command
0x30: subsystem 0 in ASCII
Next 3 bytes are the number of bytes to grab
0x31:'1'
0x30:'0'
0x30:'0'
Grabbing 100 bytes
*/
bool cmd_get_ss_log(subsystem_t subystem, size_t bytes);

bool cmd_reboot(uint32_t time, bool force, char* reason);
/*
example input: cmd_upload("/home/olivier/test.txt", "test.txt")
filename is the path of the file to be uploaded

0x32: update command
Next 3 bytes are for destinath path length
'0' '1' '9'
destination path /home/olivier/test.txt is 19 bytes long

Following bytes is the path string
"/home/olivier/test.txt" in hex

Next 3 bytes are the size of the file
'0' '1' '2'
file to upload is 12 bytes in size

The following bytes is the file content in hex
"hello space "

Complete output in ascii: '2019/home/logs/test.txt012hello space \n'
Output in hex: \\x32\\x30\\x31\\x39\\x2f\\x68\\x6f\\x6d\\x65\\x2f\\x6c\\x6f\\x67\\x73\\x2f\\x74\\x65\\x73\\x74\\x2e\\x74\\x78\\x74\\x30\\x31\\x32\\x68\\x65\\x6c\\x6c\\x6f\\x20\\x73\\x70\\x61\\x63\\x65\\xa'
*/
bool cmd_upload(char* destination_path, char* filename);
bool cmd_decode(char* src_path, char* dest_path, size_t size);

bool cmd_kill_process(char* process_name, pid_t pid, subsystem_t ss);
bool cmd_start_process(subsystem_t ss);
bool cmd_tx_test();

// This function will notify the satellite to validate and execute the last received command
bool cmd_execute(void);
bool cmd_execute(command_t cmd);

#endif
