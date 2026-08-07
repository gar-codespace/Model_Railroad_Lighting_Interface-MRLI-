# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`busio` - Bus protocol support like I2C and SPI
=================================================

See `CircuitPython:busio` in CircuitPython for more details.

* Author(s): cefn
"""

import entities

try:
    import threading
except ImportError:
    threading = None

# pylint: disable=unused-import
# import adafruit_platformdetect.constants.boards as ap_board
# import adafruit_platformdetect.constants.chips as ap_chip
# from adafruit_blinka import Enum, Lockable, agnostic
# from adafruit_blinka.agnostic import board_id, detector

# pylint: disable=import-outside-toplevel,too-many-branches,too-many-statements
# pylint: disable=too-many-arguments,too-many-function-args,too-many-return-statements


class I2C:
    """
    Busio I2C Class for CircuitPython Compatibility. Used
    for both MicroPython and Linux.

    NOTE: Frequency has no effect on Linux systems. The argument is only there for compatibility.
    """

    def __init__(self, scl, sda, frequency=100000):
        self.init(scl, sda, frequency)

    def init(self, scl, sda, frequency):
        """Initialization"""
        self.deinit()

        _I2C = entities.I2C()

        portId = 1

        self._i2c = _I2C(portId, mode=_I2C.MASTER, baudrate=frequency)

        if threading is not None:
            self._lock = threading.RLock()

    def deinit(self):
        """Deinitialization"""
        try:
            del self._i2c
        except AttributeError:
            pass

    def __enter__(self):
        if threading is not None:
            self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if threading is not None:
            self._lock.release()
        self.deinit()

    def scan(self):
        """Scan for attached devices"""
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        """Read from a device at specified address into a buffer"""
        if start != 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        return self._i2c.readfrom_into(address, buffer, stop=True)

    def writeto(self, address, buffer, *, start=0, end=None):
        """Write to a device at specified address from a buffer"""
        if isinstance(buffer, str):
            buffer = bytes([ord(x) for x in buffer])
        if start != 0 or end is not None:
            if end is None:
                return self._i2c.writeto(address, memoryview(buffer)[start:], stop=True)
            return self._i2c.writeto(address, memoryview(buffer)[start:end], stop=True)
        return self._i2c.writeto(address, buffer, stop=True)

    def writeto_then_readfrom(
        self,
        address,
        buffer_out,
        buffer_in,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
        stop=False,
    ):
        """ "Write to a device at specified address from a buffer then read
        from a device at specified address into a buffer
        """
        return self._i2c.writeto_then_readfrom(
            address,
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
            stop=stop,
        )

