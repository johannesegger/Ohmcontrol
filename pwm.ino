#include <util/atomic.h>

#define LED_PIN    13
#define MAINS_PIN   2
#define RELAY_PIN  10

#define PWM_NR_WAVES 10

static volatile bool zeroCrossing = false;

void setup()
{
    // MAINS_PIN toggles between 1 and 0 every time the Mains voltage passes 0V.
    // if Mains is <=0, MAINS_PIN will read 0. otherwise 1.
    pinMode(MAINS_PIN, INPUT);

    // pinMode(LED_PIN, OUTPUT);

    // initialize Relay to 'off' state
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);

    // configure MAINS_PIN as interrupt source, notifying the main loop that we just crossed zero
    attachInterrupt(digitalPinToInterrupt(MAINS_PIN), [](){zeroCrossing=true;}, CHANGE);

    Serial.begin(115200);
}

static uint8_t pwm = 0;
static uint8_t waveCnt = 0;

void loop()
{

    // Check if controller sent something
    if (Serial.available())
    {
        String cmd = Serial.readStringUntil(' ');
        // supported commands: 'PWM xy'
        if (cmd == "PWM")
        {
            // read value (xy)
            int rpiInput = Serial.readStringUntil('\n').toInt();
            // sanity check
            if (rpiInput > 100 || rpiInput < 0 || (rpiInput % 10 != 0))
            {
                Serial.print("FAIL: No entiendo '" + String(rpiInput) + "', must be 0, 10, 20, ... 90 or 100\n");
                return;
            }
            // update internal pwm setting and acknowledge command
            pwm = (uint8_t)rpiInput;
            Serial.print("SUCCESS: " + String(rpiInput) + "%\n");
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
            if (++waveCnt == 10)
                waveCnt = 0;
        }
    }
    delayMicroseconds(20);
}
