#include "Motor_Controller.h"

#include "Encoder_helper.h"
#include "SpeedCal.h"
const uint8_t motor_in1 = 6;
const uint8_t motor_in2 = 9;
const uint8_t motor_in3 = 10;
const uint8_t motor_in4 = 11;

long speed = 0;
float fspeed = 0.0f;

SpeedCal sc = SpeedCal();

Motor_Controller controller(
    motor_in1,
    motor_in2,
    motor_in3,
    motor_in4);
void setup()
{
    Serial.begin(9600);
    setup_encoders_with_interrupts();
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
    controller.set_motor_speed(fspeed, 0.0f);
    sc.update(countA, countB);
    Serial.println(sc.speed_A);
    delay(5);
}
