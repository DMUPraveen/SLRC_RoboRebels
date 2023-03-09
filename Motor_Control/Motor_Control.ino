#include "Motor_Controller.h"

#include "Encoder_helper.h"
#include "SpeedCal.h"

#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;
const uint8_t motor_in1 = 32;
const uint8_t motor_in2 = 33;
const uint8_t motor_in3 = 25;
const uint8_t motor_in4 = 26;

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
    SerialBT.begin("Watson");
    setup_encoders_with_interrupts();
}

void loop()
{
    bool speed_recieved = false;
    if (SerialBT.available())
    {
        speed_recieved = true;
        // speed = Serial.parseInt();
        fspeed = SerialBT.parseFloat();
    }
    if (speed_recieved)
    {
        SerialBT.println(fspeed);
    }
    controller.set_motor_speed(fspeed, 0.0f);
    sc.update(countA, countB);
    SerialBT.println(sc.speed_A);
    delay(5);
}
