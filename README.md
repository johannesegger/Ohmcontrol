# Ohmcontrol

DIY replacement for Fronius Ohmpilot.

> Warning: Don't do this on your own if you're a software-only guy like me. Get professional help from someone who understands electronic shizzle (thank you, [Stefan, my dear brother](https://github.com/bananenbaer)).

## Hardware

* Raspberry Pi
  * Tested with a RPi 3 Model B+, but it should work with any model that can run a Python script.
* Arduino Nano
* 3 x SSR Relay + Radiator
  * It should be activated with 3V3 (*load voltage*) as this is what RPi gives us.
* 6 x M-F Jumper Breadboard Wire
  * To connect RPI/Arduino with the Relays.
* Status LED
* Resistors

### Setup

* Connect RPi GPIO pins 16 and 26 each to a relay (Control +).
  * Those two relays are either on or off.
* Connect RPi GND pins (any) each to a relay (Control -).
* Connect Arduino digital pin D10 to the third relay (Control +).
  * This relay will simulate PWM by turning it off for some half-waves.
* Connect Arduino GND pin (any) to the third relay (Control -).
* Connect RPi UART TX/RX (GPIO 14/15) pins to Arduino serial pins (RX1/TX0).
* Connect phase to Arduino D2 (use resistors to reduce voltage down to 3.3V)
  * This is necessary to detect zero-crossing of voltage for switching PWM relay state.
  * Zero-cross-detection works best when no other devices use that phase.
* Connect Arduino A3 (R), D5 (G) and D6 (B) to status LED.

```
   Separate phase       Separate phase
     from grid            to Ohmpilot
          │                   │
       ┌──┴───────────────────┴──┐
       │ Load               Load │
2 X    │          Relay          │
       │ Control -     Control + │
       └───┬────────────────┬────┘
           │                │
        RPi GND     RPi GPIO pin 16/26
```

```
   Separate phase       Separate phase
     from grid            to Ohmpilot
          │                   │
       ┌──┴───────────────────┴──┐
       │ Load               Load │
1 X    │          Relay          │
       │ Control -     Control + │
       └───┬────────────────┬────┘
           │                │
      Arduino GND  Arduino pin D10
```

## Software

* Flash SD card e.g. using [Raspberry Pi Imager](https://www.raspberrypi.com/software/).
  * Set all necessary settings so that you can connect to your RPi after it starts up.
* Connect to your RPi e.g. using [Visual Studio Code](https://code.visualstudio.com/docs/remote/ssh).
* Run the following commands to clone the repository and install Ohmcontrol as service:
    ```bash
    sudo apt update && apt install -y git
    git clone https://github.com/johannesegger/Ohmcontrol
    cd Ohmcontrol
    ./setup.sh
    ```
* Check logs
    ```bash
    journalctl -u ohmcontrol -r
    ```
