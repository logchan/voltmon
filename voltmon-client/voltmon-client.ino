#define N_PINS 6
int pin_ids[N_PINS] = { 3, 5, 6, 9, 10, 11 };
#define LERP_TIME 2000.0f

struct pin_data
{
    int start_value = 0;
    int current_value = 0;
    int target_value = 0;
    unsigned long start_time = 0;
};

pin_data pins[N_PINS];
byte cmd[8];

void setup() {
    Serial.begin(9600);
}

void update_value() {
    for (int i = 0; i < N_PINS; ++i) {
        pin_data* pin = &pins[i];

        if (pin->current_value == pin->target_value) {
            continue;
        }

        float t = constrain((millis() - pin->start_time) / LERP_TIME, 0, 1);
        pin->current_value = (int)((pin->target_value - pin->start_value) * t + pin->start_value);
        analogWrite(pin_ids[i], pin->current_value);
        delay(50);
    }
}

void set_target(int i, int v) {
    if (i < 0 || i >= N_PINS || v < 0 || v > 255) {
        return;
    }

    pin_data* pin = &pins[i];
    pin->target_value = v;
    pin->start_value = pin->current_value;
    pin->start_time = millis();
}

void read_input() {
    if (!Serial.available()) {
        return;
    }

    size_t read = Serial.readBytes(cmd, 8);
    if (read != 8) {
        return;
    }

    if (cmd[0] != 0x22 || cmd[1] != 0x33) {
        return;
    }

    switch (cmd[2])
    {
    case 0x01:
        set_target(cmd[3], cmd[4]);
        break;
    
    default:
        break;
    }
}

void loop() {
    update_value();
    read_input();
}
