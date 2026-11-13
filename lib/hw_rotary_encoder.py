'''
Hardware library for the rotary encoder.
Rolled up rotary_encoder_rp2.py into this file
Move imports to entities

usage example:
controller.py

    tra = entities.PIN(entities.PICO_PIN['TRA'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
    trb = entities.PIN(entities.PICO_PIN['TRB'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
    psh = entities.PIN(entities.PICO_PIN['PSH'], mode=entities.PIN.IN, pull=entities.PIN.PULL_UP)
    self.encoder = entities.RotaryEncoderRP2(params=entities.ENCODER0, pin_clk=trb, pin_dt=tra, pin_sw=psh)
    self.encoder.on(self.encoder.CW, self.cb_clock_wise)
    self.encoder.on(self.encoder.ACW, self.cb_anti_clock_wise)
    self.encoder.on(self.encoder.CLICK, self.cb_click)
    self.encoder.on(self.encoder.MULTI, self.cb_multi)

entities.py:

    from machine import Pin as PIN
    from machine import Timer as TIMER
    import uasyncio as UASYNCIO
    import utime as UTIME

    ENCODER0 = {
                'DEBOUNCE_MS':50, # filter out pin jitter
                'ENCODER_STEP':1, # filter out pin jitter
                'HALF_STEP':False,# support increment every click for KY040 encoder
                'ONE_STEP_MS':15, # It is a crunch, but it works for now
                'CLICK_MS':400, # detect a single click
                'STEP_MS':200, # detect a multiple press
                'LONG_MS':1000, # detect a long press
                'FAST_MS':50, # detect a fast encoder turn
                }
'''

__fork__ = 'https://github.com/TTitanUA/micropython_rotary_encoder/tree/main'
__refactor__ = 'Greg Ritacco'


# TODO still a lot of nesting


import entities


class RotaryEncoder:
    '''Base class'''

# Events
    CLICK = 'click'
    MULTI = 'multi'
    LONG = 'long'
    RELEASE_MSG = 'rel'
    CW = 'cw'
    CW_FAST = 'cwf'
    CW_HOLD = 'cwh'
    CW_FAST_HOLD = 'cwfh'
    ACW = 'acw'
    ACW_FAST = 'acwf'
    ACW_HOLD = 'acwh'
    ACW_FAST_HOLD = 'acwfh'

    _listeners:dict = {}
