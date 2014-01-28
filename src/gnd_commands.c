#include <stdio.h>
#include "../include/gnd_commands.h"
#include "../include/of2g.h"

bool cmd_get_time()
{
  // echo -n -e \\x31 > gnd-input
 unsigned char hex_cmd = 0x31;
}

bool cmd_set_time(uint32 time)
{
  unsigned char hex_cmd = 0x32;
}

// This function retrieves n bytes from a log file for a given subsystem
// TODO: Get log command currently consumes n bytes from a log file. We want to obtain the whole file, not just the logs
bool cmd_get_ss_log(subsystem_t subystem, size_t bytes)
{
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
  unsigned char hex_cmd[5];
  hex_cmd[0] = 0x33;
  hex_cmd[1] = subsystem;
}

bool cmd_reboot(uint32_t time, bool force, char* reason)
{
  // echo -n -e \\x34 > gnd-input
}

bool cmd_upload(char* destination_path, char* filename)
{
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
}

// This function will notify the satellite to validate and execute the last received command
bool cmd_execute()
{
  // echo -n -e \\x21 > gnd-input
  unsigned char hex_cmd = 0x21;
}

bool cmd_decode()
{
}

// Following functions have not been implemented on the commander

bool cmd_kill_process(char* process_name, pid_t pid, subsystem_t ss);
{
}


bool cmd_start_process(subsystem_t ss)
{
}

bool cmd_tx_test()
{
}
