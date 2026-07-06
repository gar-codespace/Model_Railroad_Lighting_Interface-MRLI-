'''
Metropolitan Harbor Railroad
Metropolitan Uniom Transfer Terminal
Layout Lighting Automation
Copyright 2026 Greg Ritacco
'''

import entities
import interface

# both the rotary encoder and selector button
control_interface = interface.Controller(entities.P_ROTARY).get_interface()

async def run_routine(delay):
    while True:
        entities.LED.toggle()
        await entities.ASYNCIO.sleep_ms(delay)

async def main():

    entities.ASYNCIO.create_task(run_routine(200))

    entities.ASYNCIO.create_task(control_interface.async_tick())

    while True:
        print(entities.CURRENT_ROUTINE)
        await entities.ASYNCIO.sleep_ms(1000)


entities.ASYNCIO.run(main())