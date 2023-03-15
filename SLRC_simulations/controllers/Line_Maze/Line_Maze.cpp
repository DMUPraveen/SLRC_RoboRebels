#include <webots/Robot.hpp>
#include <webots/DistanceSensor.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <LineSensor.h>
using namespace std;
using namespace webots;

string line_sensor_names[] = {
    "linesensor(1)",
    "linesensor(2)",
    "linesensor(3)",
    "linesensor(4)",
    "linesensor(5)",
    "linesensor(6)",
    "linesensor(7)",
    "linesensor(8)",
};
vector<DistanceSensor *> create_line_sensors(Robot *rb, string line_sensor_names[])
{
  vector<DistanceSensor *> v;
  for (int i = 0; i < 8; i++)
  {
    v.push_back(rb->getDistanceSensor(line_sensor_names[i]));
  }
  return v;
}

void destroy_line_sensors(vector<DistanceSensor *> &vdis)
{
  for (DistanceSensor *x : vdis)
  {
    delete x;
  }
}

int main(int argc, char **argv)
{
  Robot *robot = new Robot();

  int timeStep = (int)robot->getBasicTimeStep();
  auto line_sensors = create_line_sensors(robot, line_sensor_names);

  LineSensor linesensor = LineSensor(line_sensors, timeStep, robot);
  cout << "Starting calibration" << endl;
  linesensor.calibrate(100);
  cout << "Finished calibration" << endl;
  cout << linesensor.m_line_detection_threshold << endl;
  while (robot->step(timeStep) != -1)
  {
    linesensor.update();
    for (int i = 0; i < 8; i++)
    {
      cout << (int)linesensor.m_linedetected[i] << " ";
    }
    bool has_line = false;
    cout << linesensor.calculate_line_position(has_line) << " ";
    cout << (has_line ? "line_detected" : "no line_detected");
    cout << endl;
  }

  delete robot;
  destroy_line_sensors(line_sensors);
  return 0;
}
