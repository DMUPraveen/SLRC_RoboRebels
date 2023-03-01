#line 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Controller.h"
#ifndef MOTOR_CONTROLLER
#define MOTOR_CONTROLLER

const long MAX_OUTPUT = 255;
const long MIN_VALUE_FOR_OUTPUT = 90;

const float zero_threshold = 0.01f;

struct Motor_Controller
{

    uint8_t m_motor_in1 = 6;
    uint8_t m_motor_in2 = 9;
    uint8_t m_motor_in3 = 10;
    uint8_t m_motor_in4 = 11;
    Motor_Controller(
        uint8_t m_motor_in1,
        uint8_t m_motor_in2,
        uint8_t m_motor_in3,
        uint8_t m_motor_in4)
        : m_motor_in1(m_motor_in1), m_motor_in2(m_motor_in2), m_motor_in3(m_motor_in3), m_motor_in4(m_motor_in4)
    {
        pinMode(m_motor_in1, OUTPUT);
        pinMode(m_motor_in2, OUTPUT);
        pinMode(m_motor_in3, OUTPUT);
        pinMode(m_motor_in4, OUTPUT);

        analogWrite(m_motor_in1, 0);
        analogWrite(m_motor_in2, 0);
        analogWrite(m_motor_in3, 0);
        analogWrite(m_motor_in4, 0);
    }

    void set_motor_speed_raw(long motor1_speed, long motor2_speed)
    {
        if (motor1_speed >= 0)
        {
            analogWrite(m_motor_in1, motor1_speed);
            analogWrite(m_motor_in2, 0);
        }
        else
        {
            analogWrite(m_motor_in1, 0);
            analogWrite(m_motor_in2, -motor1_speed);
        }
        if (motor2_speed >= 0)
        {
            analogWrite(m_motor_in3, motor2_speed);
            analogWrite(m_motor_in4, 0);
        }

        else
        {
            analogWrite(m_motor_in3, 0);
            analogWrite(m_motor_in4, -motor2_speed);
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
        // Serial.print(m1s);
        // Serial.print(",");
        // Serial.println(m2s);

        set_motor_speed_raw(m1s, m2s);
    }

    void stop()
    {
        analogWrite(m_motor_in1, 0);
        analogWrite(m_motor_in2, 0);
        analogWrite(m_motor_in3, 0);
        analogWrite(m_motor_in4, 0);
    }

    void brake()
    {

        analogWrite(m_motor_in1, 1);
        analogWrite(m_motor_in2, 1);
        analogWrite(m_motor_in3, 1);
        analogWrite(m_motor_in4, 1);
    }
};

#endif