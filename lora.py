from network import LoRa
import socket
import time
import binascii
import pycom
from pass import secret_codes

# Manages a connection to the Things Network
class LoRaConn:
    def __init__(self):
        colors = {
           'off': 0x000000,
           'red': 0x330000,
           'green': 0x003300,
           'yellow': 0x333300,
           'blue': 0x000033,
           'purple': 0x330033,
           'orange': 0x773300,
           'white': 0x7f7f7f
        }

        # Joining - yellow LED
        pycom.heartbeat(False)
        pycom.rgbled(colors['off'])

        # Initialize LoRa in LORAWAN mode.
        self._lora = LoRa(mode=LoRa.LORAWAN)

        # Find the codes for this device by checking for its MAC in the codes dictionary
        my_codes = secret_codes[self._lora.mac()]

        # Join a network using OTAA (Over the Air Activation)
        self._lora.join(activation=LoRa.OTAA, auth=(my_codes[0], my_codes[1]), timeout=0)
        pycom.rgbled(colors['blue'])

        # Wait until the module has joined the network
        while not self._lora.has_joined():
           time.sleep(5)

        pycom.rgbled(colors['green'])

    # Returns a LoRa socket to send data on
    def socket(self):
        # Create a LoRa socket
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        # Set the LoRaWAN data rate
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        return s
