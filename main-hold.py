"""
MUTT Layout Lighting Automation (LLA)
Copyright 2026 Greg Ritacco
No restrictions on use, but I would appreciate the reference.
"""


import entities
# import ssd1306

# functions
SLEEP = entities.SLEEP
PIN = entities.PIN

# constants
SCRIPT_NAME = 'main'
SCRIPT_REV = '20260626'
LED = entities.LED

entities.Initialize().initializeAll()





print("Testing...")




while True:
    try:
        LED.toggle()
        entities.testSwitches()
        entities.SLEEP(0.5)
    except KeyboardInterrupt:
        LED.off()
        entities.shutDown()
        break
        

print("Finished.")
