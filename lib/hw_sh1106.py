'''
Hardware library for an SH1106 OLED.
MicroPython SH1106 OLED driver, I2C interfaces
https://github.com/CrispStrobe/sh1106-py
imports moved to entities
'''

import entities

# SH1106 Commands
SET_CONTRAST = entities.CONST(0x81)
SET_ENTIRE_ON = entities.CONST(0xA4)
SET_NORM_INV = entities.CONST(0xA6)
SET_DISP = entities.CONST(0xAE)
SET_DISP_START_LINE = entities.CONST(0x40)
SET_SEG_REMAP = entities.CONST(0xA0)
SET_MUX_RATIO = entities.CONST(0xA8)
SET_COM_OUT_DIR = entities.CONST(0xC0)
SET_DISP_OFFSET = entities.CONST(0xD3)
SET_COM_PIN_CFG = entities.CONST(0xDA)
SET_DISP_CLK_DIV = entities.CONST(0xD5)
SET_PRECHARGE = entities.CONST(0xD9)
SET_VCOM_DESEL = entities.CONST(0xDB)
SET_CHARGE_PUMP = entities.CONST(0x8D)

# SH1106 specific addressing
SH1106_SET_PAGE_ADDR = entities.CONST(0xB0)
SH1106_SET_LOW_COL = entities.CONST(0x00)
SH1106_SET_HIGH_COL = entities.CONST(0x10)

class Driver_I2C(entities.FRAMEBUF.FrameBuffer):
    '''SH1106 OLED driver for I2C interface'''
    
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.external_vcc = external_vcc
        self.width = width
        self.height = height
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, entities.FRAMEBUF.MONO_VLSB)
        self.init_display()

    def write_cmd(self, cmd):
        '''Write a single command'''
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def write_data(self, buf):
        '''Write data buffer'''
        chunk_size = 32  # I2C buffer limit
        for i in range(0, len(buf), chunk_size):
            chunk = buf[i:i+chunk_size]
            data = bytearray([0x40]) + chunk
            self.i2c.writeto(self.addr, data)

    def init_display(self):
        '''Initialize the SH1106 display'''
        init_commands = [
            SET_DISP | 0x00,          # Display OFF
            SET_DISP_CLK_DIV, 0x80,   # Set clock divide ratio
            SET_MUX_RATIO, self.height - 1,  # Set multiplex ratio
            SET_DISP_OFFSET, 0x00,    # Set display offset
            SET_DISP_START_LINE | 0x00,  # Set start line address
            SET_CHARGE_PUMP, 0x10 if self.external_vcc else 0x14,  # Charge pump
            SET_SEG_REMAP | 0x01,     # Set segment re-map
            SET_COM_OUT_DIR | 0x08,   # Set COM output scan direction
            SET_COM_PIN_CFG, 0x12,    # Set COM pins configuration
            SET_CONTRAST, 0x80,       # Set contrast
            SET_PRECHARGE, 0x22 if self.external_vcc else 0xF1,  # Set pre-charge period
            SET_VCOM_DESEL, 0x40,     # Set VCOMH deselect level
            SET_ENTIRE_ON,            # Resume to RAM content display
            SET_NORM_INV,             # Set normal display
            SET_DISP | 0x01           # Display ON
        ]
        
        for cmd in init_commands:
            self.write_cmd(cmd)
            entities.UTIME.sleep_ms(1)
        
        self.fill(0)
        self.show()

    def show(self):
        '''Update display - SH1106 uses page-by-page addressing'''
        for page in range(self.pages):
            # Set page address
            self.write_cmd(SH1106_SET_PAGE_ADDR | page)
            
            # Set column address (SH1106 has 2-pixel offset for 128px displays)
            col_offset = 2 if self.width == 128 else 0
            self.write_cmd(SH1106_SET_LOW_COL | (col_offset & 0x0F))
            self.write_cmd(SH1106_SET_HIGH_COL | (col_offset >> 4))
            
            # Write page data
            start = page * self.width
            end = start + self.width
            page_data = self.buffer[start:end]
            self.write_data(page_data)

    def poweroff(self):
        '''Turn off the display'''
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        '''Turn on the display'''
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        '''Set display contrast (0-255)'''
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        '''Invert display colors'''
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def rotate(self, rotate):
        '''Rotate display 180 degrees'''
        if rotate:
            self.write_cmd(SET_COM_OUT_DIR)
            self.write_cmd(SET_SEG_REMAP)
        else:
            self.write_cmd(SET_COM_OUT_DIR | 0x08)
            self.write_cmd(SET_SEG_REMAP | 0x01)
