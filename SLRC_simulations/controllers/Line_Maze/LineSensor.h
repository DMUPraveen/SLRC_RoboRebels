#include <stdint.h>
#include <algorithm>
#include <vector>
#include <webots/Robot.hpp>
#include <webots/DistanceSensor.hpp>
#ifndef LINESENSOR_HEADER
#define LINESENSOR_HEADER

using namespace webots; // bad idea?
using namespace std;

const uint8_t NUM_SENSORS = 8;
struct LineSensor
{
    /*

    Provides an interface and ultility functions for Lines Sensor

    */
    float m_readings[NUM_SENSORS] = {0.0f};

    vector<DistanceSensor *> m_distanceSensors;
    // varaibles for line detection
    uint8_t m_linedetected[NUM_SENSORS] = {0};
    float m_line_detection_threshold = 0.0f;
    Robot *m_robot;
    // vdistance weights for each sensor
    float weight[8] = {-4.0f, -3.0f, -2.0f, -1.0f, 1.0f, 2.0f, 3.0f, 4.0f};
    int m_timestep = 0;

    LineSensor(vector<DistanceSensor *> distanceSensors, int timestep, Robot *robot)
        : m_distanceSensors(distanceSensors), m_robot(robot), m_timestep(timestep)
    {
        for (uint8_t i = 0; i < NUM_SENSORS; i++)
        {
            m_distanceSensors[i]->enable(timestep);
        }
    }

    void update_readings()
    {

        // updates stored raw readings
        for (uint8_t i = 0; i < NUM_SENSORS; i++)
        {
            m_readings[i] = m_distanceSensors[i]->getValue();
        }
    }

    void update()
    {
        // updates both raw readings and whether a line was detected or not as well
        update_readings();
        caluclate_line_detected();
    }

    void calibrate(int32_t iterations) // this function is a blocking function
    {
        /*
         used to calibrate the threshold value
          this function will call webots step so can be called outside of the while Loop
         Caution Calls Robot.step
        */
        //  dark values
        float dark_sum = 0.0f;   // sum(x)
        float dark_2_sum = 0.0f; // sum(x^2)

        // light values
        float light_sum = 0.0f;
        float light_2_sum = 0.0f;

        for (int j = 0; j < iterations; j++)
        {

            m_robot->step(m_timestep);
            update_readings();
            float max_reading = 0.0f; // readins are greater than 0
            float min_reading = 1.0f; // readins are less than 1
            for (int i = 0; i < NUM_SENSORS; i++)
            {
                max_reading = max(max_reading, m_readings[i]);
                min_reading = min(min_reading, m_readings[i]);
            }
            dark_sum += max_reading;
            dark_2_sum += max_reading * max_reading;

            light_sum += min_reading;
            light_2_sum += min_reading * min_reading;
        }

        float dark_mean = dark_sum / iterations;
        float dark_variation = dark_2_sum / iterations - dark_mean * dark_mean;

        float light_mean = light_sum / iterations;
        float light_variation = light_2_sum / iterations - light_mean * light_mean;
        m_line_detection_threshold =
            (dark_mean * light_variation + light_mean * dark_variation) / (dark_variation + light_variation);
        m_line_detection_threshold = (dark_mean + light_mean) / 2;
    }

    void caluclate_line_detected()
    {
        // calculating whether lines are detected using the line_detection_threshold
        for (int i = 0; i < NUM_SENSORS; i++)
        {
            m_linedetected[i] = (m_readings[i] < m_line_detection_threshold);
        }
    }

    float calculate_line_position(bool &has_line)
    {
        /*
        calucalte the position of the line and whether a line was detected at all

        the returned value will be in the range [-1,1], has_line will indicate whether a
        line was detected or not

        If no line is detected,
            has_line will be set to false
            return value will be 0

        If a line is detected
            has_line will be set to true
            return value will be in the range [-1,1]

        */
        float weighted_sum = 0.0f;
        float num_weights = 0.0f;
        for (int i = 0; i < NUM_SENSORS; i++)
        {
            weighted_sum += weight[i] * m_linedetected[i];
            num_weights += m_linedetected[i];
        }
        if (num_weights == 0)
        {
            has_line = false;
            return 0;
        }
        has_line = true;
        return weighted_sum / num_weights / 4;
    }
};
#endif
