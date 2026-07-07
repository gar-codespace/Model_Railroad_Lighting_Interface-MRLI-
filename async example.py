import entities
import model
import interface

import machine
import uasyncio
import utime
import queue

# Settings
# btn = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_UP)


        
# Coroutine: only return on button press
# async def wait_button():
#     btn_prev = btn.value()
#     while (btn.value() == 1) or (btn.value() == btn_prev):
#         btn_prev = btn.value()
#         await uasyncio.sleep(0.04)
        
# Coroutine: entry point for asyncio program
async def main():
    # the display, the rotary encoder and selector button
    
    # Queue for passing messages
    q = queue.Queue()

    control_interface = interface.Controller(entities.P_ROTARY, q).get_interface()
    
    uasyncio.create_task(model.run_routine(q))
    
    while True:
        
        await control_interface.async_tick()

    
# Start event loop and run entry point coroutine
uasyncio.run(main())