#ifndef ENCODER_HELPER
#define ENCODER_HELPER

volatile int64_t countA = 0;
volatile int64_t countB = 0;

const uint8_t encoderA = 2;
const uint8_t encoderB = 3;

const uint8_t dirpinA = 4;
const uint8_t dirpinB = 5;

void ISRA()
{
    if (digitalRead(dirpinA) == HIGH)
    {
        countA++;
        return;
    }
    countA--;
}

void ISRB()
{
    if (digitalRead(dirpinB) == HIGH)
    {
        countB++;
        return;
    }
    countB--;
}
#endif