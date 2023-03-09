#ifndef LINESENSOR_HEADER
#define LINESENSOR_HEADER
const float max_value = 4095.0f;
struct LineSensor
{
    const uint8_t *m_pins;
    uint8_t m_size;
    float m_readings[8] = {0.0f};
    LineSensor(const uint8_t *pins, uint8_t size)
        : m_pins(pins), m_size(size)
    {
        for (uint8_t i = 0; i < m_size; i++)
        {
            pinMode(m_pins[i], INPUT);
        }
    }

    void update()
    {

        for (uint8_t i = 0; i < m_size; i++)
        {
            m_readings[i] = ((float)analogRead(m_pins[i])) / (max_value);
        }
    }
};
#endif
