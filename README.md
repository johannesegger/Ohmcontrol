# Ohmcontrol

DIY replacement for Fronius Ohmpilot.

## Hardware

* Raspberry Pi
  * Tested with a RPi 3 Model B+, but it should work with any model that can run a Python script.
* 3 x SSR Relay + Radiator
  * It should be activated with 3V3 (*load voltage*) as this is what RPi gives us.
* 6 x M-F Jumper Breadboard Wire
  * To connect the RPi with the Relays. 

## Setup

### Hardware

```
   Separate phase       Separate phase
     from grid            to Ohmpilot

          │                   │
          │                   │
       ┌──┴───────────────────┴──┐
       │                         │
       │ Load               Load │
       │                         │
       │                         │
3 X    │          Relay          │
       │                         │
       │                         │
       │ Control -     Control + │
       │                         │
       └───┬────────────────┬────┘
           │                │
           │                │

        RPi GND         GPIO pin
                        17/27/22
```

> Created with [asciiflow](https://asciiflow.com).

### Software

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
