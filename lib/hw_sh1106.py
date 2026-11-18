'''
Model Railroad Lighting Interface (MRLI)

Hardware library for an SH1106 OLED, I2C interface
imports moved to entities

params:
OLED0 = {
        'NAME':'Main Display',
        'MAKE':'GODIYMODULES',
        'MODEL':'White OLED Display Screen',
        'SIZE':'1.3 inch',
        'BUS':'i2c',
        'CONTROLLER':'sh1106',
        'ADDRESS': CONST(0x3C),
        'WIDTH': 128,
        'HEIGHT': 64,
        'ROTATE': False,
        'EXTERNAL_VCC':False,
        }
'''
__author__ = 'https://github.com/CrispStrobe/sh1106-py'

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
    
    def __init__(self, params:dict=None, bus:object=None):
        self.params = params
        self.i2c = bus
        self.addr = params['ADDRESS']
        self.external_vcc = params['EXTERNAL_VCC']
        self.rotate = params['ROTATE']
        self.width = params['WIDTH']
        self.height = params['HEIGHT']
        self.pages = params['HEIGHT'] // 8
        self.buffer = bytearray(self.pages * params['WIDTH'])
        super().__init__(self.buffer, params['WIDTH'], params['HEIGHT'], entities.FRAMEBUF.MONO_VLSB)
        self._init_display()
        print(f'{params['NAME']}: {params['SIZE']}, {params['BUS']}, {params['CONTROLLER']}')

    def _init_display(self):

        init_commands = [
            SET_DISP | 0x00,          # Display OFF
            SET_DISP_CLK_DIV, 0x80,   # Set clock divide ratio
            SET_MUX_RATIO, self.params['WIDTH'] - 1,  # Set multiplex ratio
            SET_DISP_OFFSET, 0x00,    # Set display offset
            SET_DISP_START_LINE | 0x00,  # Set start line address
            SET_CHARGE_PUMP, 0x10 if self.params['EXTERNAL_VCC'] else 0x14,  # Charge pump
            SET_SEG_REMAP | 0x01,     # Set segment re-map
            SET_COM_OUT_DIR | 0x08,   # Set COM output scan direction
            SET_COM_PIN_CFG, 0x12,    # Set COM pins configuration
            SET_CONTRAST, 0x80,       # Set contrast
            SET_PRECHARGE, 0x22 if self.params['EXTERNAL_VCC'] else 0xF1,  # Set pre-charge period
            SET_VCOM_DESEL, 0x40,     # Set VCOMH deselect level
            SET_ENTIRE_ON,            # Resume to RAM content display
            SET_NORM_INV,             # Set normal display
            SET_DISP | 0x01           # Display ON
        ]
        
        for cmd in init_commands:
            self._write_cmd(cmd)
            entities.UTIME.sleep_ms(1)

        self.fill(0)
        self.show()

    def _write_cmd(self, cmd):
        '''Write a single command'''
        self.i2c.writeto(self.addr, bytearray([0x80, cmd]))

    def _write_data(self, buf):
        '''Write data buffer'''
        chunk_size = 32  # I2C buffer limit
        for i in range(0, len(buf), chunk_size):
            chunk = buf[i:i+chunk_size]
            data = bytearray([0x40]) + chunk
            self.i2c.writeto(self.addr, data)

    def show(self):
        '''Update display - SH1106 uses page-by-page addressing'''
        for page in range(self.pages):
            # Set page address
            self._write_cmd(SH1106_SET_PAGE_ADDR | page)
            
            # Set column address (SH1106 has 2-pixel offset for 128px displays)
            col_offset = 2 if self.width == 128 else 0
            self._write_cmd(SH1106_SET_LOW_COL | (col_offset & 0x0F))
            self._write_cmd(SH1106_SET_HIGH_COL | (col_offset >> 4))
            
            # Write page data
            start = page * self.width
            end = start + self.width
            page_data = self.buffer[start:end]
            self._write_data(page_data)

    def poweroff(self):
        '''Turn off the display'''
        self._write_cmd(SET_DISP | 0x00)

    def poweron(self):
        '''Turn on the display'''
        self._write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        '''Set display contrast (0-255)'''
        self._write_cmd(SET_CONTRAST)
        self._write_cmd(contrast)

    def invert(self, invert:bool):
        '''Invert display colors'''
        self._write_cmd(SET_NORM_INV | (invert & 1))

    def rotate_disp(self):
        '''Rotate display 180 degrees'''
        if self.rotate:
            self._write_cmd(SET_COM_OUT_DIR)
            self._write_cmd(SET_SEG_REMAP)
            self.rotate = False
            return

        self._write_cmd(SET_COM_OUT_DIR | 0x08)
        self._write_cmd(SET_SEG_REMAP | 0x01)
        self.rotate = True
