'''
hardware library
'''
import entities


class Button:
    """
    A simple Button class
    Create the button using Button(pinnumber, name, handler)
    handler is typically self, and create two methods buttonPressed and buttonReleased
    to handle the push and release of the button.
    The name of the button will be passed back to the handler to identify
    which button was pressed/released
    https://github.com/jitsengupta/PicoLibrary/blob/main/Button.py
    """
    
    def __init__(self, pin, name, *, handler=None, lowActive=True):
        """
        Initialize attributes and other internal data
        """
        
        self._pinNo = pin
        self._name = name
        if lowActive:
            self._pin = entities.PIN(pin, entities.PIN.IN, entities.PIN.PULL_UP)
        else:
            self._pin = entities.PIN(pin, entities.PIN.IN, entities.PIN.PULL_DOWN)
        self._debounce_time = 0
        self._lowActive = lowActive
        self._lastStatus = None
        self._handler = None
        self.setHandler(handler)
        
    def isPressed(self):
        """ Check if the button is pressed or not - useful if polling """
        
        status = (self._lowActive and self._pin.value() ==0) or (not self._lowActive and self._pin.value() == 1)
        return status
    
    def setHandler(self, handler):
        """ 
	    set the handler to a new handler. Pass None to remove existing handler
	    """
        
        # if the old handler was active already, or if the new handler is None, remove the irq
        if self._handler is not None or handler is None:
            self._pin.irq(handler = None)
    
        # Now set it to th enew handler
        self._handler = handler
        # Create the IRQ if the handler is not None
        if self._handler:
            self._pin.irq(trigger = entities.PIN.IRQ_FALLING | entities.PIN.IRQ_RISING, handler = self._callback)
        
    def _callback(self, pin):
        """ The private interrupt handler - will call appropriate handlers """
        
        t = entities.UTIME.ticks_ms()
        v = self._pin.value()
        if ((self._lastStatus == None or self._lastStatus != v) and t-self._debounce_time) > 50:
            self._debounce_time=t
            self._lastStatus = v
            if self._handler is not None:
                if self.isPressed():
                    self._handler.buttonPressed(self._name)
                else:
                    self._handler.buttonReleased(self._name)
        #self._debounce_time=t