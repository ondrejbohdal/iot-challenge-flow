from network import LoRa
import socket
import time
import binascii
import pycom
from machine import Pin

# Initialize LoRa in LORAWAN mode.
lora = LoRa(mode=LoRa.LORAWAN)

# create an OTAA authentication parameters 70B3D57EF0003A54
app_eui = binascii.unhexlify('70 B3 D5 7E F0 00 3A 54'.replace(' ',''))
app_key = binascii.unhexlify('0B ED 11 C9 03 5D 5C 7B 54 7A D3 C5 ED F4 50 4F'.replace(' ',''))

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(10)
    print('Not yet joined...')

print('Joined')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

#config
hold_time_sec = 0.25

#flags
last_trigger = -10

pir = Pin('G17',mode=Pin.IN,pull=Pin.PULL_UP)

# send the gps coordinates for the device - do this just once 

# main loop
print("Starting detecting presence")
x = 0
while x < 60:
    if pir() == 1:
        if time.time() - last_trigger > hold_time_sec:
            last_trigger = time.time()
            print("Presence detected")
            # make the socket blocking
            # (waits for the data to be sent and for the 2 receive windows to expire)
            s.setblocking(True)

            # send some data
            #s.send(bytes([0x41, 0x42, 0x43]))
            s.send(bytes([1]))

            # make the socket non-blocking
            # (because if there's no data received it will block forever...)
            s.setblocking(False)
             
            data = s.recv(64)
            print(data)
    else:
        last_trigger = 0
        print("No presence")
        # make the socket blocking
        # (waits for the data to be sent and for the 2 receive windows to expire)
        s.setblocking(True)

        # send some data
        #s.send(bytes([0x41, 0x42, 0x43]))
        s.send(bytes([0]))

        # make the socket non-blocking
        # (because if there's no data received it will block forever...)
        s.setblocking(False)
        data = s.recv(64)
        print(data)

    time.sleep_ms(200)
    x += 1

print("Exited main loop")
