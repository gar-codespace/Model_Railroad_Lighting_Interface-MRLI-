import entities


class SoundFX:

    def __init__(self, uart: object, board: object):

        self._uart = entities.UART(uart['ID'], baudrate=board['BAUD_RATE'], tx=uart['TX'], rx=uart['RX'])
        self.board = board

        self._sb_rst = board['RESET_PIN']
        if board['RESET_PIN']:
            self._sb_rst = entities.PIN(board['RESET_PIN'], mode=entities.PIN.IN)

        self.vol = board['VOLUME']

        self._files = None
        self._sizes = None
        self._lengths = None
        self._track = {}

        self._cur_vol = None
        self._cur_track = None
        self._reset_attempted = False

        if board['ALT_GET_FILES']:
            self.use_alt_get_files()

        self._flush_uart_input()

    def _flush_uart_input(self):
        '''Read any available data from the UART bus until none is left.'''
        while self._uart.any():
            self._uart.read()
        print('here')
        
    def _send_simple(self, cmd, check=None, strip=True):
        '''Send the command, optionally do a check on the output.'''

        self._flush_uart_input()
        cmd = cmd.strip()  # Make sure there's not more than one newline
        self._uart.write(b'{}\n'.format(cmd))
        if len(cmd) > 1:
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
            return self._send_simple(cmd, check)

        if check is None:
            return msg
        else:
            self._reset_attempted = True  # We already sent a command successfully

        if isinstance(check, str):
            return msg.startswith(check.encode())
        elif isinstance(check, bytes):
            return msg.startswith(check)
        elif check:
            return msg.startswith(cmd[0].encode())

    @property
    def files(self):
        '''Return a ``list`` of the files on the sound board.

        :rtype: list
        '''
        if self._files is None:
            self._get_files()
        return self._files

    @property
    def sizes(self):
        '''Return a ``list`` of the files' sizes on the sound board.

        .. seealso:: :meth:`use_alt_get_files`

        :rtype: list
        '''
        if self._sizes is None:
            self._get_files()
        return self._sizes

    def _get_files(self):
        '''Ask the board for the files and their sizes, store the results.'''
        self._flush_uart_input()

        self._files = []
        self._sizes = []
        self._uart.write('L\n')
        entities.UTIME.sleep_ms(10)
        i = 0
        while self._uart.any():
            msg = self._uart.readline().strip()

            fname, fsize = msg.split(b'\t')
            fname = fname.decode()
            self._files.append(fname)
            self._sizes.append(int(fsize))
            self._track[fname] = i
            i += 1

    def _get_files_alt(self):
        '''Play every track, get info from feedback.'''
        vol = self.vol
        self.vol = 0
        self._files = []
        self._lengths = []
        self._sizes = []
        for i in range(entities.MAX_FILES):
            self.stop()
            msg = self._send_simple('#{}'.format(i))
            if msg.startswith(b'NoFile'):
                # Playing track i failed, it must not be a valid track number
                break
            play, track_num, fname = msg.split(b'\t')
            self._files.append(fname)
            self._track[fname] = i

            entities.UTIME.sleep_ms(50)
            sec = self.track_time()
            if sec:
                self._lengths.append(sec[1])
            else:
                self._lengths.append(0)
            size = self.track_size()
            if size:
                self._sizes.append(size[1])
            else:
                self._sizes.append(0)

        self.vol = vol

    @property
    def lengths(self):
        '''Return a ``list`` of the track lengths in seconds.

        .. note::

            In my own testing of this method, the board always returns a value
            of zero seconds for the length for every track, no matter if it's a
            WAV or OGG file, short or long track.

        :rtype: list
        '''
        if self._lengths is None:
            self._get_lengths()
        return self._lengths

    def _get_lengths(self):
        '''Store the length of each track.'''
        self._get_files_alt()

    def file_name(self, n):
        '''Return the name of track ``n``.

        :param int n: Index of a file on the sound board or ``False`` if the
            track number doesn't exist.
        :return: Filename of track ``n``.
        :rtype: str or bool
        '''
        try:
            return self.files[n]
        except IndexError:
            return False

    def track_num(self, file_name):
        '''Return the track number of the given file name.

        :param str file_name: File name of the track. Should be one of the
            values from the :attr:`files` property.
        :return: The track number of the file name or ``False`` if not found.
        :rtype: int or bool
        '''
        try:
            return self._track[file_name]
        except KeyError:
            return False

    def play(self, track=None):
        '''Play a track on the board.

        :param track: The index (``int``) or filename (``str``) of the track to
            play.
        :type track: int or str
        :return: If the command was successful.
        :rtype: bool
        '''
        if isinstance(track, int):
            cmd = '#'
            num = track
        elif isinstance(track, str):
            cmd = 'P'
            num = self.track_num(track)
        else:
            raise TypeError('You must specify a track by its number (int) or its name (str)')
        
        if self._send_simple('{}{}'.format(cmd, track), 'play'):
            self._cur_track = num
            return True
        return False

    def play_now(self, track):
        '''Play a track on the board now, stopping current track if necessary.

        :param track: The index (``int``) or filename (``str``) of the track to
            play.
        :type track: int or str
        :return: If the command was successful.
        :rtype: bool
        '''
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

        '''Turn volume up by 2 points, return current volume level [0-204].

        :param int vol: Target volume. When not ``None``, volume will be turned
            up to be greater than or equal to this value.
        :rtype: int
        '''
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
        '''Turn volume down by 2 points, return current volume level [0-204].

        :param int vol: Target volume. When not ``None``, volume will be turned
            down to be less than or equal to this value.
        :rtype: int
        '''


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
        '''Pause playback, return if the command was successful.

        :rtype: bool
        '''
        return self._send_simple('=', True)

    def unpause(self):
        '''Continue playback, return if the command was successful.

        :rtype: bool
        '''
        return self._send_simple('>', True)

    def stop(self):
        '''Stop playback, return if the command was successful.

        :rtype: bool
        '''
        return self._send_simple('q', True)

    def track_time(self):
        '''Return the current position of playback and total time of track.

        :rtype: tuple
        '''
        msg = self._send_simple('t')
        if not msg:
            return -1, -1

        if len(msg) != 11:
            return False
        current, total = msg.decode('utf-8').split(':')
        return int(current), int(total)

    def track_size(self):
        '''Return the remaining size and total size.

        It seems the remaining track size refers to the number of bytes left
        for the sound board to process before the playing of the track will be
        over.

        :return: Remaining track size and total size
        :rtype: tuple
        '''
        msg = self._send_simple('s')
        if not msg:
            return -1, -1

        if len(msg) != 21:
            return False
        remaining, total = msg.decode('utf-8').split('/')
        return int(remaining), int(total)

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

    def use_alt_get_files(self, now=False):
        '''Get list of track files using an alternate method.

        If the list of files is missing tracks you know are on the sound board,
        try calling this method. It doesn't depend on the sound board's internal
        command for returning a list of files. Instead, it plays each of the
        tracks using their track numbers and gets the filename and size from
        the output of the play command.

        :param bool now: When set to ``True``, the alternate method of getting
            the files list will be called immediately. Otherwise, the list of
            files will be populated the next time the :attr:`files` property is
            accessed (lazy loading).
        :rtype: None
        '''
        self._get_files = self._get_files_alt
        if now:
            self._get_files()
