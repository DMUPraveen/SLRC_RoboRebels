# 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\esp32_pwm_test\\esp32_pwm.ino"
const uint8_t motor_in1 = GPIO_NUM_32;
const uint8_t motor_in2 = GPIO_NUM_33;
const uint8_t motor_in1_channel = 0;
const uint8_t motor_in2_channel = 1;
const uint32_t PWM_frequency = 5000;
const uint8_t resolution_bits = 8;

const uint8_t interrupt_A = GPIO_NUM_36;
const uint8_t dir_A = GPIO_NUM_39;

volatile int64_t countA = 0;
bool direction = false;

void __attribute__((section(".iram1" "." "28"))) ISRA()
{
    if (digitalRead(dir_A))
    {
        countA++;
    }
    else
    {
        countA--;
    }
}

void setup()
{
    ledcSetup(motor_in1_channel, PWM_frequency, resolution_bits);
    ledcAttachPin(motor_in1, motor_in1_channel);
    ledcAttachPin(motor_in2, motor_in2_channel);
    pinMode(dir_A, 0x01);
    attachInterrupt(
        (((interrupt_A)<40)?(interrupt_A):-1),
        ISRA,
        0x01);
    Serial.begin(9600);
}

void loop()
{
    if (Serial.available())
    {
        direction = !direction;
        while (Serial.available())
        {
            char t = Serial.read();
        }
    }
    if (direction)
    {
        ledcWrite(motor_in1_channel, 255);
        ledcWrite(motor_in2_channel, 0);
    }
    else
    {

        ledcWrite(motor_in1_channel, 0);
        ledcWrite(motor_in2_channel, 255);
    }
    Serial.println(countA);
}
