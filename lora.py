from network import LoRa
import socket
import time
import binascii
import pycom

" Manages a connection to the Things Network "
class LoRaConn:
    def __init__(self):
        colors = {
            off: 0x000000,
            red: 0x330000,
            green: 0x003300,
            yellow: 0x333300,
            blue: 0x000033,
            purple: 0x330033,
            orange: 0x773300,
            white: 0x7f7f7f,
        }

        # Joining - yellow LED
        pycom.heartbeat(False)
        pycom.rgbled(colors[off])

        # Initialize LoRa in LORAWAN mode.
        self._lora = LoRa(mode=LoRa.LORAWAN)

        # The codes required to connect to IoT
        # format: MAC (DevEUI): (AppEUI, AppKey, DevID)
        secret_codes = {
            binascii.unhexlify('70B3D549967490A5'): (binascii.unhexlify('70B3D57EF0003A54'), binascii.unhexlify('0BED11C9035D5C7B547AD3C5EDF4504F'), 'teamb1'),
            binascii.unhexlify('70B3D5499A855818'): (binascii.unhexlify('70B3D57EF0003A54'), binascii.unhexlify('6ABB6090FC44A70816A5D61117EFAD22'), 'teamb2'),
            binascii.unhexlify('70B3D54996759D75'): (binascii.unhexlify('70B3D57EF0003A54'), binascii.unhexlify('0D382D0FED63ACB965560A1FB2D39D54'), 'teamb3'),
        }

        # Find the codes for this device by checking for its MAC in the codes dictionary
        my_codes = secret_codes[lora.mac()]

        # Join a network using OTAA (Over the Air Activation)
        lora.join(activation=LoRa.OTAA, auth=(my_codes[0], my_codes[1]), timeout=0)
        pycom.rgbled(colors[blue])

        # Wait until the module has joined the network
        while not lora.has_joined():
           time.sleep(10)

        pycom.rgbled(colors[green])

    " Returns a LoRa socket to send data on "
    def socket(self):
        # Create a LoRa socket
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        # Set the LoRaWAN data rate
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        return s
