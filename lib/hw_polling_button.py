'''
Hardware library for the fromt panel buttons.
Move imports to entities
'''
'''
params:
BUTTON0 = {
            'NORMALLY_OPEN':True, # False for NORMALLY_CLOSED
            'TRIGGER_TYPE':'HI2LO',
            # 'TRIGGER_TYPE':'LO2HI',
            'DEBOUNCE_TIME':50,
            'PRESSED_MSG':'button pressed',
            'RELEASED_MSG':'button released'
            }
'''

__author__ = 'https://github.com/ubidefeo/MicroPython-Button'

import entities


class Button:

  def __init__(self, params:dict, pin:object, cb_press:object=None, cb_release:object=None, name:str=None):

  # Setttings
    self.pin = pin
    self.name = name
    self.pressed_msg = params['PRESSED_MSG']
    self.released_msg = params['RELEASED_MSG']
    self.cb_press = cb_press # pressed callback
    self.cb_release = cb_release # released callback
  # Debounce logic
    self.rest_state = params['NORMALLY_OPEN']
    self.previous_state = params['NORMALLY_OPEN']
    self.current_state = params['NORMALLY_OPEN']
    self.previous_debounced_state = params['NORMALLY_OPEN']
    self.current_debounced_state = params['NORMALLY_OPEN']
    self.debounce_time = params['DEBOUNCE_TIME']
    self.last_check_tick = entities.UTIME.ticks_ms()

  def press_callback(self):
    try:
      self.cb_press(self.name, self.pressed_msg)
    except:
      pass

  def release_callback(self):
    try:
      self.cb_release(self.name, self.released_msg)
    except:
      pass

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

  def check_debounce_state(self):

    if self.current_debounced_state == self.previous_debounced_state:
      return

    if self.current_debounced_state != self.rest_state:
      self.press_callback()
    else:
      self.release_callback()
    
    self.previous_debounced_state = self.current_debounced_state

  def poll(self):
    self.debounce()
    self.check_debounce_state()
