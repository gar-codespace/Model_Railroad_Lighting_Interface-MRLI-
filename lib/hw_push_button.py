'''
Hardware library for the fromt panel buttons.
Catches single release, multi release and long press.
Button actions are triggered by either:
a) an IRQ event: 'IRQ_TRIGGER':True
b) continuous polling: 'IRQ_TRIGGER':False
Move imports to entities

usage example:
pin = entities.PIN(entities.PICO_PIN['CONFIRM'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
self.bC = entities.Button(params=entities.BUTTON0, pin=pin, name='STANDBY')
self.bC.on(event='RELEASE', callback=self.cb_confirm_release)

entities.py:
from machine import Pin as PIN
import utime as UTIME

DEFAULT_CYCLE = 20

BUTTON0 = {
            'IRQ_TRIGGER':True, # False for asyncio trigger
            'DEBOUNCE_TIME':40,
            'MULTI_TIME':350,
            'LONG_TIME':800,
            'RELEASED_MSG':'button released',
            'MULTI_MSG':'multiple presses',
            'LONG_MSG':'long press'
            }
'''

__fork__ = 'https://github.com/ubidefeo/MicroPython-Button'
__reference__ = 'https://github.com/TTitanUA/micropython_rotary_encoder/tree/main'
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
    self.pin.irq(handler=self._irq_handler)
    self.name = name
    self.irq_polling = params['IRQ_TRIGGER']
    self.cb_release:callable = None # released callback
    self.cb_multi:callable = None # Multi release callback
    self.cb_long:callable = None # long press callback
    self.released_msg = params['RELEASED_MSG']
    self.multi_msg = params['MULTI_MSG']
    self.long_msg = params['LONG_MSG']
  # async polling
    self.rest_state = pin.value()
    self.previous_state = pin.value()
    self.current_state = pin.value()
    self.previous_debounced_state = pin.value()
    self.current_debounced_state = pin.value()
    self.debounce_time = params['DEBOUNCE_TIME']
    self.last_check_tick = entities.UTIME.ticks_ms()
  #IRQ polling
    self.tick_increment = 0
    self.tick_count = 0
    self.debounce_threshold = params['DEBOUNCE_TIME'] / entities.DEFAULT_CYCLE
  # Parsing logic
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

  def _irq_handler(self, pin):

    self.tick_increment = 1

  def _irq_parse(self):

  # On Press
    if self.current_debounced_state != self.rest_state:
      self.long_tick = 1
      self.multi_tick = 0 # Stops the _multi_counter
      self.press_count += 1
      return
  # On release
    self.long_tick = 0
    self.long_count = 0
    self.multi_tick = 1 # Starts the _multi_counter

  def _irq_counter(self):

    self.tick_count += self.tick_increment
    if self.tick_count >= self.debounce_threshold:
      self.tick_increment = 0
      self.tick_count = 0
      self.current_debounced_state = self.pin.value()
      self._irq_parse()

  def _uasyncio_debounce(self):

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

  def _uasyncio_parse(self):

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

    if self.irq_polling:
      self.irq_poll()
    else:
      self.asyncio_poll()

# Picks one of these to put into an uasyncio loop
  def irq_poll(self):
    '''IRQ triggers the button action.'''
    self._irq_counter()
    self._multi_counter()
    self._long_counter()

  def asyncio_poll(self):
    '''uasyncio polling triggers the button action'''
    self._uasyncio_debounce()
    self._uasyncio_parse()
    self._multi_counter()
    self._long_counter()
