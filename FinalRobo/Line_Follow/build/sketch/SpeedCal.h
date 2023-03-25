#line 1 "e:\\Project_Archive\\SLRC\\Code\\SLRC_RoboRebels\\Line_Follow\\SpeedCal.h"
#ifndef SPEED_CAL
#define SPEED_CAL

struct SpeedCal
{
    int64_t pre_countA = 0;
    int64_t pre_countB = 0;
    int64_t pre_time = 0;
    float speed_A = 0.0f;
    float speed_B = 0.0f;
    SpeedCal()
    {
        pre_time = millis();
    }

    void update(int64_t countA, int64_t countB)
    {
        if (countA == pre_countA & countB == pre_countB)
        {
            return;
        }
        int64_t dt = millis() - pre_time;
        speed_A = float(countA - pre_countA) / float(dt);
        speed_B = float(countB - pre_countB) / float(dt);
        pre_countA = countA;
        pre_countB = countB;
        pre_time = millis();
    }
};

#endif