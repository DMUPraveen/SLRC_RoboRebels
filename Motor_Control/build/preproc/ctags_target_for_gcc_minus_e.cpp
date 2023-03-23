# 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino"
# 2 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino" 2

# 4 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino" 2
# 5 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino" 2

# 7 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Motor_Control\\Motor_Control.ino" 2





BluetoothSerial SerialBT;
const uint8_t motor_in1 = 32;
const uint8_t motor_in2 = 33;
const uint8_t motor_in3 = 25;
const uint8_t motor_in4 = 26;

long speed = 0;
float fspeed = 1.0f;

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
    controller.set_motor_speed(fspeed, fspeed);
    sc.update(countA, countB);
    SerialBT.println(sc.speed_A);
    delay(5);
}
