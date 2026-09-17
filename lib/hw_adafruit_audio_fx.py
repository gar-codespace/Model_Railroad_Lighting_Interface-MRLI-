'''
hardware library for the Adafruit Audio FX Sound Board
This library is a much less enthusiastic version of:
https://github.com/mmabey/Adafruit_Soundboard_uPy/tree/master

I have taylored it to the specific requirements of my project.
For this project it is not necessary to receive any replies from the sound card,
so there is no RX pin on the Pico.

Move imports to entities
'''

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

    def __init__(self, board:dict, protocol:dict):

        self.uart = entities.UART(protocol['ID'], baudrate=board['BAUD_RATE'], tx=protocol['TX'], rx=protocol['RX'])
        self.board = board
        self.wait = board['MIN_WAIT']

        self.reset_pin = None
        if board['RESET_PIN']:
            self.reset_pin = entities.PIN(board['RESET_PIN'], entities.PIN.IN)

    def initialize_board(self):

        self._flush_uart_input()
        self.reset()
        # self.volume = entities.SOUND_LEVEL
        # self.current_volume = entities.SOUND_LEVEL

    def _flush_uart_input(self):
        '''Read any available data from the UART bus until none is left.'''

        while self.uart.any():
            self.uart.read()
        
    def _send_simple(self, command):

        self._flush_uart_input()

        self.uart.write(f'{command}\n'.encode('utf-8'))

        entities.SLEEP_MS(self.wait)

        return self.uart.read()

    def play(self, track=None):

        if isinstance(track, int):
            command = CMD.NUMBER

        if isinstance(track, str):
            command = CMD.NAME

        self._send_simple(f'{command}{track}')

    def play_now(self, track):

        self.stop()
        entities.SLEEP_MS(self.wait)
        # print(self.uart.read())
        self.play(track)          

    def increment_up(self):

        self._send_simple(CMD.UP)

    def increment_down(self):

        self._send_simple(CMD.DOWN)

    def pause(self):

        self._send_simple(CMD.PAUSE)

    def unpause(self):

        self._send_simple(CMD.UNPAUSE)

    def stop(self):

        self._send_simple(CMD.STOP)

    def volume_up(self):
        '''does not work in tests'''

        for _ in range(0, 50):
            self._send_simple(CMD.UP)
            entities.SLEEP_MS(self.wait)

    def reset(self):
        '''Reset the sound board.'''

        if self.reset_pin:

            self.reset_pin(0)
            self.reset_pin(entities.PIN.OUT)
            entities.SLEEP_MS(self.wait)
            self.reset_pin(entities.PIN.IN)

            entities.SLEEP_MS(1000)  # Give the board some time to boot

        return True
