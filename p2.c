// Testing passing a struct through pipes
#include <stdio.h>
#include <NamedPipe.h>

static NamedPipe readpipe("pipe");

static bool initialized = false;

void initialize(){
  if(!initialized) {
    if (!readpipe.Exist()) readpipe.CreatePipe();
    readpipe.ensure_open('r');
    initialized = true;
  }
}


int main(int argc, const char *argv[])
{
  initialize();
  int bytes_read;
  char buffer[256];
  while(1) {
    printf("Reading shit\n");
    getchar();
    readpipe.ensure_open('r');
    bytes_read = readpipe.ReadFromPipe(buffer, 100);
    if ( bytes_read > 0 ) {
      for(int i = 0; i < bytes_read; ++i)
        printf("%c", buffer[i]);
    }

  }

  return 0;
}
