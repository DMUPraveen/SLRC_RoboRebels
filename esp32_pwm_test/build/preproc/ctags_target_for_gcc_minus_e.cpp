# 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\esp32_pwm_test\\esp32_pwm.ino"
const uint8_t motor_in1 = GPIO_NUM_25;
const uint8_t motor_in2 = GPIO_NUM_26;

const uint8_t motor_in1_channel = 0;
const uint8_t motor_in2_channel = 1;

const uint8_t motor_in3 = GPIO_NUM_32;
const uint8_t motor_in4 = GPIO_NUM_33;

const uint8_t motor_in3_channel = 2;
const uint8_t motor_in4_channel = 4;

const uint32_t PWM_frequency = 5000;
const uint8_t resolution_bits = 8;

const uint8_t interrupt_A = GPIO_NUM_23;
const uint8_t dir_A = GPIO_NUM_35;

const uint8_t interrupt_B = GPIO_NUM_18;
const uint8_t dir_B = GPIO_NUM_19;

volatile int64_t countA = 0;
volatile int64_t countB = 0;
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

void __attribute__((section(".iram1" "." "29"))) ISRB()
{
    if (digitalRead(dir_B))
    {
        countB++;
    }
    else
    {
        countB--;
    }
}
void setup()
{
    ledcSetup(motor_in1_channel, PWM_frequency, resolution_bits);
    ledcSetup(motor_in2_channel, PWM_frequency, resolution_bits);
    ledcSetup(motor_in3_channel, PWM_frequency, resolution_bits);
    ledcSetup(motor_in4_channel, PWM_frequency, resolution_bits);
    ledcAttachPin(motor_in1, motor_in1_channel);
    ledcAttachPin(motor_in2, motor_in2_channel);
    ledcAttachPin(motor_in3, motor_in3_channel);
    ledcAttachPin(motor_in4, motor_in4_channel);

    pinMode(dir_A, 0x01);
    pinMode(dir_B, 0x01);
    attachInterrupt(
        (((interrupt_A)<40)?(interrupt_A):-1),
        ISRA,
        0x01);
    attachInterrupt(
        (((interrupt_B)<40)?(interrupt_B):-1),
        ISRB,
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

        ledcWrite(motor_in3_channel, 255);
        ledcWrite(motor_in4_channel, 0);
    }
    else
    {

        ledcWrite(motor_in1_channel, 0);
        ledcWrite(motor_in2_channel, 255);

        ledcWrite(motor_in3_channel, 0);
        ledcWrite(motor_in4_channel, 255);
    }
    Serial.print(countA);
    Serial.print(",");
    Serial.println(countB);
}
