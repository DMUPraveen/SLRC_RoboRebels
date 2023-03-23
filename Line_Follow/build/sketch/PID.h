#line 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Line_Follow\\PID.h"
#ifndef PID_HEADER
#define PID_HEADER

void unit_float_clamp(float &value)
{
    // clamps a value between -1 and 1 (by reference)
    if (value > 1.0f)
    {
        value = 1.0f;
    }

    if (value < -1.0f)
    {
        value = -1.0f;
    }
}

struct PID_data
{
    float K_P;
    float K_I;
    float K_D;
    float Derivative_filter;
};

struct PID
{

    float m_set_point = 0.0f;

    // gain values
    float m_K_P = 0.0f;
    float m_K_D = 0.0f;
    float m_K_I = 0.0f;

    float m_derivative_filter_constant = 0.0f; // when 0 there is no filtering /1 meanse noe derivative calculations
    // must be between 0 and 1

    // vairables used for calculation puposes
    float m_I_error = 0.0f;   // integration of the error
    float m_pre_error = 0.0f; // previous error
    float m_D_error = 0.0f;   // derivative term

    PID()
    {
    }
    PID(PID_data data) // used for setting data from a external packet
    {
        m_K_P = data.K_P;
        m_K_I = data.K_I;
        m_K_D = data.K_D;
        m_derivative_filter_constant = data.Derivative_filter;
    }

    PID(float K_P, float K_D, float K_I, float derivative_filter)
        : m_K_P(K_P), m_K_D(K_D), m_K_I(K_I), m_derivative_filter_constant(derivative_filter)
    {
    }

    void reset()
    {

        m_I_error = 0.0f;
        m_pre_error = 0.0f;
        m_D_error = 0.0f;
    }

    void set_point(float set_point)
    {
        m_set_point = set_point;
    }

    float control(float measurement, float delta)
    {
        /*
            Returns a value between 1 and -1
        */

        float error = m_set_point - measurement;

        m_I_error = m_I_error + delta * error;

        //---------------integrator anti-windup-------------------
        unit_float_clamp(m_I_error); // not ideal but will work for now
        //--------------------------------------------------------

        float new_derivative = (error - m_pre_error) / delta;

        m_D_error = m_derivative_filter_constant * m_D_error + (1 - m_derivative_filter_constant) * new_derivative;

        // caluclating the signal
        float signal = m_K_P * error + m_K_I * m_I_error + m_K_D * m_D_error;

        unit_float_clamp(signal);

        // storing values for next calculation
        m_pre_error = error;

        return signal;
    }
};

#endif