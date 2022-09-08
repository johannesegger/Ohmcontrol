#!/usr/bin/env python3

import logging
import requests
from threading import Event
import RPi.GPIO as GPIO
import signal
import sys
from fn import update_state, state_to_string

if len(sys.argv) < 2:
    sys.exit("Usage: python3 app.py <inverter-host-name>")

host_name = sys.argv[1]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

on_off_relay_pin_numbers = [17, 27]
# pwm_relay_pin_number = 22

GPIO.setmode(GPIO.BCM)
for pin_number in on_off_relay_pin_numbers:
    GPIO.setup(pin_number, GPIO.OUT, initial = GPIO.LOW)

quitEvent = Event()

def quit(_signo, _frame):
    quitEvent.set()

signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)

state = 0

try:
    while not quitEvent.is_set():
        response = requests.get(f'http://{host_name}/solar_api/v1/GetPowerFlowRealtimeData.fcgi')
        watt_to_grid = float(response.json()['Body']['Data']['Site']['P_Grid']) * -1
        new_state = update_state(state, watt_to_grid)
        logger.info(f"Power to grid: {watt_to_grid}W - Actual State: {state_to_string(state)} - Desired state: {state_to_string(new_state)}")
        for (index, pin_number) in enumerate(on_off_relay_pin_numbers):
            actual_state = (state >> index) & 0b1 != 0
            desired_state = (new_state >> index) & 0b1 != 0
            if actual_state != desired_state:
                logger.info(f"  Set pin #{pin_number} to {desired_state}")
                GPIO.output(pin_number, desired_state)
        state = new_state
        quitEvent.wait(60)
finally:
    GPIO.cleanup()
