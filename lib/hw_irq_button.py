'''
Hardware library for the front panel buttons.
Move imports to entities
'''
'''
Parameters are:
IRQ_BUTTON_0 = {
            'INITIATE_TRIGGER':'falling', # pick one
            # 'INITIATE_TRIGGER':'rising',
            # 'INITIATE_TRIGGER':'high',
            # 'INITIATE_TRIGGER':'low'

            'RISING | FALLING':True, # one or the other
            'HIGH | LOW':False,

            'PRESS_MSG':'button pressed',
            'RELEASE_MSG':'button released',
            'MULTI_PRESS_TIME':50,
            }
'''

__author__ = 'Greg Ritacco'

import entities


class IrqButton:

  def __init__(self, params:dict, pin:object, cb_press:object=None, cb_release:object=None, name:str=None):

    trigger= entities.PIN.IRQ_RISING | entities.PIN.IRQ_FALLING
    if params['HIGH | LOW']:
      trigger= entities.PIN.HIGH_LEVEL | entities.PIN.LOW_LEVEL

    self.pin = pin.irq(trigger=trigger, handler=self.handler)

    if params['INITIATE_TRIGGER'] == 'rising':
      self.button_state = 1
      self.trigger = 'lo2hi'

    if params['INITIATE_TRIGGER'] == 'falling':
      self.button_state = 0
      self.trigger = 'hi2lo'

    if params['INITIATE_TRIGGER'] == 'high':
      self.button_state = 1
      self.trigger = 'lo2hi'

    if params['INITIATE_TRIGGER'] == 'low':
      self.button_state = 0
      self.trigger = 'hi2lo'

    self.name = name
    self.cb_press = cb_press # pressed callback
    self.cb_release = cb_release # released callback

    self.press_msg = params['PRESS_MSG']
    self.release_msg = params['RELEASE_MSG']

  def handler(self, pin):
    '''pin is automatically passed in by Micropython, there's no choice.'''
    
    pin.irq(handler=None)
    
    if pin.value() == self.button_state == 0:
      self.button_state = 1
      self.callback_0()
    
    elif pin.value() == self.button_state == 1:
      self.button_state = 0
      self.callback_1()

    entities.UASYNCIO.sleep_ms(entities.CLOCK_CYCLE) # Adds some more stability
    pin.irq(handler=self.handler)

  def callback_0(self):
    if self.trigger == 'hi2lo':
      attrib = 'cb_press'
      msg = self.press_msg
    else:
      attrib = 'cb_release'
      msg = self.release_msg

    try:
      getattr(self, attrib)(self.name, msg)
    except:
      pass

  def callback_1(self):
    if self.trigger == 'lo2hi':
      attrib = 'cb_press'
      msg = self.press_msg
    else:
      attrib = 'cb_release'
      msg = self.release_msg

    try:
      getattr(self, attrib)(self.name, msg)
    except:
      pass
