#include "LineSensor.h"
#include "PID.h"
#include "Motor_Controller.h"

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
const uint8_t motor_in1 = 32;
const uint8_t motor_in2 = 33;
const uint8_t motor_in3 = 25;
const uint8_t motor_in4 = 26;
const uint32_t calibration_iterations = 10000;
LineSensor ls = LineSensor(lineSensorPins);

Motor_Controller mt = Motor_Controller(
    motor_in1,
    motor_in2,
    motor_in3,
    motor_in4);

PID pid = PID(1.0f, 0.0f, 0.0f, 0.0f);
void setup()
{
    Serial.begin(9600);
    pinMode(BUILTIN_LED, OUTPUT);
    delay(5000);
    Serial.println("Begin calibrating");
    digitalWrite(BUILTIN_LED, HIGH);
    ls.calibrate(calibration_iterations);
    digitalWrite(BUILTIN_LED, LOW);
    Serial.println("End calibrating");
    delay(5000);
    pid.set_point(0.0);
}

void loop()
{
    ls.update();
    // Serial.printf(
    //     "%i %i %i %i %i %i %i %i %f\n",
    //     ls.m_linedetected[0],
    //     ls.m_linedetected[1],
    //     ls.m_linedetected[2],
    //     ls.m_linedetected[3],
    //     ls.m_linedetected[4],
    //     ls.m_linedetected[5],
    //     ls.m_linedetected[6],
    //     ls.m_linedetected[7],
    //     ls.m_line_detection_threshold);
    float measurement = ls.calculate_line_position();
    float control_signal = pid.control(measurement, 1.0f);
    mt.set_motor_speed(0.5 + 0.5 * control_signal, 0.5 - 0.5 * control_signal);
    Serial.printf(
        "measurement : %f,control_signal: %f\n",
        measurement, control_signal);
}
