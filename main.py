'''
Metropolitan Harbor Railroad
Metropolitan Uniom Transfer Terminal
Layout Lighting Automation
Copyright 2026 Greg Ritacco
'''

import entities
import interface

display0 = entities.interface.Display1(entities.DISPLAY0).getDisplay()
entities.interface.testDisplay(display0)

rotary = interface.Rotary(entities.ROTARY).getRotary() 
entities.ASYNCIO.run(rotary.async_tick())

print('start')
entities.LED.on()

while True:
    try:
        entities.LED.toggle()
        entities.UTIME.sleep(0.5)
    except KeyboardInterrupt:
        entities.LED.off()
        entities.shutDown()
        break
        
print("Finished.")

