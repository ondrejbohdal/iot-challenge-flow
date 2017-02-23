#This sensor has 4 pins, VCC, GND, TRIGGER and ECHO.
#Connect:
#- VCC to VIN on the expansion board. (This only works well when the sensor is powered by 5V, so power the expansion board from the USB port).
#- GND to GND on the expansion board.
#- TRIGGER to any output pin on the LoPy (e.g. P11).
#- ECHO to any input pin on the LoPy (e.g. P12), via a resistor divider. Use for instance a 10K and a 20K resistor divider to take the 5V output of the sensor to a safe 3V3 for the LoPy.

import time
import machine
from ring import Ring

class DistanceSensorComm:
    def __init__(self, trigger, echo):
        self._trigger = machine.Pin(trigger, mode=machine.Pin.OUT, value=0)
        self._echo = machine.Pin(echo, mode=machine.Pin.IN)

    # This _does_ return erroneous values over 400 cm
    # They can be cut off while reading the data
    def distance(self):
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
        dt = t2 - t1

        # Calculate distance in centimeters. The constants are found
        # in the datasheet, and calculated from the assumed speed 
        # of sound in air at sea level (~340 m/s).
        cm = float(dt / 58.0)

        return cm
