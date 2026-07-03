'''
Metropolitan Harbor Railroad
Metropolitan Uniom Transfer Terminal
Layout Lighting Automation
Copyright 2026 Greg Ritacco
'''

import entities
import interface

# both the rotary encoder and selector button
rotary = interface.Rotary(entities.P_ROTARY).getRotary() 
entities.ASYNCIO.run(rotary.async_tick())
