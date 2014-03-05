// using GoogleTests
#include "gtest/gtest.h"
#include "../../include/of2g.h"
#include "../../include/gnd_commands.h"

class ground_command_test : public ::testing::Test {
	protected:
	virtual void SetUp() {
}
  char* upload_bytes = "2019/home/logs/test.txt012hello space \n";
  unsigned char getlog_bytes[5] = {0x33, 0x30, 0x31, 0x30, 0x30};

};

TEST_F(ground_command_test, GetTimeCommand) {
  bool result = cmd_get_time();
}

TEST_F(ground_command_test, SetTimeCommand) {
  cmd_set_time(2013);
}

TEST_F(ground_command_test, UploadCommand) {
  bool result = cmd_upload("/home/logs/test.txt", "test.txt");
}

TEST_F(ground_command_test, GetLogCommand) {
  bool result = cmd_get_ss_log(SS_ACS, 100);
  ASSERT_TRUE(result);
}

TEST_F(ground_command_test, Execute) {
  bool result = cmd_execute();
}

TEST_F(ground_command_test, RebootCommand) {
  bool result = cmd_reboot(2013, true, "reason");
}

TEST_F(ground_command_test, DecodeCommand) {
}

