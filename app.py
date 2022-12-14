#!/usr/bin/env python3

import logging
import requests
from threading import Event
import RPi.GPIO as GPIO
import signal
import sys

def update_state(state, watt_to_grid):
    if watt_to_grid >= 9000:
        return 0b111
    if watt_to_grid >= 6000:
        return (state << 2 | 0b11) & 0b111
    if watt_to_grid >= 3000:
        return (state << 1 | 0b1) & 0b111
    if watt_to_grid >= 0:
        return state
    if watt_to_grid >= -3000:
        return state >> 1
    if watt_to_grid >= -6000:
        return state >> 2
    else:
        return 0

# def test_update_state(state, watt_to_grid, expected_state):
#     actual_state = update_state(state, watt_to_grid)
#     if actual_state == expected_state:
#         print(f"update_state({bin(state)}, {watt_to_grid}) = {bin(actual_state)}")
#     else:
#         print(f"ERROR: update_state({bin(state)}, {watt_to_grid}) = {bin(actual_state)}, but should be {bin(expected_state)}")

# test_update_state(0b000, -10000, 0b000)
# test_update_state(0b000, -8000, 0b000)
# test_update_state(0b000, -5000, 0b000)
# test_update_state(0b000, -2000, 0b000)
# test_update_state(0b000, 0, 0b000)
# test_update_state(0b000, 2000, 0b000)
# test_update_state(0b000, 5000, 0b001)
# test_update_state(0b000, 8000, 0b011)
# test_update_state(0b000, 10000, 0b111)

# test_update_state(0b001, -10000, 0b000)
# test_update_state(0b001, -8000, 0b000)
# test_update_state(0b001, -5000, 0b000)
# test_update_state(0b001, -2000, 0b000)
# test_update_state(0b001, 0, 0b001)
# test_update_state(0b001, 2000, 0b001)
# test_update_state(0b001, 5000, 0b011)
# test_update_state(0b001, 8000, 0b111)
# test_update_state(0b001, 10000, 0b111)

# test_update_state(0b011, -10000, 0b000)
# test_update_state(0b011, -8000, 0b000)
# test_update_state(0b011, -5000, 0b000)
# test_update_state(0b011, -2000, 0b001)
# test_update_state(0b011, 0, 0b011)
# test_update_state(0b011, 2000, 0b011)
# test_update_state(0b011, 5000, 0b111)
# test_update_state(0b011, 8000, 0b111)
# test_update_state(0b011, 10000, 0b111)

# test_update_state(0b111, -10000, 0b000)
# test_update_state(0b111, -8000, 0b000)
# test_update_state(0b111, -5000, 0b001)
# test_update_state(0b111, -2000, 0b011)
# test_update_state(0b111, 0, 0b111)
# test_update_state(0b111, 2000, 0b111)
# test_update_state(0b111, 5000, 0b111)
# test_update_state(0b111, 8000, 0b111)
# test_update_state(0b111, 10000, 0b111)

if len(sys.argv) < 2:
    sys.exit("Usage: python3 app.py <inverter-host-name>")

host_name = sys.argv[1]

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

pin_numbers = [17, 27, 22]

GPIO.setmode(GPIO.BCM)
for pin_number in pin_numbers:
    GPIO.setup(pin_number, GPIO.OUT, initial = GPIO.LOW)

quitEvent = Event()

def quit(_signo, _frame):
    quitEvent.set()

signal.signal(signal.SIGINT, quit)
signal.signal(signal.SIGTERM, quit)

state = 0

def state_to_string(state):
    if state == 0b000: return "0 phases"
    elif state == 0b001: return "1 phase"
    elif state == 0b011: return "2 phases"
    elif state == 0b111: return "3 phases"
    return f"{bin(state)} (invalid)"

try:
    while not quitEvent.is_set():
        response = requests.get(f'http://{host_name}/solar_api/v1/GetPowerFlowRealtimeData.fcgi')
        watt_to_grid = float(response.json()['Body']['Data']['Site']['P_Grid']) * -1
        new_state = update_state(state, watt_to_grid)
        logger.info(f"Power to grid: {watt_to_grid}W - Actual State: {state_to_string(state)} - Desired state: {state_to_string(new_state)}")
        for (index, pin_number) in enumerate(pin_numbers):
            actual_state = (state >> index) & 0b1 != 0
            desired_state = (new_state >> index) & 0b1 != 0
            if actual_state != desired_state:
                logger.info(f"  Set pin #{pin_number} to {desired_state}")
                GPIO.output(pin_number, desired_state)
        state = new_state
        quitEvent.wait(60)
finally:
    GPIO.cleanup()
