'''
Hardware library for the fromt panel buttons.
Move imports to entities
'''
'''
Parameters are:
BUTTON_IRQ = {
            'NORMALLY_OPEN':True, # False for NORMALLY_CLOSED TODO does this matter?
            'DEBOUNCE_TIME':50, TODO use this as the basis for multipress
            'PRESSED':'button pressed',
            'RELEASED':'button released'
            }
'''

__author__ = 'Greg Ritacco'

import entities


class IrqButton:

  def __init__(self, params:dict, pin:object, cb_press:object=None, cb_release:object=None, name:str=None):

  # Setttings
    self.button_state = pin.value()
    self.pin = pin.irq(trigger=entities.PIN.IRQ_RISING | entities.PIN.IRQ_FALLING, handler=self.interrupt)
    self.name = name
    self.pressed = params['PRESSED']
    self.released = params['RELEASED']
    self.cb_press = cb_press # pressed callback
    self.cb_release = cb_release # released callback

  def interrupt(self, pin):
    
    pin.irq(handler=None)
    
    if pin.value() == self.button_state == 0: # Pressed
        self.button_state = 1
        self.press_callback()
    
    elif pin.value() == self.button_state == 1: # Released
        self.button_state = 0
        self.release_callback()

    pin.irq(handler=self.interrupt)

  def press_callback(self):
    try:
      self.cb_press(self.name, self.pressed)
    except:
      pass

  def release_callback(self):
    try:
      self.cb_release(self.name, self.released)
    except:
      pass
