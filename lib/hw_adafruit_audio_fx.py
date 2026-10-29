'''
Hardware library for the Adafruit Audio FX Sound Board.
This library is a much less enthusiastic version of:
https://github.com/mmabey/Adafruit_Soundboard_uPy/tree/master

I have taylored it to the specific requirements of my project.
For this project the RX pin on the Pico is optional.
'''

'''
TODO If the UART pin is connected to ground to set the board to uart mode,
reset does not work. Only power cycling
will reset the board when it is in UART mode.
Look into this some more.
'''
'''
board:
SB0 = {
       'BOARD': 'Adafruit Sound FX Board',
       'WAIT':50,
       'DUPLEX':False,
       'RESET':False,
       }
'''

__author__ = 'Greg Ritacco'


import entities


class CMD:

    NUMBER = '#' # Play a file by number
    NAME = 'P' # Play a file by name
    UP = '+' # Volume up
    DOWN = '-' # Volume down
    PAUSE = '='
    UNPAUSE = '>'
    STOP = 'q'
    POSITION = 't' # Give current time of playback and total time of track
    SIZE = 's' # Current track size and total size
    LIST = 'L'


class SoundFX:

    def __init__(self, board:dict, bus:object, reset:entities.PIN=None):

        self.uart = bus
        self.board = board
        self.duplex = board['DUPLEX']
        self.wait = board['WAIT']
        self.reset = reset
    
    def _flush_uart_input(self):
        '''Read any available data from the UART bus until none is left.'''

        if not self.duplex:
            return
        while self.uart.any():
            self.uart.read()

    def _get_reply(self):

        if self.duplex:
            entities.UTIME.sleep_ms(self.wait)
            return self.uart.read()

    def reset_board(self):
        '''TODO Retest this.'''

        if self.reset:
            self.reset.value(0)
            self.reset(entities.PIN.OUT)
            entities.UTIME.sleep_ms(self.wait)
            self.reset(entities.PIN.IN)
            entities.UTIME.sleep_ms(1000)  # Give the board some time to boot

        return self._get_reply()
        
    def _send_simple(self, command):

        self._flush_uart_input()

        self.uart.write(f'{command}\n'.encode('utf-8'))

        return self._get_reply()

    def set_volume(self):

        pass

    def play(self, track=None):

        if isinstance(track, int):
            command = CMD.NUMBER

        if isinstance(track, str):
            command = CMD.NAME

        self._send_simple(f'{command}{track}')

        return self._get_reply()
        
    def play_now(self, track):

        self.stop()
        entities.UTIME.sleep_ms(self.wait)
        self.play(track)          

        return self._get_reply()

    def stop(self):

        self._send_simple(CMD.STOP)
        
        return self._get_reply()
        
# These are untested

    def increment_up(self):

        self._send_simple(CMD.UP)

        return self._get_reply()
        
    def increment_down(self):

        self._send_simple(CMD.DOWN)

        return self._get_reply()
        
    def pause(self):

        self._send_simple(CMD.PAUSE)

        return self._get_reply()
        
    def unpause(self):

        self._send_simple(CMD.UNPAUSE)

        return self._get_reply()
