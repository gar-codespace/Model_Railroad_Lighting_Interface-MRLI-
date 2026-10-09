'''
Hardware library for the fromt panel buttons.
Move imports to entities
'''
__author__ = 'https://github.com/ubidefeo/MicroPython-Button'

import entities


class Button:

  def __init__(self, params:dict, pin:object, cb_press:object=None, cb_release:object=None, name:str=None):

  # Setttings
    self.pin = pin
    self.name = name
    self.pressed = params['PRESSED']
    self.released = params['RELEASED']
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
      self.cb_press(self.name, self.pressed)
    except:
      pass

  def release_callback(self):
    try:
      self.cb_release(self.name, self.released)
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

  def update(self):
    self.debounce()
    self.check_debounce_state()
