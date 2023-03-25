# 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Line_Follow\\Line_Follow.ino"
# 2 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Line_Follow\\Line_Follow.ino" 2
# 3 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Line_Follow\\Line_Follow.ino" 2
# 4 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Line_Follow\\Line_Follow.ino" 2

# 6 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Line_Follow\\Line_Follow.ino" 2





BluetoothSerial SerialBT;
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

float pre_measurement = 0.0f;
Motor_Controller mt = Motor_Controller(
    motor_in1,
    motor_in2,
    motor_in3,
    motor_in4);

PID pid = PID(0.7f, 0.0f, 0.0f, 0.0f);
void setup()
{
    SerialBT.begin("Watson");
    pinMode(LED_BUILTIN /* backward compatibility*/, 0x03);
    delay(5000);
    SerialBT.println("Begin calibrating");
    digitalWrite(LED_BUILTIN /* backward compatibility*/, 0x1);
    ls.calibrate(calibration_iterations);
    digitalWrite(LED_BUILTIN /* backward compatibility*/, 0x0);
    SerialBT.println("End calibrating");
    delay(5000);
    pid.set_point(0.0);
}

void loop()
{
    ls.update();
    //    SerialBT.printf(
    //        "%i %i %i %i %i %i %i %i %f\n",
    //        ls.m_linedetected[0],
    //        ls.m_linedetected[1],
    //        ls.m_linedetected[2],
    //        ls.m_linedetected[3],
    //        ls.m_linedetected[4],
    //        ls.m_linedetected[5],
    //        ls.m_linedetected[6],
    //        ls.m_linedetected[7],
    //        ls.m_line_detection_threshold);
    bool has_line = false;
    SerialBT.printf(
        "%f %f %f %f %f %f %f %f %f\n",
        ls.m_readings[0],
        ls.m_readings[1],
        ls.m_readings[2],
        ls.m_readings[3],
        ls.m_readings[4],
        ls.m_readings[5],
        ls.m_readings[6],
        ls.m_readings[7],
        ls.calculate_line_position(has_line));

    float measurement = ls.calculate_line_position(has_line);
    if (!has_line)
    {
        // mt.set_motor_speed(pre_measurement * 0.75, -pre_measurement * 0.75);
        SerialBT.printf("No line detected pre measurement %f", pre_measurement);
    }
    else
    {

        pre_measurement = pre_measurement * 0.2 + measurement * 0.8;
        float control_signal = pid.control(measurement, 1.0f);
        // mt.set_motor_speed(0.3 + 0.5 * control_signal, 0.3 - 0.5 * control_signal);
    }
    // Serial.printf(
    //     "measurement : %f,control_signal: %f\n",
    //     measurement, control_signal);
}
