'''
Metropolitan Harbor Railroad
Metropolitan Uniom Transfer Terminal
Layout Lighting Automation
Copyright 2026 Greg Ritacco
'''

import entities
import interface

# both the rotary encoder and selector button
controller = interface.Controller(entities.P_ROTARY).getRotary() 
entities.ASYNCIO.run(controller.async_tick())