# Parsing and debounce logic
    _enc_last_event_ms:int = 0
    _enc_last_direction:int = 0
    _enc_last_status:int = 0
    _flag_last_event:int = 0
    _sw_last_event_ms:int = 0
    _sw_prev_event_ms:int = 0
    _sw_prev_state:bool = False
    _sw_last_state:bool = False
    _sw_held_with_encoder:bool = False
    _sw_held:bool = False
    _sw_clicks:int = 0

    def __init__(
            self,
            pin_clk:entities.PIN = None,
            pin_dt:entities.PIN = None,
            pin_sw:entities.PIN = None,
        # Passed in by params
            debounce_ms:int = 0,
            encoder_step:int = 0,
            half_step:bool = False, # support increment every click for KY040 encoder
            hold_ms:int = 0,
            step_ms:int = 0,
            fast_ms:int = 0,
            click_ms:int = 0,
            one_step_ms:int = 0
    ):
        self.pin_clk = pin_clk
        self.pin_dt = pin_dt
        self.pin_sw = pin_sw
        self.sw_debounce_ms = debounce_ms
        self.enc_step = encoder_step
        self.half_step=half_step
        self.sw_hold_ms = hold_ms
        self.sw_step_ms = step_ms
        self.enc_fast_ms = fast_ms
        self.sw_click_ms = click_ms
        self.one_step_ms = one_step_ms

    def on(self, event:int, callback:callable):
        '''Registers an event with a list of callbacks.'''

        if event not in self._listeners:
            self._listeners[event] = []

        self._listeners[event].append(callback)

    def off_callback(self, event:int, callback:callable):
        '''Remove a specific callback for an event.'''

        if event in self._listeners:
            self._listeners[event].remove(callback)

    def off_event(self, event:int):
        '''Remove all the callbacks for an event.'''
        
        self._listeners.pop(event, None)

    def off_all(self):
        '''Remove all the callbacks for all the events.'''

        self._listeners = {}

    def _sw_irq_handler(self, pin):
        '''Debounce'''

        timestamp = entities.UTIME.ticks_ms()
        c_s = pin.value() == 0

        diff = entities.UTIME.ticks_diff(timestamp, self._sw_last_event_ms)
        if self._sw_last_state == c_s or diff < self.sw_debounce_ms:
            return

        self._sw_prev_state = self._sw_last_state
        self._sw_last_state = c_s
        self._sw_last_event_ms = timestamp

    def _sw_tick_process_event(self):

        __sw_l_s = self._sw_last_state
        __sw_h_w_e = self._sw_held_with_encoder
        __sw_s_ms = self.sw_step_ms
        __sw_l_e_ms = self._sw_last_event_ms
        __sw_p_e_ms = self._sw_prev_event_ms

    # button event already processed
        if self._sw_last_state == self._sw_prev_state:
            return

    # process encoder event with held button
        if self._sw_held_with_encoder and self._sw_last_state:
            return

        elif self._sw_held_with_encoder and not self._sw_last_state:
            self._sw_held_with_encoder = False
            self._sw_last_event_ms = 0
            return

        timestamp = entities.UTIME.ticks_ms()

    # button press
        if self._sw_last_state:
            diff_held = entities.UTIME.ticks_diff(entities.UTIME.ticks_ms(), self._sw_last_event_ms)
            diff_multi = entities.UTIME.ticks_diff(self._sw_last_event_ms, self._sw_prev_event_ms)
        # button held
            if diff_held > self.sw_hold_ms and not self._sw_held:
                self._sw_held = True
                self._flag_last_event = self.LONG
        # it's a multiple click
            elif diff_multi < self.sw_step_ms:
                self._sw_prev_event_ms = 1

            return

    # button release
        if self._sw_held:
            self._sw_held = False
            self._flag_last_event = self.RELEASE_MSG
            self._sw_prev_state = self._sw_last_state

            return

        diff = entities.UTIME.ticks_diff(timestamp, self._sw_last_event_ms)
    # maybe a multiple click, need to wait for the next event
        if diff < self.sw_step_ms:
            if self._sw_prev_event_ms == 1:
                if self._sw_clicks == 0:
                    self._sw_clicks = 1
                self._sw_clicks += 1
            self._sw_prev_event_ms = timestamp

            return        
    # maybe a single click
        if diff < self.sw_click_ms:
            if self._sw_clicks == 0:
                self._flag_last_event = self.CLICK
            else:
                self._flag_last_event = self.MULTI
            self._sw_prev_state = self._sw_last_state

    def _enc_irq_handler(self, pin):
        '''Debounce'''
        
        new_status = (self.pin_dt.value() << 1) | self.pin_clk.value()
        if new_status == self._enc_last_status:
            return

        transition = (self._enc_last_status << 2) | new_status

        if self._sw_last_state:
            self._sw_held_with_encoder = True

        direction = 0
        if (transition == 0b1110) or (self.half_step and (transition == 0b0001)):
            direction = 1
        elif (transition == 0b1101) or (self.half_step and (transition == 0b0010)):
            direction = -1

        if direction != 0:
            self._enc_process_event(direction)

        self._enc_last_status = new_status

    def _enc_process_event(self, direction:int):
        self._enc_last_direction += direction
        self._enc_last_event_ms = entities.UTIME.ticks_ms()

    def _enc_tick_process_turn_event(self):
    # __e_l_d = neg int on left turn, pos int on right turn

        __e_l_d = self._enc_last_direction
        __o_s_m = self.one_step_ms

        if not self.enc_fast_ms:
            fast_turn_count = 4
        else:
            fast_turn_count = (self.enc_fast_ms // __o_s_m)

        if __e_l_d == 1:
            if self._sw_held_with_encoder:
                self._flag_last_event = self.CW_HOLD
            else:
                self._flag_last_event = self.CW

        if __e_l_d == -1:
            if self._sw_held_with_encoder:
                self._flag_last_event = self.ACW_HOLD
            else:
                self._flag_last_event = self.ACW

        if __e_l_d > fast_turn_count:
            if self._sw_held_with_encoder:
                self._flag_last_event = self.CW_FAST_HOLD
            else:
                self._flag_last_event = self.CW_FAST

        if __e_l_d < -fast_turn_count:
            if self._sw_held_with_encoder:
                self._flag_last_event = self.ACW_FAST_HOLD
            else:
                self._flag_last_event = self.ACW_FAST

        self._enc_last_direction = 0

    def __encoder_has_event(self):

        return self._enc_last_direction >= self.enc_step or self._enc_last_direction <= -self.enc_step

    def __tick(self):
        self._sw_tick_process_event()

        diff = entities.UTIME.ticks_diff(entities.UTIME.ticks_ms(), self._enc_last_event_ms)
        if self.__encoder_has_event() and diff > self.enc_fast_ms:

            self._enc_tick_process_turn_event()

        if not self._flag_last_event:
            return

        self.__call_listeners()

        if self._flag_last_event == self.MULTI:
            self._sw_clicks = 0

        self._flag_last_event = 0

    def __call_listeners(self):

        if not self._flag_last_event:
            return

        if self._flag_last_event not in self._listeners:
            return
        
        for listener in self._listeners[self._flag_last_event]:
            try:
                listener(self._sw_clicks)

            except Exception as e:
                print(f'Name:{__name__}.__call_listeners(), Listener:{listener}, Error:{e}')


class RotaryEncoderRP2(RotaryEncoder):
    timer:entities.TIMER = None
    alive:bool = True

    def __init__(
            self,
            params:dict,
            pin_clk:entities.PIN = None,
            pin_dt:entities.PIN = None,
            pin_sw:entities.PIN = None,
            ):

        super().__init__(
            pin_clk=pin_clk,
            pin_dt=pin_dt,
            pin_sw=pin_sw,
            debounce_ms=params['DEBOUNCE_MS'],
            encoder_step=params['ENCODER_STEP'],
            half_step=params['HALF_STEP'],
            hold_ms=params['LONG_MS'],
            step_ms=params['STEP_MS'],
            fast_ms=params['FAST_MS'],
            click_ms=params['CLICK_MS'],
            one_step_ms=params['ONE_STEP_MS']
            )

        self._enable_irq()

    def _enable_irq(self):
        '''For this version of uPython, trigger is passed in automatically.'''
        if self.pin_clk and self.pin_dt:
            # self.pin_clk.irq(trigger=entities.PIN.IRQ_FALLING | entities.PIN.IRQ_RISING, handler=self._enc_irq_handler)
            # self.pin_dt.irq(trigger=entities.PIN.IRQ_FALLING | entities.PIN.IRQ_RISING, handler=self._enc_irq_handler)
            self.pin_clk.irq(handler=self._enc_irq_handler)
            self.pin_dt.irq(handler=self._enc_irq_handler)

        if self.pin_sw:
            # self.pin_sw.irq(trigger=entities.PIN.IRQ_FALLING | entities.PIN.IRQ_RISING, handler=self._sw_irq_handler)
            self.pin_sw.irq(handler=self._sw_irq_handler)

    def deactivate(self):

        self.alive = False

        if self.timer:
            self.timer.deinit()

# Call one of these, depending upon how this library is being used.
# __tick() is used to process the encoder events.

    async def async_tick(self, timeout=20):
        '''This should be run by entities.UASYNCIO.'''

        while True:
            if self.alive:
                self.__tick()
            await entities.UASYNCIO.sleep_ms(timeout)

    def timer_tick(self, timeout=20):
        '''https://docs.micropython.org/en/latest/rp2/quickref.html#timers'''
        
        self.timer = entities.TIMER(-1, period=timeout, mode=entities.TIMER.PERIODIC, callback=lambda t:self.__tick())

    def poll(self):
        '''This should be used in an external uasyncio loop.'''
        self.__tick()
