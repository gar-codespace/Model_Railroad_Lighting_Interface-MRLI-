from machine import Pin
from time import sleep

myButton = Pin(18, Pin.IN)

while True:
    print(myButton.value())
    sleep(.1)