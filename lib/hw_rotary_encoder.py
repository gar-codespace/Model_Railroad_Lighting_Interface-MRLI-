'''
Hardware library for the rotary encoder.
Rolled up rotary_encoder_rp2.py into this file
timeout is now based on entities.DEFAULT_CYCLE
Move imports to entities
'''
'''
params:
ENCODER0 = {
            'DEBOUNCE_MS':50, # filter out pin jitter
            'ENCODER_STEP':1, # filter out pin jitter
            'HALF_STEP':False,# support increment every click for KY040 encoder
            'HOLD_MS':1000, # detect a long press
            'STEP_MS':200, # detect a multiple press
            'FAST_MS':50, # detect a fast encoder turn
            'CLICK_MS':400, # detect a single click
            'ONE_STEP_MS':15 # It is a crunch, but it works for now
            }
'''

__fork__ = 'https://github.com/TTitanUA/micropython_rotary_encoder/tree/main'
__refactor__ = 'Greg Ritacco'


# TODO still a lot of nesting


import entities


class RotaryEncoder:
    '''Base class'''

# Events
    CLICK = 2
    MULTIPLE_CLICK = 3
    HELD = 4
    RELEASED_MSG = 5
    TURN_LEFT = 6
    TURN_LEFT_FAST = 7
    TURN_LEFT_HOLD = 8
    TURN_LEFT_FAST_HOLD = 9
    TURN_RIGHT = 10
    TURN_RIGHT_FAST = 11
    TURN_RIGHT_HOLD = 12
    TURN_RIGHT_FAST_HOLD = 13

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

        if event not in self._listeners:
            self._listeners[event] = []

        self._listeners[event].append(callback)

    def off(self, event:int):
        self._listeners.pop(event, None)

    def off_all(self, event:int):
        self._listeners = {}

    def _sw_irq_handler(self, pin):
        '''Debounce'''

        timestamp = entities.UTIME.ticks_ms()
        c_s = pin.value() == 0

        if self._sw_last_state == c_s or entities.UTIME.ticks_diff(timestamp, self._sw_last_event_ms) < self.sw_debounce_ms:
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
        if __sw_l_s == self._sw_prev_state:
            return

    # process encoder event with held button
        if __sw_h_w_e and __sw_l_s:
            return

        elif __sw_h_w_e and not __sw_l_s:
            self._sw_held_with_encoder = False
            self._sw_last_event_ms = 0
            return

        timestamp = entities.UTIME.ticks_ms()

    # button press
        if __sw_l_s:
        # button held
            if entities.UTIME.ticks_diff(entities.UTIME.ticks_ms(), __sw_l_e_ms) > self.sw_hold_ms and not self._sw_held:
                self._sw_held = True
                self._flag_last_event = self.HELD
        # it's a multiple click
            elif entities.UTIME.ticks_diff(__sw_l_e_ms, self._sw_prev_event_ms) < __sw_s_ms:
                self._sw_prev_event_ms = 1

            return
        
    # button release
        if self._sw_held:
            self._sw_held = False
            self._flag_last_event = self.RELEASED_MSG
            self._sw_prev_state = __sw_l_s

            return

    # maybe a multiple click, need wait for the next event
        diff = entities.UTIME.ticks_diff(timestamp, __sw_l_e_ms)
        if diff < __sw_s_ms:
            if __sw_p_e_ms == 1:
                if self._sw_clicks == 0:
                    self._sw_clicks = 1
                self._sw_clicks += 1
            self._sw_prev_event_ms = timestamp

            return
        
    # maybe a single click
        diff = entities.UTIME.ticks_diff(timestamp, __sw_l_e_ms)
        if diff < self.sw_click_ms:
            if self._sw_clicks == 0:
                self._flag_last_event = self.CLICK
            else:
                self._flag_last_event = self.MULTIPLE_CLICK
            self._sw_prev_state = __sw_l_s
    # some old event, skip it
        # else:
        #     self._sw_prev_state = __sw_l_s

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
                self._flag_last_event = self.TURN_RIGHT_HOLD
            else:
                self._flag_last_event = self.TURN_RIGHT

        if __e_l_d == -1:
            if self._sw_held_with_encoder:
                self._flag_last_event = self.TURN_LEFT_HOLD
            else:
                self._flag_last_event = self.TURN_LEFT

        if __e_l_d > fast_turn_count:
            if self._sw_held_with_encoder:
                self._flag_last_event = self.TURN_RIGHT_FAST_HOLD
            else:
                self._flag_last_event = self.TURN_RIGHT_FAST

        if __e_l_d < -fast_turn_count:
            if self._sw_held_with_encoder:
                self._flag_last_event = self.TURN_LEFT_FAST_HOLD
            else:
                self._flag_last_event = self.TURN_LEFT_FAST

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

        if self._flag_last_event == self.MULTIPLE_CLICK:
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
            hold_ms=params['HOLD_MS'],
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
