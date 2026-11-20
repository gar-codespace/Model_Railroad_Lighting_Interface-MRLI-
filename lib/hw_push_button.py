'''
Model Railroad Lighting Interface (MRLI)

Hardware library for the fromt panel buttons.
Catches single release, multi release and long press.
Button actions are triggered by either:
a) an IRQ event: 'IRQ_TRIGGER':True
b) continuous polling: 'IRQ_TRIGGER':False
Moved imports to entities.

params:
BUTTON_0 = {
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
  RELEASE = 'release'
  MULTI = 'multi'
  LONG = 'long'

  def __init__(self, params:dict, pin:entities.PIN, name:str=None):

# Callback management
    self._callbacks:dict = {}
    self._working_event:str = None
# Callback setttings
    self.pin = pin
    self.pin.irq(handler=self._irq_handler) # uPython automatically triggers on rising and falling
    self.name = name
    self.irq_polling = params['IRQ_TRIGGER']
    self.cb_release:callable = None # released callback
    self.cb_multi:callable = None # Multi release callback
    self.cb_long:callable = None # long press callback
    self.released_msg = params['RELEASED_MSG']
    self.multi_msg = params['MULTI_MSG']
    self.long_msg = params['LONG_MSG']
# async polling
    self.debounce_time = params['DEBOUNCE_TIME']
    self._rest_state = pin.value()
    self._previous_state = pin.value()
    self._current_state = pin.value()
    self._previous_debounced_state = pin.value()
    self._current_debounced_state = pin.value()
    self._last_check_tick = entities.UTIME.ticks_ms()
# IRQ polling
    self.debounce_threshold = params['DEBOUNCE_TIME'] / entities.DEFAULT_CYCLE
    self._tick_increment = 0
    self._tick_count = 0
# Parsing logic
    self.multi_threshold = params['MULTI_TIME'] / entities.DEFAULT_CYCLE
    self._multi_count:int = 0
    self._multi_tick:int = 0
    self._press_count:int = 0
    self.long_threshold = params['LONG_TIME'] / entities.DEFAULT_CYCLE
    self._long_count:int = 0
    self._long_tick:int = 0

  def on(self, event:str, callback:callable):
      '''Registers an event with a list of callbacks.'''

      if event not in self._callbacks:
          self._callbacks[event] = []

      self._callbacks[event].append(callback)
        
  def off_callback(self, event:str, callback:callable):
      '''Remove a specific callback for an event.'''

      if event in self._callbacks:
          self._callbacks[event].remove(callback)

  def off_event(self, event:int):
      '''Remove all the callbacks for an event.'''
      
      self._callbacks.pop(event, None)

  def off_all(self):
      '''Remove all the callbacks for all the events.'''

      self._callbacks = {}

  def _irq_handler(self, pin):
    '''uPython wants pin.'''

    self._tick_increment = 1

  def _irq_parse(self):

  # On Press
    if self._current_debounced_state != self._rest_state:
      self._long_tick = 1
      self._multi_tick = 0 # Stops the _multi_counter
      self._press_count += 1
      return
  # On release
    self._long_tick = 0
    self._long_count = 0
    self._multi_tick = 1 # Starts the _multi_counter

  def _irq_counter(self):

    self._tick_count += self._tick_increment
    if self._tick_count >= self.debounce_threshold:
      self._tick_increment = 0
      self._tick_count = 0
      self._current_debounced_state = self.pin.value()
      self._irq_parse()

  def _uasyncio_debounce(self):

    ms_now = entities.UTIME.ticks_ms()
    self._current_state = self.pin.value()
    state_changed = self._current_state != self._previous_state
    if state_changed:
      self._last_check_tick = ms_now
    state_stable = (ms_now - self._last_check_tick) > self.debounce_time
    if state_stable and not state_changed:
      self._last_check_tick = ms_now
      self._current_debounced_state = self._current_state
    self._previous_state = self._current_state

  def _uasyncio_parse(self):

  # Did anything change?
    if self._current_debounced_state == self._previous_debounced_state:
      return
  # On Press
    if self._current_debounced_state != self._rest_state:
      self._long_tick = 1
      self._multi_tick = 0 # Stops the _multi_counter
      self._press_count += 1
      self._previous_debounced_state = self._current_debounced_state
      return
  # On release
    self._long_tick = 0
    self._long_count = 0
    self._multi_tick = 1 # Starts the _multi_counter
    self._previous_debounced_state = self._current_debounced_state

  def _multi_counter(self):
    '''Single or multiple releases.'''

  # Start on release, stop on press.
    self._multi_count += self._multi_tick
    if self._multi_count >= self.multi_threshold:
      if self._press_count == 1:
        self._working_event = self.RELEASE
        self._run_callbacks(name=self.name, message=self.released_msg)
      if self._press_count > 1:
        self._working_event = self.MULTI
        self._run_callbacks(name=self.name, message=self.multi_msg)
      self._multi_tick = 0
      self._multi_count = 0
      self._press_count = 0
      self._long_tick = 0
      self._long_count = 0

  def _long_counter(self):
    '''Long press.'''
    
  # Start on press, stop on release.
    self._long_count += self._long_tick
    if self._long_count >= self.long_threshold:
      self._working_event = self.LONG
      self._run_callbacks(name=self.name, message=self.long_msg)
      self._multi_tick = 0
      self._multi_count = 0
      self._press_count = 0
      self._long_tick = 0
      self._long_count = 0

  def _run_callbacks(self, name:str, message:str):

      if not self._working_event:
          return

      if self._working_event not in self._callbacks:
          return
      
      for callback in self._callbacks[self._working_event]:
          try:
              callback(name, message)

          except Exception as e:
              entities.LOGGING_MESSAGE = [f'Name:{__name__}._callbacks(), Listener:{callback}, Error:{e}']
              entities.log()

  def poll(self):

    if self.irq_polling:
      self._irq_poll()
    else:
      self._asyncio_poll()

# Poll() picks one of these to put into an uasyncio loop
  def _irq_poll(self):
    '''IRQ triggers the button action.'''
    self._irq_counter()
    self._multi_counter()
    self._long_counter()

  def _asyncio_poll(self):
    '''uasyncio polling triggers the button action.'''
    self._uasyncio_debounce()
    self._uasyncio_parse()
    self._multi_counter()
    self._long_counter()
