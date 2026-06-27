from machine import Pin
from utime import sleep

led = Pin(15, Pin.OUT)
check = Pin("LED", Pin.OUT)
led.value(0)

print("LED starts flashing...")
while True:
    try:
        led.toggle()
        check.toggle()
        sleep(0.5) # sleep 1sec
    except KeyboardInterrupt:
        break
led.off()
check.off()

print("Finished.")
