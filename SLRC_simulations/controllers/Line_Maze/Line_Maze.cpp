#include <webots/Robot.hpp>
#include <webots/DistanceSensor.hpp>
#include <iostream>
#include <vector>
#include <string>
#include "LineSensor.h"
#include "ResourceManager.h"
using namespace std;
using namespace webots;

int main(int argc, char **argv)
{
  ResourceManager resman = ResourceManager();
  cout << "Starting calibration" << endl;
  resman.m_linesensor->calibrate(100);
  cout << "Finished calibration" << endl;
  cout << resman.m_linesensor->m_line_detection_threshold << endl;
  while (resman.m_robot->step(resman.m_time_step) != -1)
  {
    resman.m_linesensor->update();
    for (int i = 0; i < 8; i++)
    {
      cout << (int)resman.m_linesensor->m_linedetected[i] << " ";
    }
    bool has_line = false;
    cout << resman.m_linesensor->calculate_line_position(has_line) << " ";
    cout << (has_line ? "line_detected" : "no line_detected");
    cout << endl;
  }

  return 0;
}
