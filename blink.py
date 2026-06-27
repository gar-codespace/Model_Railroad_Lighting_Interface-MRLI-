from machine import Pin
from utime import sleep

led = Pin(15, Pin.OUT)
led.value(0)

print("LED starts flashing...")
while True:
    try:
        led.toggle()
        sleep(1) # sleep 1sec
        print("Finished.")
    except KeyboardInterrupt:
        break
led.off()

print("Finished.")
