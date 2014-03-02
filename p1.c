// Testing passing a struct through pipes
#include <stdio.h>
#include <NamedPipe.h>

static NamedPipe writepipe("pipe");

static bool initialized = false;

void initialize(){
  if(!initialized) {
    if (!writepipe.Exist()) writepipe.CreatePipe();
    writepipe.ensure_open('r');
    initialized = true;
  }
}

int main(int argc, const char *argv[])
{
  initialize();
  char* test = "12345";
  while(1) {
    getchar();
    if(writepipe.Exist()) {
      printf("Writing shit\n");
      if (!writepipe.ensure_open('w'))
        printf("Couldn't open fd\n");

      writepipe.WriteToPipe(test,5);
    }
  }
  return 0;
}
