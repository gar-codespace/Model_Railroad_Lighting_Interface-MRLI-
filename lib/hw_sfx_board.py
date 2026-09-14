import entities


class SoundFX:

    def __init__(self, uart: object, board: object):

        self._uart = entities.UART(uart['ID'], baudrate=board['BAUD_RATE'], tx=uart['TX'], rx=uart['RX'])
        self.board = board

        self._sb_rst = board['RESET_PIN']
        if board['RESET_PIN']:
            self._sb_rst = entities.PIN(board['RESET_PIN'], mode=entities.PIN.IN)

        self.vol = board['VOLUME']

        self._cur_vol = None
        self._cur_track = None
        self._reset_attempted = False

        self._flush_uart_input()

    def _flush_uart_input(self):

        '''Read any available data from the UART bus until none is left.'''

        while self._uart.any():
            self._uart.read()
        
    def _send_simple(self, command, check=None, strip=True):
        '''Send the command, optionally do a check on the output.'''

        self._flush_uart_input()
        command = command.strip()  # Make sure there's not more than one newline
        self._uart.write(b'{}\n'.format(command))
        if len(command) > 1:
            # We need to gobble the return when there's more than one character in the command
            self._uart.readline()
        try:
            msg = self._uart.readline()
            if strip:
                msg = msg.strip()
            assert isinstance(msg, bytes)

        except (AttributeError, AssertionError):
            if self._reset_attempted:
                # Only try resetting once
                return False  # TODO: Better way to handle failed commands? Too broad?

            self._reset_attempted = True
            self.reset()
            return self._send_simple(command, check)

        if check is None:
            return msg
        else:
            self._reset_attempted = True  # We already sent a command successfully

        if isinstance(check, str):
            return msg.startswith(check.encode())
        elif isinstance(check, bytes):
            return msg.startswith(check)
        elif check:
            return msg.startswith(command[0].encode())

    def play(self, track=None):

        '''Play a track on the board.'''

        if isinstance(track, int):
            command = '#'
            num = track
        elif isinstance(track, str):
            command = 'P'
            num = self.track_num(track)
        else:
            raise TypeError('You must specify a track by its number (int) or its name (str)')
        
        if self._send_simple('{}{}'.format(command, track), 'play'):
            self._cur_track = num
            return True
        return False

    def play_now(self, track):

        '''Play a track on the board now, stopping current track if necessary.'''

        self.stop()
        if not self.play(track):
            # Playing the specified track failed, so just return False
            return False
        return True

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
            self.vol_down()
        return self._cur_vol

    @vol.setter
    def vol(self, new_vol):
        if new_vol is None:
            return
        if isinstance(new_vol, float):
            new_vol = int(new_vol * self.board['MAX_VOL'])
        if not isinstance(new_vol, int):

            return
        elif new_vol > self.vol:
            self.vol_up(new_vol)
        elif new_vol < self.vol:
            self.vol_down(new_vol)

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

    def pause(self):

        '''Pause playback, return if the command was successful.'''

        return self._send_simple('=', True)

    def unpause(self):

        '''Continue playback, return if the command was successful.'''

        return self._send_simple('>', True)

    def stop(self):

        '''Stop playback, return if the command was successful.'''

        return self._send_simple('q', True)

    def reset(self):
        '''Reset the sound board.

        Soft reset the board by bringing the ``RST`` pin low momentarily (10
        ms). This only has effect if the reset pin has been initialized in the
        constructor.

        Doing a soft reset on the board before doing any other actions can help
        ensure that it has been started in UART control mode, rather than GPIO
        trigger mode.

        .. seealso::

            `Soundboard Pinout <https://learn.adafruit.com/adafruit-audio-fx-sound-board/pinouts#uart-pins>`_
                Documentation on the sound boards' pinouts.


        :return: Whether the reset was successful. If the reset pin was not
            initialized in the constructor, this will always return ``False``.
        :rtype: bool
        '''
        if self._sb_rst is None:
            # Don't attempt to restart the board if the reset pin wasn't initialized
            return False


        self._sb_rst(0)
        self._sb_rst.mode(entities.PIN.OUT)
        entities.UTIME.sleep_ms(10)
        self._sb_rst.mode(entities.PIN.IN)

        entities.UTIME.sleep_ms(1000)  # Give the board some time to boot
        msg = self._uart.readline().strip()


        msg = self._uart.readline().strip()


        if not msg.startswith('Adafruit FX Sound Board'):
            return False

        entities.UTIME.sleep_ms(250)

        msg = self._uart.readline().strip()


        msg = self._uart.readline().strip()


        # Reset volume level and current track
        self.vol = self._cur_vol
        self._cur_track = None

        return True
