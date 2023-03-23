#ifndef COMMUNICATION_HEADER
#define COMMUNICATION_HEADER

#include "LineSensor.h"
#include "Motor_Controller.h"

const size_t MAX_FUNCTIONS = 10;
const size_t MAX_BUFFER = 20;

struct Communicator
{
    uint8_t m_buffer[MAX_BUFFER];

    void (*m_functions[MAX_FUNCTIONS])(void *buffer);
    LineSensor *linesensor = nullptr;
    volatile int64_t *countA = nullptr;
    volatile int64_t *countB = nullptr;
    Motor_Controller *motors = nullptr;

    void communicate()
    {
        if (!Serial.available())
        {
            return;
        }
        uint8_t instruction = Serial.read();
        uint8_t size = Serial.read();
        if (size != 0)
        {
            Serial.readBytes(m_buffer, size);
        }
        m_functions[instruction](m_buffer);
        while (Serial.available())
        {
            Serial.read();
        }
    }
};

#endif