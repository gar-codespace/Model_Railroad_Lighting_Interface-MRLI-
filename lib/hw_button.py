'''
Hardware library for the fromt panel buttons.
https://github.com/ubidefeo/MicroPython-Button
Move imports to entities

params looks like this:
BUTTON0 = { # Generic push button, normally open
            'REST_STATE':True,
            'INTERNAL_PULLDOWN':False,
            'INTERNAL_PULLUP':True,
            'DEBOUNCE_TIME':50    
            }
'''

import entities

class Button(object):

  RELEASED = 'released'
  PRESSED = 'pressed'

  def __init__(self, params:dict, pin:object, cb_release:object = None, cb_press:object = None, name:str = None):
    self.pin_number = pin
    self.name = name
    self.rest_state = params['REST_STATE']
    self.previous_state = params['REST_STATE']
    self.current_state = params['REST_STATE']
    self.previous_debounced_state = params['REST_STATE']
    self.current_debounced_state = params['REST_STATE']
    self.debounce_time = params['DEBOUNCE_TIME']
    self.last_check_tick = entities.UTIME.ticks_ms()

    if params['INTERNAL_PULLDOWN']:
      self.internal_pull = entities.PIN.PULL_DOWN
    elif  params['INTERNAL_PULLUP']:
      self.internal_pull = entities.PIN.PULL_UP
    else:
      self.internal_pull = None

    if isinstance(pin, int):
      self.pin = entities.PIN(pin, mode=entities.PIN.IN, pull=self.internal_pull)
    else:
      self.pin = pin
      
    self.cb_press = cb_press # pressed callback
    self.cb_release = cb_release # released callback
    self.active = False

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
    if self.current_debounced_state != self.previous_debounced_state:
      if self.current_debounced_state != self.rest_state:
        self.active = True
        if self.cb_press:
          self.cb_press(self.name, Button.PRESSED)
      else:
        self.active = False
        if self.cb_release:
          self.cb_release(self.name, Button.RELEASED)
    self.previous_debounced_state = self.current_debounced_state

  def update(self):
    self.debounce()
    self.check_debounce_state()
