#include <util/atomic.h>

#define LEDR_PIN   3
#define LEDG_PIN   6
#define LEDB_PIN   5

#define RED    0b011
#define GREEN  0b101
#define BLUE   0b110
#define YELLOW 0b001

#define MAINS_PIN   2
#define RELAY_PIN  10

// after this delay, turn red LED on. TODO: notify rpi about it.
#define ZERO_CROSS_TIMEOUT_MS 3000

#define PWM_NR_WAVES 10

static volatile bool zeroCrossing = false;
static unsigned long lastZeroCross;

void setup()
{
    // MAINS_PIN toggles between 1 and 0 every time the Mains voltage passes 0V.
    // if Mains is <=0, MAINS_PIN will read 0. otherwise 1.
    pinMode(MAINS_PIN, INPUT);

    pinMode(LEDR_PIN, OUTPUT);
    pinMode(LEDG_PIN, OUTPUT);
    pinMode(LEDB_PIN, OUTPUT);

    // initialize Relay to 'off' state
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);

    // configure MAINS_PIN as interrupt source, notifying the main loop that we just crossed zero
    attachInterrupt(digitalPinToInterrupt(MAINS_PIN), [](){zeroCrossing=true;}, CHANGE);

    Serial.begin(115200);

    lastZeroCross = millis();
}

static uint8_t pwm = 0;
static uint8_t waveCnt = 0;


void setLeds(uint8_t bitmask)
{
    // analog == pwm, and this is done because apparently I'm too stupid to calculate resistor values for LEDs...
    // ... and 100/255 ~= 40% duty cycle (inverted) looks like a nice yellow, combined with 100% green
    analogWrite(LEDR_PIN, ((bitmask >> 2) & 1) ? 255 : 100);
    digitalWrite(LEDG_PIN, (bitmask >> 1) & 1);
    digitalWrite(LEDB_PIN, (bitmask >> 0) & 1);
}


void loop()
{
    // TODO detect millis() overflow
    bool isPhasePresent = (millis() - lastZeroCross < ZERO_CROSS_TIMEOUT_MS);
    if (isPhasePresent)
    {
        setLeds(pwm == 0 ? GREEN : YELLOW);
    }
    else
    {
        // phase is not connected or the fuse triggered

        // TODO this does only work when absolutely nothing is coupling into the L/N wires...
        // ... which is then triggering 0-cross detection
        pwm = 0;
        setLeds(RED);
    }

    // Check if controller sent something
    if (Serial.available())
    {
        String cmd = Serial.readStringUntil(' ');
        // supported commands: 'PWM xy'
        if (cmd == "PWM")
        {
            // read value (xy)
            int rpiPwm = Serial.readStringUntil('\n').toInt();
            // sanity check
            if (rpiPwm > 100 || rpiPwm < 0 || (rpiPwm % 10 != 0))
            {
                Serial.print("FAIL: No entiendo '" + String(rpiPwm) + "', must be 0, 10, 20, ... 90 or 100\n");
                return;
            }

            waveCnt = 0; // reset wave counter
            pwm = (uint8_t)rpiPwm; // update internal pwm setting and acknowledge command

            Serial.print("SUCCESS: " + String(rpiPwm) + "%\n");
        }
        else
        {
            Serial.print("FAIL: Unknown Command " + cmd + "\n");
            return;
        }
    }

    // access to 'zeroCrossing' variable needs to be atomic because it's also written inside an interrupt routine
    ATOMIC_BLOCK(ATOMIC_RESTORESTATE) // https://forum.arduino.cc/t/demonstration-atomic-access-and-interrupt-routines/73135/2
    {
        if (zeroCrossing)
        {
            lastZeroCross = millis();
            // reset strobe
            zeroCrossing = false;

            // counting waves until we reach the pwm value, then we switch off for the rest of the period (10 half-waves total)
            if (waveCnt*PWM_NR_WAVES >= pwm)
            {
                digitalWrite(RELAY_PIN, LOW);
            }
            else
            {
                digitalWrite(RELAY_PIN, HIGH);
            }
            if (++waveCnt >= 10)
                waveCnt = 0;
        }
    }
    delayMicroseconds(20);
}
