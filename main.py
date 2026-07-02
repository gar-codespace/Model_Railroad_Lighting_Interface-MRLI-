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

# both the rotary encoder and selector button
rotary = interface.Rotary(entities.ROTARY).getRotary() 
entities.ASYNCIO.run(rotary.async_tick())


