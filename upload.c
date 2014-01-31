#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <string.h>

#define MAX_SIZE 256
#define CMD_UPLOAD 0x32

int main ()
{
  char* destination_path = "/home/logs/test.txt";
  char* filename = "test.txt";
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
  size_t max_data_bytes = MAX_SIZE - 1 - 3 - path_length - 3;

  char hex_cmd[300];
  hex_cmd[0] = CMD_UPLOAD;
  hex_cmd[1] = '0';
  snprintf(hex_cmd + 1 + 1, 4,"%d", path_length);
  // TODO: Get rid of null character
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
      snprintf(hex_cmd + 1 + 3 + path_length, 4, "%d", file_size);
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
    total_bytes_read += bytes_read;
  }

  return 0;
}
