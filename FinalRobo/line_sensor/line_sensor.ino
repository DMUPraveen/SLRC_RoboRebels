const uint8_t NUM_SENSORS = 7;
uint8_t analog_pins[NUM_SENSORS] = {A0, A1, A2, A3, A4, A5, A6};
uint8_t out_pins[NUM_SENSORS] = {4, 5, 6, 7, 8, 9, 10};

const int batch = 20;
const int iterations = 1000;
const int delta = 2;

const float MAX_VALUE = 1000.0f;
struct calibrator
{
    float max_values[NUM_SENSORS] = {-1.0f};
    float min_values[NUM_SENSORS] = {MAX_VALUE};
    float threshold_values[NUM_SENSORS] = {0.0f};
    calibrator()
    {
    }
    void calibrate(int64_t iterations, int64_t batch, int delta)
    {
        for (int64_t i = 0; i < iterations; i++)
        {
            delay(delta);
            float readins[NUM_SENSORS] = {0.0f};
            for (int64_t j = 0; j < batch; j++)
            {
                for (int64_t k = 0; k < NUM_SENSORS; k++)
                {
                    readins[k] += analogRead(analog_pins[k]);
                }
            }
            for (int64_t k = 0; k < NUM_SENSORS; k++)
            {
                readins[k] /= batch;
            }
            for (int64_t k = 0; k < NUM_SENSORS; k++)
            {
                max_values[k] = max(max_values[k], readins[k]);
                min_values[k] = min(max_values[k], readins[k]);
            }
        }

        for (int64_t k = 0; k < NUM_SENSORS; k++)
        {
            threshold_values[k] = (max_values[k] + min_values[k]) / 2;
        }
    }

    void show()
    {
        for (int i = 0; i < NUM_SENSORS; i++)
        {
            digitalWrite(
                out_pins[i],
                analogRead(analog_pins[i]) < threshold_values[i]);
        }
    }
};

calibrator cal = calibrator();

void setup()
{
    for (auto pin : analog_pins)
    {
        pinMode(pin, INPUT);
    }
    for (auto pin : out_pins)
    {
        pinMode(pin, OUTPUT);
    }
    for (auto pin : out_pins)
    {
        digitalWrite(pin, LOW);
    }
    delay(1000);
    pinMode(LED_BUILTIN, HIGH);
    cal.calibrate(iterations, batch, delta);
    pinMode(LED_BUILTIN, LOW);
}

void loop()
{
    cal.show();
}
