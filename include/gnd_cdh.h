#ifndef GND_CDH_H_
#define GND_CDH_H_

// This file defines the logic of the command and data handling on the ground station
// upon communication with the satellite

// This component is reponsible for:
// 1. Split a file into multiple frames to be uploaded
// 2. Reconstruct a file from the satellite
// 3. Send time-tagged commands to the satellite
// 4. Queue commands that will be sent to the satellite

// TODO: Review design of this application
// 1. Split this file into many
// 2. Implement queue
// 3. Implement functions
// 4. Queue data in case communication breaks when not finished uploading
// 5. On satellite: queue received commands
// 6. cdh vs cmd namespace
// 7. Have a CLI and parse user input
// 8. Review return types & function parameters
// 9. Store and display time of received data
// 10. Store command response/data

// Reasons to use SQL for log managing:
// 1. Obtain specific log information (temperature reading from sensor x)
// 2. View all log with errors
// 3. If in 1 file, we simplify file system structure
// 4. Can use SQL api
// 5. Better organization of data (seperates errors and actual telemetry)

#include <inttypes.h>
#include <string.h>
#include <stdbool.h>

// This enum describes the subsystem for obtaining information or to perform a specific command
// TODO: Get commands for specific sensor
typedef enum {
  SS_ACS = 0x30,
  SS_COMMS = 0x31,
  SS_CDH = 0x32,
  SS_MECH = 0x33,
  SS_PAYLOAD = 0x34,
  SS_POWER = 0x35,
  SS_NETMAN = 0x36,
  SS_BABYCRON = 0x37,
  SS_WATCHPUPPY = 0x38
} subsystem_t;

// This enum defined the commands that can be sent to the satellite
// TODO: Have more specific commands, ie: Get temperature reading from sensor X
// Differentiate log (any notice) vs actual telemetry data
typedef enum {
  CMD_EXECUTE = 0x21,
  CMD_GET_TIME = 0x30,
  CMD_SET_TIME = 0x31,
  CMD_UPLOAD  = 0x32,
  CMD_GET_LOG = 0x33,
  CMD_REBOOT = 0x34, // TODO: Specify reboot reason

  // TODO: should the satellite automatically know how to decode when it receives a binary?
  CMD_DECODE = 0x35,

  // The following commands have not been implemented yet on the satellite
  CMD_KILL_PROCESS = 0x37,
  CMD_START_PROCESS = 0x38,
  CMD_GET_REMAINING_MEMORY = 0x39,

  // Verifies all processes currently active and their run time
  // TODO: Check definition: process vs subsystem
  CMD_GET_ALL_PROCESS = 0x3A,

  // Test communication with satellite
  // TODO: Add on satellite a way to response to this command for test purposes
  CMD_TEST_TX = 0x3B
} command_t;

// The following struct holds information regarding a subsystem
typedef struct {
  char* ss_name;
  pid_t ss_pid;
  uint32_t ss_run_time;

} subsystem_info_t;

// This struct describes commands that can be loaded to queue commands
// TODO: Define specific commands
typedef struct {
  uint32_t priority;
  command_t cmds[];
  uint32_t time;

} cmd_info_t;

// This function loads a command table and queues all commands to be transmitted.
bool cdh_load(cmd_info_t cmdinfo);

// Initializes the command queue
bool cdh_queue_init();

// Add a command to the queue list
bool cdh_enqueue(command_t cmd);

// Remove the last added command from the queue list
bool cdh_dequeue();

// Add a command a new command
bool cdh_new(command_t cmd); // TODO: Specify priority or sequence number

// Add a command that to the queue with a delayed time // TODO: Delayed time vs specific time
bool cdh_enqueue_delayed(command_t cmd, uint32_t delay_s);

// Clears and resets the command queue
bool cdh_queue_clear();

// The following function reconstructs a file received from the satellite
bool cdh_rx_file();

// This function stores received bytes into a data structure
// TODO: cat a file
bool cdh_store_recv_data();

// This function transmit the prepared command frames
bool cdh_tx_cmd();

#endif
