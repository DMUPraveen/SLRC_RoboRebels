#include "LineSensor.h"

const uint8_t line_sensor_size = 8;
const uint8_t lineSensorPins[8] = {
    GPIO_NUM_15,
    GPIO_NUM_4,
    GPIO_NUM_13,
    GPIO_NUM_14,
    GPIO_NUM_27,
    GPIO_NUM_34,
    GPIO_NUM_39,
    GPIO_NUM_36,

};

LineSensor ls = LineSensor(lineSensorPins, line_sensor_size);
void setup()
{
    Serial.begin(9600);
}

void loop()
{
    ls.update();
    Serial.printf("%f,%f,%f,%f,%f,%f,%f,%f\n",
                  ls.m_readings[0],
                  ls.m_readings[1],
                  ls.m_readings[2],
                  ls.m_readings[3],
                  ls.m_readings[4],
                  ls.m_readings[5],
                  ls.m_readings[6],
                  ls.m_readings[7]);
}
