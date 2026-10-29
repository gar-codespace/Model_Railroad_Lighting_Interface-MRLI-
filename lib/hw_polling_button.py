'''
Hardware library for the fromt panel buttons.
Move imports to entities
'''
'''
params:
BUTTON0 = {
            'NORMALLY_OPEN':True, # False for NORMALLY_CLOSED
            'DEBOUNCE_TIME':50,
            'MULTI_TIME':200,
            'PRESSED_MSG':'button pressed',
            'RELEASED_MSG':'button released',
            'MULTI_MSG':'multiple presses',
            }
'''

__fork__ = 'https://github.com/ubidefeo/MicroPython-Button'
__author__ = 'Greg Ritacco'

import entities


class Button:

  PRESS:bool = False
  RELEASE:bool = False
  MULTI:bool = False

  def __init__(self, params:dict, pin:entities.PIN, name:str=None):

  # Setttings
    self.pin = pin
    self.name = name
    self.cb_press:callable = None # pressed callback
    self.cb_release:callable = None # released callback
    self.cb_multi:callable = None # Multi press callback
    self.pressed_msg = params['PRESSED_MSG']
    self.released_msg = params['RELEASED_MSG']
    self.multi_msg = params['MULTI_MSG']
  # Debounce logic
    self.rest_state = params['NORMALLY_OPEN']
    self.previous_state = params['NORMALLY_OPEN']
    self.current_state = params['NORMALLY_OPEN']
    self.previous_debounced_state = params['NORMALLY_OPEN']
    self.current_debounced_state = params['NORMALLY_OPEN']
    self.debounce_time = params['DEBOUNCE_TIME']
    self.multi_time = params['MULTI_TIME']
    self.last_check_tick = entities.UTIME.ticks_ms()

  def on(self, event:str, callback:callable):
    '''Registers an event with a callback.'''

    setattr(self, event, True)
    attrib = f'cb_{event.lower()}'
    setattr(self, attrib, callback)

  def press_callback(self):
    if self.PRESS:
      self.cb_press(self.name, self.pressed_msg)

  def release_callback(self):
    if self.RELEASE:
      self.cb_release(self.name, self.released_msg)

  def multi_callback(self):
    if self.MULTI:
      self.cb_multi(self.name, self.multi_msg)

  def debounce(self):

    ms_now = entities.UTIME.ticks_ms()
    self.current_state = self.pin.value()
    state_changed = self.current_state != self.previous_state
    if state_changed:
      self.last_check_tick = ms_now
    state_stable = (ms_now - self.last_check_tick) > self.debounce_time
    if state_stable and not state_changed:
      self.last_check_tick = ms_now
      self.current_debounced_state = self.current_state
    self.previous_state = self.current_state

  def multi_press(self):
    ...

  def single_press(self):

    if self.current_debounced_state == self.previous_debounced_state:
      return

    if self.current_debounced_state != self.rest_state:
      self.press_callback()
    else:
      self.release_callback()
    
    self.previous_debounced_state = self.current_debounced_state

  def poll(self):
    self.debounce()
    self.multi_press()
    self.single_press()
