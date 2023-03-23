#ifndef SMART_SPEED_HEADER
#define SMART_SPEED_HEADER
#include "SpeedCal.h"
#include "PID.h"
#include "Motor_Controller.h"

struct SpeedControl
{
    SpeedCal *m_speedcal = nullptr;
    Motor_Controller *m_motors = nullptr;
    PID right_pid = PID(1, 0, 0, 0);
    PID left_pid = PID(1, 0, 0, 0);
    SpeedControl(SpeedCal *speedcal, Motor_Controller *motors) : m_speedcal(speedcal), m_motors(motors)
    {
        left_pid.set_point(0);
        right_pid.set_point(0);
    }

    void control_speed(float left, float right, float delta_t)
    {
        float lerror = left - m_speedcal->speed_A;
        float rerror = right - m_speedcal->speed_B;
        float rc = right_pid.control(lerror, delta_t);
        float lc = left_pid.control(rerror, delta_t);
        m_motors->set_motor_speed(rc, lc);
    }
};

#endif
