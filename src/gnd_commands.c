#include <stdio.h>
#include <string.h>
#include <sys/stat.h>

#include "../include/gnd_commands.h"
#include "../include/of2g.h"

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

bool cmd_get_ss_log(subsystem_t subsystem, size_t bytes)
{
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
  int i;
  FILE* fp;
  fp = fopen(filename, "r");
  struct stat st;
  int total_bytes_read = 0;

  int path_length = strlen(destination_path);

  // Get length of the file
  stat(filename, &st);
  int file_size = st.st_size;

  // bytes from the file that we can send such that the frame capacity is not exceeded
  size_t max_data_bytes = 190 - 1 - 3 - path_length - 3;
  printf("Max data bytes: %zu\n", max_data_bytes);
  char hex_cmd[300];
  hex_cmd[0] = CMD_UPLOAD;
  hex_cmd[1] = '0';
  snprintf(hex_cmd + 1 + 1, 4,"%d", path_length);
  strcat(hex_cmd, destination_path);

  while(total_bytes_read != file_size)
  {
    char buffer[256];
    size_t bytes_read = fread(buffer, 1, max_data_bytes, fp);
    if(bytes_read < 100)
    {
      hex_cmd[1 + 3 + path_length] = '0';
      snprintf(hex_cmd + 1 + 3 + path_length + 1, 3, "%d", (int)bytes_read);
    }
    else
    {
      snprintf(hex_cmd + 1 + 3 + path_length, 4, "%d", (int)bytes_read);
    }

    for(i = 0; i <= 1 + 3 + path_length + 3 + bytes_read; ++i)
    {
      hex_cmd[1 + 3 + path_length + 3 + i] = buffer[i];
    }
    for(i = 0; i < 1 + 3 + path_length + 3 + bytes_read; ++i)
    {
      printf("%c", hex_cmd[i]);
    }
    printf("\nHEX : \n");
    for(i = 0; i < 1 + 3 + path_length + 3 + bytes_read; ++i)
    {
      printf("\\\\x%2X", hex_cmd[i]);
    }
    printf("\n");

    /*
       add to command queue
    */

    total_bytes_read += bytes_read;
  }

  return true;
}

// This function will notify the satellite to validate and execute the last received command
bool cmd_execute(void)
{
  size_t data_length = 1;
  unsigned char hex_cmd = 0x21;
  return true;
}

bool cmd_decode(char* src_path, char* dest_path, size_t sizee)
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
