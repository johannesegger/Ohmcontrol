import serial

__serial = None

rpiPort = '/dev/ttyS0'
pcPort = '/dev/ttyUSB0'

def init(port=rpiPort, baudRate=115200):
    global __serial
    __serial = serial.Serial(port=port, baudrate=baudRate, timeout=1)

def set(pwm : int = 0):
    global __serial
    val = f'PWM {pwm}\n'.encode('utf-8')

    __serial.write(val)

    response = __serial.readline().decode('utf-8').replace('\n', '')

    if response.startswith('SUCCESS:'): # very basic protocol :-)
        return ''

    return response
