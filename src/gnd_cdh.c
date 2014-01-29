#include <stdio.h>
#include <string.h>

#include "../include/gnd_commands.h"
#include "../include/of2g.h"

#define MAX_FRAME_LENGTH 190

// This function loads a command table and queues all commands to be transmitted.
bool cdh_load(cmd_info_t cmdinfo)
{
  return true;
}

// Initializes the command queue
bool cdh_queue_init()
{
  return true;
}

// Add a command to the queue list
bool cdh_enqueue(command_t cmd)
{
  return true;
}


// Remove the last added command from the queue list
bool cdh_dequeue()
{
  return true;
}


// Add a command a new command
bool cdh_new(command_t cmd) // TODO: Specify priority or sequence number
{
  return true;
}

// Add a command that to the queue with a delayed time // TODO: Delayed time vs specific time
bool cdh_enqueue_delayed(command_t cmd, uint32_t delay_s)
{
  return true;
}

// Clears and resets the command queue
bool cdh_queue_clear()
{
  return true;
}

// The following function reconstructs a file received from the satellite
bool cdh_rx_file()
{
  return true;
}

// This function stores received bytes into a data structure
// TODO: cat a file
bool cdh_store_recv_data()
{
  return true;
}

// This function transmit the prepared command frames
bool cdh_tx_cmd()
{
  return true;
}
