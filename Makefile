CC=g++
BB=arm-linux-gnueabi-g++
CFLAGS=-Wall
DEBUGFLAGS=-ggdb -g -gdwarf-2 -g3 #gdwarf-2 + g3 provides macro info to gdb
INCPATH=-I./include/ -I../space-lib/shakespeare/inc/ -I../space-netman/lib/include
LIBPATH=-L./lib/ -L../space-lib/shakespeare/lib -L../space-netman/lib
LIBS= -lshakespeare -lNamedPipe

DEBUG_SRC_FILES =`find src/ ! -name 'baby-cron-main.c' -name '*.c'`

buildBin:
	$(CC) $(CFLAGS) $(INCPATH) $(LIBPATH) src/*.c -o bin/gnd-commander -lshakespeare

buildBB:
	$(BB) $(CFLAGS) $(INCPATH) $(LIBPATH) src/*.c -o bin/gnd-commander-bb -lshakespeare-BB

p1:
	$(CC) $(CFLAGS) $(INCPATH) $(LIBPATH) *.c -o $@ -lshakespeare -lNamedPipe
