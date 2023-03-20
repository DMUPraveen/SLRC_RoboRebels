

const size_t MAX_FUNCTIONS = 10;
const size_t MAX_BUFFER = 20;

struct Data
{
    float Kp = 0.5f;
    float Ki = 0.0f;
    float Kd = 0.0f;
    float set_point = 0.0f;

    void update(void *buffer)
    {
        float *buf = (float *)buffer;
        Kp = buf[0];
        Ki = buf[1];
        Kd = buf[2];
        set_point = buf[3];
    }
};

struct Communicator
{
    uint8_t m_buffer[MAX_BUFFER];

    void (*m_functions[MAX_FUNCTIONS])(void *buffer);

    void communicate()
    {
        if (!Serial.available())
        {
            return;
        }
        uint8_t instruction = Serial.read();
        uint8_t size = Serial.read();
        if (size != 0)
        {
            Serial.readBytes(m_buffer, size);
        }
        m_functions[instruction](m_buffer);
        while (Serial.available())
        {
            Serial.read();
        }
    }
};
Data d;
Communicator com;
uint8_t state = LOW;
void update_data(void *buffer)
{
    d.update(buffer);
}
void toggle_led(void *buffer)
{
    state = !state;
    digitalWrite(LED_BUILTIN, state);
}
void setup()
{
    Serial.begin(9600);
    delay(5000);
    com.m_functions[0] = update_data;
}

void loop()
{

    com.communicate();
    Serial.print("Kp: ");
    Serial.print(d.Kp);
    Serial.print(",");
    Serial.print("Ki: ");
    Serial.print(d.Ki);
    Serial.print(",");
    Serial.print("Kd: ");
    Serial.print(d.Kd);
    Serial.print(",");
    Serial.print("set_point: ");
    Serial.print(d.set_point);
    Serial.println();
}
