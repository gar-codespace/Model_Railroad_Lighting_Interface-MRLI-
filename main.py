'''
Model Railroad Lighting Automation
Code to automate control of 5 banks of RGBWC strip led lights
and toggle a scenic lighting bus.
Written to run on a Raspi Pico or Pico 2. WiFi not utilized.
Copyright 2026 Greg Ritacco
'''


import entities
import controls


async def main():

    ui = controls.UserInterface()

    while True:
        
        await entities.UASYNCIO.gather(
                                      ui.run_lighting_effect(),
                                      ui.play_ambient_sounds(),
                                      ui.get_encoder().async_tick(),
                                      )

entities.UASYNCIO.run(main())