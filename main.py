'''
Model Railroad Lighting Interface (MRLI)
Code to control of 5 banks of RGBWC strip lights & toggle a scenic lighting bus.
Includes sound effects.
Includes visual effects.
Written to run on a Raspi Pico 2. WiFi not utilized.
Copyright 2026 Greg Ritacco
'''
__author__ = 'Greg Ritacco'
__repo__ = 'https://github.com/gar-codespace/Diorama_Lighting_Automation'


import entities
import controller


async def main():

    mrli = controller.Mech()
    mrli.boot()

    while True:
        
        await entities.UASYNCIO.gather(
                                      mrli.run_lighting_effect(),
                                      mrli.play_ambient_effects(),
                                      mrli.poll_the_controls(),
                                      )

entities.UASYNCIO.run(main())
