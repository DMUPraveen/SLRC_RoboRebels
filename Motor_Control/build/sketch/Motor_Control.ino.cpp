#include <Arduino.h>
#line 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino"
#include "Motor_Controller.h"

#include "Encoder_helper.h"
#include "SpeedCal.h"
const uint8_t motor_in1 = 6;
const uint8_t motor_in2 = 9;
const uint8_t motor_in3 = 10;
const uint8_t motor_in4 = 11;
const uint8_t motor_pins[4] = {motor_in1, motor_in2, motor_in3, motor_in4};

long speed = 0;
float fspeed = 0.0f;
SpeedCal sc = SpeedCal();

Motor_Controller controller(
    motor_in1,
    motor_in2,
    motor_in3,
    motor_in4);
#line 20 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino"
void setup();
#line 29 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino"
void loop();
#line 20 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino"
void setup()
{
    Serial.begin(9600);
    attachInterrupt(
        digitalPinToInterrupt(encoderA),
        ISRA,
        RISING);
}

void loop()
{
    bool speed_recieved = false;
    if (Serial.available())
    {
        speed_recieved = true;
        // speed = Serial.parseInt();
        fspeed = Serial.parseFloat();
    }
    if (speed_recieved)
    {
        Serial.println(fspeed);
    }
    // controller.set_motor_speed_raw(speed, 0);
    controller.set_motor_speed(fspeed, 0.0f);
    // Serial.println((long)sc.pre_countA);
    // Serial.println((long)countA);
    sc.update(countA, countB);
    // Serial.print((long)(countA));
    // Serial.print(",");
    Serial.println(sc.speed_A);
    delay(5);
}

