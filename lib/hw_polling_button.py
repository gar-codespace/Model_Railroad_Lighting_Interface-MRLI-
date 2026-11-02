'''
Hardware library for the fromt panel buttons.
Catches single release, multi release and long press.
Move imports to entities
'''
'''
usage:
pin = entities.PIN(entities.PICO_PIN['CONFIRM'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
self.bC = entities.Button(params=entities.BUTTON0, pin=pin, name='STANDBY')
self.bC.on(event='RELEASE', callback=self.cb_confirm_release)
params:
BUTTON0 = {
            'NORMALLY_OPEN':True, # False for NORMALLY_CLOSED
            'DEBOUNCE_TIME':40,
            'MULTI_TIME':350,
            'LONG_TIME':800,
            'RELEASED_MSG':'button released',
            'MULTI_MSG':'multiple presses',
            'LONG_MSG':'long press'
            }
'''

__fork__ = 'https://github.com/ubidefeo/MicroPython-Button'
__author__ = 'Greg Ritacco'

import entities


class Button:

# Events
  RELEASE:bool = False
  MULTI:bool = False
  LONG:bool = False

  def __init__(self, params:dict, pin:entities.PIN, name:str=None):

  # Callback setttings
    self.pin = pin
    self.name = name
    self.cb_release:callable = None # released callback
    self.cb_multi:callable = None # Multi release callback
    self.cb_long:callable = None # long press callback
    self.released_msg = params['RELEASED_MSG']
    self.multi_msg = params['MULTI_MSG']
    self.long_msg = params['LONG_MSG']
  # Debounce
    self.rest_state = params['NORMALLY_OPEN']
    self.previous_state = params['NORMALLY_OPEN']
    self.current_state = params['NORMALLY_OPEN']
    self.previous_debounced_state = params['NORMALLY_OPEN']
    self.current_debounced_state = params['NORMALLY_OPEN']
    self.debounce_time = params['DEBOUNCE_TIME']
    self.last_check_tick = entities.UTIME.ticks_ms()
  # Parse
    self.multi_count:int = 0
    self.multi_tick:int = 0
    self.multi_threshold = params['MULTI_TIME'] / entities.DEFAULT_CYCLE
    self.press_count:int = 0
    self.long_count:int = 0
    self.long_tick:int = 0
    self.long_threshold = params['LONG_TIME'] / entities.DEFAULT_CYCLE

  def on(self, event:str, callback:callable):
    '''Registers an event with a callback.'''

    setattr(self, event, True)
    attrib = f'cb_{event.lower()}'
    setattr(self, attrib, callback)

  def _debounce(self):

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

  def _parse_input(self):

  # Did anything change?
    if self.current_debounced_state == self.previous_debounced_state:
      return
  # On Press
    if self.current_debounced_state != self.rest_state:
      self.long_tick = 1
      self.multi_tick = 0 # Stops the _multi_counter
      self.press_count += 1
      self.previous_debounced_state = self.current_debounced_state
      return
  # On release
    self.long_tick = 0
    self.long_count = 0
    self.multi_tick = 1 # Starts the _multi_counter
    self.previous_debounced_state = self.current_debounced_state

  def _multi_counter(self):
    '''Single or multiple releases.'''

# Start on release, stop on press.
    self.multi_count += self.multi_tick
    if self.multi_count >= self.multi_threshold:
      self._rubric(self.press_count) # Catches single or multi
      # print(f'press count: {self.press_count}')
      self.multi_tick = 0
      self.multi_count = 0
      self.press_count = 0
      self.long_tick = 0
      self.long_count = 0

  def _long_counter(self):
    '''Long press.'''
    
# Start on press, stop on release.
    self.long_count += self.long_tick
    if self.long_count >= self.long_threshold:
      self._rubric(0) # catches the long press
      self.multi_tick = 0
      self.multi_count = 0
      self.press_count = 0
      self.long_tick = 0
      self.long_count = 0
      print('long press')

  def _rubric(self, count:int):
    '''Picks the appropriate callback.'''

    if count == 1 and self.RELEASE:
      self.cb_release(self.name, self.released_msg)

    if count > 1 and self.MULTI:
        self.cb_multi(self.name, self.multi_msg) # one or the other
        # self.cb_multi(self.name, count)

    if count == 0 and self.LONG:
      self.cb_long(self.name, self.long_msg)

  def poll(self):
    self._debounce()
    self._parse_input()
    self._multi_counter()
    self._long_counter()
