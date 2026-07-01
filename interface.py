'''
These are the methods that control the interface
'''

import entities

class Display1() :

    # Everything about the OLED display
    # Tuple items: sda, scl, width, height, addr

    def __init__(self, list):

        self.result = ''
        self.bus = list[0]
        self.sda = list[1]
        self.scl = list[2]
        self.width = list[3]
        self.height = list[4]
        self.addr = list[5]

    def getDisplay(self):

        i2c = entities.I2C(
                        self.bus,
                        sda = entities.PIN(self.sda),
                        scl = entities.PIN(self.scl),
                        freq = 400000
                        )
        
        return entities.SSD1306_I2C(self.width, self.height, i2c, self.addr)
    
    
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
