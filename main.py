'''
Model Railroad Lighting Automation
Code to automate control of 5 banks of RGBWC strip led lights
and toggle a scenic lighting bus.
Written to run on a Raspi Pico or Pico 2. WiFi not utilized.
Copyright 2026 Greg Ritacco
'''


import entities
import controller


async def main():

    mech = controller.Machine()
    mech.boot()

    while True:
        
        await entities.UASYNCIO.gather(
                                      mech.run_lighting_effect(),
                                      mech.play_ambient_sounds(),
                                      mech.get_encoder().async_tick(),
                                      )

entities.UASYNCIO.run(main())