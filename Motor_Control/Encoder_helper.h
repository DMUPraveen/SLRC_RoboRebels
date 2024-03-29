#ifndef ENCODER_HELPER
#define ENCODER_HELPER

volatile int64_t countA = 0;
volatile int64_t countB = 0;

const uint8_t encoderA = 2;
const uint8_t encoderB = 3;

const uint8_t dirpinA = 4;
const uint8_t dirpinB = 5;

void IRAM_ATTR ISRA()
{
    if (digitalRead(dirpinA) == HIGH)
    {
        countA++;
        return;
    }
    countA--;
}

void IRAM_ATTR ISRB()
{
    if (digitalRead(dirpinB) == HIGH)
    {
        countB++;
        return;
    }
    countB--;
}

void setup_encoders_with_interrupts()
{
    attachInterrupt(encoderA, ISRA, RISING);
    attachInterrupt(encoderB, ISRB, RISING);
    pinMode(dirpinA, INPUT);
    pinMode(dirpinB, INPUT);
}
#endif
