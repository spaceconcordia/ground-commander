#include <stdio.h>
#include <string.h>

#include "../include/gnd_commands.h"
#include "../include/of2g.h"

#define MAX_FRAME_LENGTH 190

bool cmd_get_time()
{
  size_t data_size = 1;
  unsigned char hex_cmd = CMD_GET_TIME;
  // add to command queue
  return true;
}

bool cmd_set_time(uint32_t time)
{
  size_t data_size = 1;
  unsigned char hex_cmd = CMD_SET_TIME;
  // add to command queue
  return true;
}

// This function retrieves n bytes from a log file for a given subsystem
// TODO: Get log command currently consumes n bytes from a log file. We want to obtain the whole file, not just the logs
bool cmd_get_ss_log(subsystem_t subsystem, size_t bytes)
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
  size_t data_size = 5;
  char hex_cmd[5];
  hex_cmd[0] = CMD_GET_LOG;
  hex_cmd[1] = subsystem;

  snprintf(hex_cmd + 2, 4, "%zu", bytes);
  printf("Get log cmd bytes: ");
  for(int t = 0; t < 5; ++t)
  {
    printf("0x%2X ", hex_cmd[t]);

  }
  printf("\n");

  return true;
}

bool cmd_reboot(uint32_t time, bool force, char* reason)
{
  unsigned char hex_cmd = CMD_REBOOT;
  return true;
}

// TODO: Find a better way to upload files. Atm, we always have to specify the destination path every time we send a frame.
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


// size_t data_size = 1 + 3 + strlen(destination_path) + 3 + strlen(filename) + file_size;

// unsigned char hex_cmd[UPLOAD_FILE_SIZE];
 char* hex_cmd;
 hex_cmd[0] = CMD_UPLOAD;
 int path_length = strlen(destination_path);
 snprintf(hex_cmd + 1, 4,"%d", path_length);
 strcat(hex_cmd, destination_path);

 int file_size;
 snprintf(hex_cmd + path_length + 1, 4, "%d", file_size);
 // Append content of the file
  return true;
}

// This function will notify the satellite to validate and execute the last received command
bool cmd_execute()
{
  size_t data_length = 1;
  unsigned char hex_cmd = 0x21;
  return true;
}

bool cmd_decode()
{
  return true;
}

// Following functions have not been implemented on the commander

bool cmd_kill_process(char* process_name, pid_t pid, subsystem_t ss)
{
  return true;
}


bool cmd_start_process(subsystem_t ss)
{
  return true;
}

bool cmd_tx_test()
{
  return true;
}
