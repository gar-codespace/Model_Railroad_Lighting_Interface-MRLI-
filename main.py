'''
Metropolitan Harbor Railroad
Metropolitan Uniom Transfer Terminal
Layout Lighting Automation
Copyright 2026 Greg Ritacco
'''

import entities
import interface
import model
import uasyncio

# both the rotary encoder and selector button
control_interface = interface.Controller(entities.P_ROTARY).get_interface() 
# uasyncio.run(controller.async_tick())

async def blink(delay):
    while True:
        entities.LED.toggle()
        await entities.ASYNCIO.sleep_ms(delay)

async def main():

    uasyncio.create_task(blink(200000000))

    uasyncio.create_task(control_interface.async_tick())

    while True:
        print('l')
        await uasyncio.sleep_ms(1000)


entities.ASYNCIO.run(main())