#line 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Line_Follow\\Analogue_Pin_helper.h"
#ifndef ANALOGUE_PIN_HELPER
#define ANALOGUE_PIN_HELPER

const uint8_t BITDEPTH = 8;
struct AnaloguePin
{
    uint8_t m_pin = 0;
    uint8_t m_channel = 0;

    AnaloguePin()
    {
    }

    AnaloguePin(uint8_t pin, uint8_t channel, uint32_t frequency)
        : m_pin(pin), m_channel(channel)
    {
        ledcSetup(m_channel, frequency, BITDEPTH);
        ledcAttachPin(pin, channel);
    }

    void write(uint8_t duty)
    {
        ledcWrite(m_channel, duty);
    }
};
#endif