#include "ResourceManager.h"

// name for the lines sensors
const string line_sensor_names[] = {
    "linesensor(1)",
    "linesensor(2)",
    "linesensor(3)",
    "linesensor(4)",
    "linesensor(5)",
    "linesensor(6)",
    "linesensor(7)",
    "linesensor(8)",
};

vector<DistanceSensor *> create_line_sensors(Robot *rb, const string line_sensor_names[])
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

ResourceManager::ResourceManager()
{
    m_robot = new Robot();
    m_time_step = (int)m_robot->getBasicTimeStep();
    auto line_sensors = create_line_sensors(m_robot, line_sensor_names);
    m_linesensor = new LineSensor(line_sensors, m_time_step, m_robot);
}

ResourceManager::~ResourceManager()
{
    cout << "Deleting All Resources" << endl;
    delete m_robot;
    destroy_line_sensors(m_linesensor->m_distanceSensors);
    delete m_linesensor;
}