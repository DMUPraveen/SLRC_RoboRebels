#ifndef RESOURCE_MANAGER_HEADER
#define RESOURCE_MANAGER_HEADER

#include <webots/Robot.hpp>
#include <webots/DistanceSensor.hpp>
#include <iostream>
#include <vector>
#include <string>
#include "LineSensor.h"
using namespace std;
using namespace webots;

struct ResourceManager
{
    /*

    Used to Manage Resources so that manual deletion of variables need not be done
    Performed Automatically upon deallocation
    ------ Notes -----
    m_linesensor is not calibrated this must be done manually

    ------------------
    */
    LineSensor *m_linesensor;
    Robot *m_robot;
    int m_time_step = 0;
    ResourceManager();
    ~ResourceManager();
};

#endif