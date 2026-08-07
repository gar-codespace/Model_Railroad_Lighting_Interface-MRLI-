__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MAX9744.git"

import entities

try:
    import threading
except ImportError:
    threading = None

# Internal constants:
_MAX9744_DEFAULT_ADDRESS = entities.CONST(0b01001011)
_MAX9744_COMMAND_VOLUME = entities.CONST(0b00000000)
_MAX9744_COMMAND_FILTERLESS = entities.CONST(0b01000000)
_MAX9744_COMMAND_CLASSIC_PWM = entities.CONST(0b01000001)
_MAX9744_COMMAND_VOLUME_UP = entities.CONST(0b11000100)
_MAX9744_COMMAND_VOLUME_DOWN = entities.CONST(0b11000101)


class MAX9744:
    """MAX9744 20 watt class D amplifier.

    :param i2c: The I2C bus for the device.

    :param address: (Optional) The address of the device if it has been overridden from the
                    default with the AD1, AD2 pins.
    """

    # Global buffer for writing data.  This saves memory use and prevents
    # heap fragmentation.  However this is not thread-safe or re-entrant by
    # design!
    _BUFFER = bytearray(1)

    def __init__(self, i2c, address: int = _MAX9744_DEFAULT_ADDRESS):
        # This device doesn't use registers and instead just accepts a single
        # command string over I2C.  As a result we don't use bus device or
        # other abstractions and just talk raw I2C protocol.
        self._i2c = i2c
        self._address = address

    def _write(self, val: int) -> None:
        # Perform a write to update the amplifier state.
        try:
            # Make sure bus is locked before write.
            while not self._i2c.try_lock():
                pass
            # Build bytes to send to device with updated value.
            print('write')
            #self._BUFFER[0] = val & 0xFF
            self._i2c.writeto(self._address, self._BUFFER)
        except:
            pass
        #finally:
            # Ensure bus is always unlocked.
            # self._i2c.unlock()
# 
    def _set_volume(self, volume: int):
        # Set the volume to the specified level (0-63).
        assert 0 <= volume <= 63
        self._write(_MAX9744_COMMAND_VOLUME | (volume & 0x3F))


    volume = property(
        None,
        _set_volume,
        None,
        "Set the volume of the amplifier.  Specify a value from 0-63 where 0 is muted/off and 63 is maximum volume.",  # noqa: E501
    )


# 
    def volume_up(self) -> None:
        """Increase the volume by one level."""
        self._write(_MAX9744_COMMAND_VOLUME_UP)

    def volume_down(self) -> None:
        """Decrease the volume by one level."""
        self._write(_MAX9744_COMMAND_VOLUME_DOWN)
