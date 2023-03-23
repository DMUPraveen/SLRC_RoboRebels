
#ifndef NAVIGATOR
#define NAVIGATOR
#include "PID.h"
#include "Motor_Controller.h"

struct Navigator
{
    Motor_Controller *m_motors = nullptr;
    PID linear_pid = PID(1, 0, 0, 0);
    PID rotate_pid = PID(1, 0, 0, 0);
    volatile int64_t *countA = nullptr;
    volatile int64_t *countB = nullptr;
    int64_t start_countA = 0;
    int64_t start_countB = 0;
    Navigator(Motor_Controller *motors) : m_motors(motors)
    {
        linear_pid.set_point(0);
        linear_pid.set_point(0);
    }

    void go_straight_initialize()
    {
        start_countA = *countA;
        start_countB = *countB;
    }
    void go_straight(float linear_speed, float delta_t)
    {
        float error = (*countA - start_countA) - (*countB - start_countB);
        float sig = linear_pid.control(error, delta_t);
        m_motors->set_motor_speed(linear_speed + sig, linear_speed - sig);
    }
    void rotate_initialize()
    {
        start_countA = *countA;
        start_countB = *countB;
    }
    void rotate(float rotate_speed, float delta_t)
    {
        float error = (*countA - start_countA) + (*countB - start_countB);
        float sig = rotate_pid.control(error, delta_t);
        m_motors->set_motor_speed(rotate_speed, -rotate_speed);
    }
};

#endif