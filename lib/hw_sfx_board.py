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

    def __init__(self, uart: object, board: object):

        self.uart = entities.UART(uart['ID'], baudrate=board['BAUD_RATE'], tx=uart['TX'], rx=uart['RX'])
        self.board = board

        self._sb_reset_pin = board['RESET_PIN']
        if board['RESET_PIN']:
            self._sb_reset_pin = entities.PIN(board['RESET_PIN'], entities.PIN.IN)

        self.volume: float
        self.current_volume: float

        self._cur_vol = None
        self._cur_track = None
        self._reset_attempted = False

    def initialize_board(self):

        # self.uart.init()
        self._flush_uart_input()
        self.volume = entities.SOUND_LEVEL
        self.current_volume = entities.SOUND_LEVEL

    def _flush_uart_input(self):
        '''Read any available data from the UART bus until none is left.'''

        while self.uart.any():
            self.uart.read()
        
    def _send_simple(self, command):

        self._flush_uart_input()

        self.uart.write(f'{command}\n'.encode('utf-8'))

    def play(self, track=None):

        if isinstance(track, int):
            command = CMD.NUMBER

        if isinstance(track, str):
            command = CMD.NAME

        self._send_simple(f'{command}{track}')

    def play_now(self, track):

        self.stop()
        entities.UTIME.sleep_ms(50)
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


    
    @property
    def vol(self):
        '''Current volume.

        This is implemented as a class property, so you can get and set its
        value directly. When setting a new volume, you can use an ``int`` or a
        ``float`` (assuming your board supports floats). When setting to an
        ``int``, it should be in the range of 0-204. When set to a ``float``,
        the value will be interpreted as a percentage of :obj:`self.board['MAX_VOL']`.

        :rtype: int
        '''
        if self._cur_vol is None:
            self.volume_down()
        return self._cur_vol

    @vol.setter
    def vol(self, new_vol):
        if new_vol is None:
            return
        if isinstance(new_vol, float):
            new_vol = int(new_vol * self.board['MAX_VOL'])
        if not isinstance(new_vol, int):

            return
        elif new_vol > self.volume:
            self.volume_up(new_vol)
        elif new_vol < self.volume:
            self.volume_down(new_vol)


    def vol_up(self, vol=None):
        '''Turn volume up by 2 points, return current volume level [0-204].'''

        print('Turning volume up')
        if vol is None:
            self._cur_vol = int(self._send_simple('+'))
            return self._cur_vol
        if vol > self.board['MAX_VOL']:
            vol = self.board['MAX_VOL']

        self._cur_vol = self.board['MIN_VOL'] - 1


        while vol > self._cur_vol:
            self._cur_vol = int(self._send_simple('+'))

        return self._cur_vol

    def vol_down(self, vol=None):

        '''Turn volume down by 2 points, return current volume level [0-204].'''

        if vol is None:
            self._cur_vol = int(self._send_simple('-'))
            return self._cur_vol
        self._cur_vol = self.board['MAX_VOL'] + 1
        if vol < self.board['MIN_VOL']:

            vol = self.board['MIN_VOL']


        while vol < self._cur_vol:
            self._cur_vol = int(self._send_simple('-'))

        return self._cur_vol



    def reset(self):
        '''Reset the sound board.'''

        if self._sb_reset_pin is None:
            return


        self._sb_reset_pin(0)
        self._sb_reset_pin(entities.PIN.OUT)
        entities.UTIME.sleep_ms(10)
        self._sb_reset_pin(entities.PIN.IN)

        entities.UTIME.sleep_ms(1000)  # Give the board some time to boot








        # Reset volume level and current track
        self.volume = self._cur_vol
        self._cur_track = None

        return True
