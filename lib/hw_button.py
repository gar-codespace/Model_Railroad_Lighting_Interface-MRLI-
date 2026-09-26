'''
Hardware library for the fromt panel buttons.
https://github.com/ubidefeo/MicroPython-Button
Move imports to entities

params looks like this:
BUTTON0 = { # Generic push button, normally open
            'REST_STATE':True,
            'DEBOUNCE_TIME':50,
            'PRESSED':'pressed',
            'RELEASED':'released',
            'PULL':'PULL_UP' # not used
            }

'''

import entities

class Button:

  def __init__(self, params:dict, pin:object, cb_press:object = None, cb_release:object = None, name:str = None):

    self.pin = pin
    self.name = name
    self.rest_state = params['REST_STATE']
    self.previous_state = params['REST_STATE']
    self.current_state = params['REST_STATE']
    self.previous_debounced_state = params['REST_STATE']
    self.current_debounced_state = params['REST_STATE']
    self.debounce_time = params['DEBOUNCE_TIME']
    self.pressed = params['PRESSED']
    self.released = params['RELEASED']

    self.cb_press = cb_press # pressed callback
    self.cb_release = cb_release # released callback
      
    self.last_check_tick = entities.UTIME.ticks_ms()

  def press(self):
    try:
      self.cb_press(self.name)
    except:
      pass

  def release(self):
    try:
      self.cb_release(self.name)
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
      self.press()
      self.previous_debounced_state = self.current_debounced_state
    else:
      self.release()
      self.previous_debounced_state = self.current_debounced_state

  def update(self):
    self.debounce()
    self.check_debounce_state()
