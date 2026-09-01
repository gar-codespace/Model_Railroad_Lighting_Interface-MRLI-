'''
Model Railroad Lighting Automation
Code to automate control of 5 banks of RGBWC strip led lights
and toggle a scenic lighting bus.
Written to run on a Raspi Pico or Pico 2. WiFi not utilized.
Copyright 2026 Greg Ritacco
'''

__version__ = '20260801.1.1'
__repo__ = 'https://github.com/gar-codespace/Diorama_Lighting_Automation'

import entities
import controls


async def main():

    ui = controls.UserInterface()
    ui.get_main_display()
    ui.update_display(entities.WELCOME_SCREEN)

    while True:
        
        await entities.UASYNCIO.gather(
                                      ui.run_lighting_effect(),
                                      ui.run_sound_effects(),
                                      ui.get_encoder().async_tick(),
                                      ui.get_all_the_buttons(),
                                      )

entities.UASYNCIO.run(main())