'''
These are the methods that control the interface
'''

import entities

class Display() :

    # Everything about the OLED display

    def __init__(self):

        self.result = ''

        return

    def display(self):

        i2c = entities.I2C(0,
                        sda = entities.PIN(entities.OLED['sda']),
                        scl = entities.PIN(entities.OLED['scl']),
                        freq = 400000
                        )
        
        return entities.SSD1306_I2C(entities.OLED_WIDTH, entities.OLED_HEIGHT, i2c)
    
    
def testDisplay(display):

    display.fill(0)
    j = 0

    for i in range(entities.DISPLAY_ROWS):
        display.text(entities.DISPLAY_TEST_MESSAGE, 0, j)
        display.show()
        entities.SLEEP(.2)
        display.fill(0)
        j += entities.DISPLAY_LINE_HEIGHT

    entities.SLEEP(.2)
    display.text(entities.MESSAGES[1], 0, 0)
    display.show()
    return
