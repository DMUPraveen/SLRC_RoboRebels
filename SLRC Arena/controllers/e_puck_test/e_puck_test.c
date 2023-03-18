#include <webots/robot.h>

// Added a new include file
#include <webots/motor.h>

#define TIME_STEP 32

#define MAX_SPEED 6.28

int main(int argc, char **argv) {
  wb_robot_init();



  while (wb_robot_step(TIME_STEP) != -1) {
  }

  wb_robot_cleanup();

  return 0;
}