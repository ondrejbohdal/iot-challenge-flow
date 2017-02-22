#This sensor has 4 pins, VCC, GND, TRIGGER and ECHO.
#Connect:
#- VCC to VIN on the expansion board. (This only works well when the sensor is powered by 5V, so power the expansion board from the USB port).
#- GND to GND on the expansion board.
#- TRIGGER to any output pin on the LoPy (e.g. P11).
#- ECHO to any input pin on the LoPy (e.g. P12), via a resistor divider. Use for instance a 10K and a 20K resistor divider to take the 5V output of the sensor to a safe 3V3 for the LoPy.

from machine import Pin
import time
import machine
import array
import gc
import math

class Ring:
    def __init__(self, size):
        self._array = array.array('f', [0]*size)
        self._size = size
        self._i = 0

    def push(self, val):
        self._array[self._i] = val
        self._i = (self._i+1) % self._size

    def last(self):
        return self._array[(self._i-1) % self._size]

# Anything over 400 cm (23200 us pulse) is "out of range"
MAX_TIME = const(23200)
class DistanceSensorComm:
    def __init__(self, trigger, echo):
        self._trigger = Pin(trigger, mode=Pin.OUT, value=0)
        self._echo = Pin(echo, mode=Pin.IN)

    def distance(self):
        # Turn off GC for critical section
        gc.disable()

        # Hold the trigger pin high for at least 10 us
        # TODO Can we get higher resolution?
        self._trigger(1)
        time.sleep_us(11)
        self._trigger(0)

        # Wait for pulse on echo pin
        while not self._echo():
            # Undocumented..
            machine.idle()

        # Measure how long the echo pin was held high (pulse width)
        # Note: the us counter will overflow after ~70 min
        t1 = time.ticks_us()
        while self._echo():
            pass
        t2 = time.ticks_us()

        # TODO maybe just disable for entire time and don't alloc?
        gc.enable()

        dt = t2 - t1

        # Calculate distance in centimeters. The constants are found
        # in the datasheet, and calculated from the assumed speed 
        # of sound in air at sea level (~340 m/s).
        cm = dt / 58.0;

        if dt > MAX_TIME:
            return None
        else:
            return cm


comm = DistanceSensorComm('P10', 'P9')
r = Ring(512)

while True:
    time.sleep(0.05)
    d = comm.distance()
    last = r.last()
    if d:
        r.push(d)

    dd = math.pow(last-d, 2)
    print(dd)
