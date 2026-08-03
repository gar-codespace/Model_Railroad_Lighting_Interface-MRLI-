'''
Model Railroad Lighting Automation
Code to automate control of 5 banks of RGBWC strip layout lights
and toggle a scenic lighting bus.
Written to run on a Raspi Pico or Pico 2. WiFi not utilized.
Copyright 2026 Greg Ritacco
'''

__version__ = '20260801.1.1'
__repo__ = 'https://github.com/gar-codespace/Model_Railroad_Lighting_Automation'

import entities
import controls

async def main():

    ui = controls.UserInterface()
    ui.get_main_display()
    ui.show_welcome_screen()
    
    # controls.play harbor sounds

    while True:
        
        await entities.ASYNCIO.gather(ui.get_encoder().async_tick(),
                                      ui.get_confirm_button(),
                                      # ui.get_back_button(),
                                      ui.get_led_bank_buttons(),
                                      )

entities.ASYNCIO.run(main())