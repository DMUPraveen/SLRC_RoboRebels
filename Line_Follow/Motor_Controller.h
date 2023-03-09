#ifndef MOTOR_CONTROLLER
#define MOTOR_CONTROLLER

#include "Analogue_Pin_helper.h"

const long MAX_OUTPUT = 255;
const long MIN_VALUE_FOR_OUTPUT = 90;

const float zero_threshold = 0.01f;

const uint8_t bitdepth = 8;
const uint32_t frequency = 5000;
struct Motor_Controller
{

    AnaloguePin m_motor_in1;
    AnaloguePin m_motor_in2;
    AnaloguePin m_motor_in3;
    AnaloguePin m_motor_in4;
    Motor_Controller(uint8_t motor_in1, uint8_t motor_in2, uint8_t motor_in3, uint8_t motor_in4)
    {
        m_motor_in1 = AnaloguePin(motor_in1, 0, 5000);
        m_motor_in2 = AnaloguePin(motor_in2, 1, 5000);
        m_motor_in3 = AnaloguePin(motor_in3, 2, 5000);
        m_motor_in4 = AnaloguePin(motor_in4, 3, 5000);
    }

    void set_motor_speed_raw(long motor1_speed, long motor2_speed)
    {
        if (motor1_speed >= 0)
        {
            m_motor_in1.write(motor1_speed);
            m_motor_in2.write(0);
        }
        else
        {
            m_motor_in1.write(0);
            m_motor_in2.write(-motor1_speed);
        }
        if (motor2_speed >= 0)
        {
            m_motor_in3.write(motor2_speed);
            m_motor_in4.write(0);
        }

        else
        {
            m_motor_in3.write(0);
            m_motor_in4.write(-motor2_speed);
        }
    }
    long convert_to_raw(float value)
    {
        if (abs(value) < zero_threshold)
        {
            return 0;
        }
        if (value < 0)
        {
            return (value) * (MAX_OUTPUT - MIN_VALUE_FOR_OUTPUT) - MIN_VALUE_FOR_OUTPUT;
        }

        return (value) * (MAX_OUTPUT - MIN_VALUE_FOR_OUTPUT) + MIN_VALUE_FOR_OUTPUT;
    }
    void set_motor_speed(float motor1_speed, float motor2_speed)
    {
        motor1_speed = constrain(motor1_speed, -1, 1);
        motor2_speed = constrain(motor2_speed, -1, 1);

        long m1s = convert_to_raw(motor1_speed);
        long m2s = convert_to_raw(motor2_speed);

        set_motor_speed_raw(m1s, m2s);
    }

    void stop()
    {
        m_motor_in1.write(0);
        m_motor_in2.write(0);
        m_motor_in3.write(0);
        m_motor_in4.write(0);
    }

    void brake()
    {

        m_motor_in1.write(1);

        m_motor_in2.write(1);

        m_motor_in3.write(1);

        m_motor_in4.write(1);
    }
};
#endif