'''
Model Railroad Lighting Automation
Code to automate control of 5 banks of RGBWC strip lights
and toggle a scenic lighting bus.
Written to run on a Raspi Pico 2. WiFi not utilized.
Copyright 2026 Greg Ritacco
'''
__author__ = 'Greg Ritacco'
__version__ = '20261001.1.1'
__repo__ = 'https://github.com/gar-codespace/Diorama_Lighting_Automation'


import entities
import machine


async def main():

    mech = machine.Controller()
    mech.boot()

    while True:
        
        await entities.UASYNCIO.gather(
                                      mech.run_lighting_effect(),
                                      mech.play_ambient_effects(),
                                      mech.poll_the_inputs(),
                                      )

entities.UASYNCIO.run(main())
