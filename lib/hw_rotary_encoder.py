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
            }
'''

__fork__ = 'https://github.com/TTitanUA/micropython_rotary_encoder/tree/main'
__refactor__ = 'Greg Ritacco'

import entities


class RotaryEncoderEvent:

    # ANY = 1
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


class RotaryEncoder:
    """Base class"""
# Parsing and debounce logic
    _enc_last_event_ms: int = 0
    _enc_last_dir: int = 0
    _enc_last_status: int = 0
    _flag_last_event: int = 0
    _sw_last_event_ms: int = 0
    _sw_prev_event_ms: int = 0
    _sw_prev_state: bool = False
    _sw_last_state: bool = False
    _sw_held_with_encoder: bool = False
    _sw_held: bool = False
    _sw_clicks: int = 0
    _listeners: dict = {}

    def __init__(
            self,
            pin_clk: entities.PIN = None,
            pin_dt: entities.PIN = None,
            pin_sw: entities.PIN = None,
        # Passed in by params
            debounce_ms: int = 0,
            encoder_step: int = 0,
            half_step: bool = False, # support increment every click for KY040 encoder
            hold_ms: int = 0,
            step_ms: int = 0,
            fast_ms: int = 0,
            click_ms: int = 0
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

    def on(self, event: int, callback: callable):
        if event not in self._listeners:
            self._listeners[event] = []

        self._listeners[event].append(callback)

    def off(self, event: int, callback: callable):
        if event in self._listeners:
            self._listeners[event].remove(callback)

    def off_all(self, event: int, callback: callable = None):
        if event in self._listeners:
            if callback is None:
                self._listeners[event] = []
            else:
                while callback in self._listeners[event]:
                    self._listeners[event].remove(callback)

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
    # local cache
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

    # button pressed
        if __sw_l_s:
    # button held
            if entities.UTIME.ticks_diff(entities.UTIME.ticks_ms(), __sw_l_e_ms) > self.sw_hold_ms and not self._sw_held:
                self._sw_held = True
                self._flag_last_event = RotaryEncoderEvent.HELD
    # it's a multiple click
            elif entities.UTIME.ticks_diff(__sw_l_e_ms, self._sw_prev_event_ms) < __sw_s_ms:
                self._sw_prev_event_ms = 1
        else:
    # button release
            if self._sw_held:
                self._sw_held = False
                self._flag_last_event = RotaryEncoderEvent.RELEASED_MSG
                self._sw_prev_state = __sw_l_s
    # maybe a multiple click, need wait for the next event
            elif entities.UTIME.ticks_diff(timestamp, __sw_l_e_ms) < __sw_s_ms:
                if __sw_p_e_ms == 1:
                    if self._sw_clicks == 0:
                        self._sw_clicks = 1
                    self._sw_clicks += 1
                self._sw_prev_event_ms = timestamp
    # maybe a single click
            elif entities.UTIME.ticks_diff(timestamp, __sw_l_e_ms) < self.sw_click_ms:
                # it's a single click
                if self._sw_clicks == 0:
                    self._flag_last_event = RotaryEncoderEvent.CLICK
                else:
                    self._flag_last_event = RotaryEncoderEvent.MULTIPLE_CLICK
                self._sw_prev_state = __sw_l_s
    # some old event, skip it
            else:
                self._sw_prev_state = __sw_l_s

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

    def _enc_process_event(self, direction: int):
        self._enc_last_dir += direction
        self._enc_last_event_ms = entities.UTIME.ticks_ms()

    def _enc_tick_process_turn_event(self):
    # local cache
        __e_l_d = self._enc_last_dir

        # @FIXME: It is a crunch, but it works for now
        # 15ms it's a time for one step
        if self.enc_fast_ms == 0:
            fast_turn_count = 1000
        else:
            fast_turn_count = (self.enc_fast_ms // 15)

        if __e_l_d > 0:
            if __e_l_d > fast_turn_count:
                if self._sw_held_with_encoder:
                    self._flag_last_event = RotaryEncoderEvent.TURN_RIGHT_FAST_HOLD
                else:
                    self._flag_last_event = RotaryEncoderEvent.TURN_RIGHT_FAST
            else:
                if self._sw_held_with_encoder:
                    self._flag_last_event = RotaryEncoderEvent.TURN_RIGHT_HOLD
                else:
                    self._flag_last_event = RotaryEncoderEvent.TURN_RIGHT
        else:
            if __e_l_d < -fast_turn_count:
                if self._sw_held_with_encoder:
                    self._flag_last_event = RotaryEncoderEvent.TURN_LEFT_FAST_HOLD
                else:
                    self._flag_last_event = RotaryEncoderEvent.TURN_LEFT_FAST
            else:
                if self._sw_held_with_encoder:
                    self._flag_last_event = RotaryEncoderEvent.TURN_LEFT_HOLD
                else:
                    self._flag_last_event = RotaryEncoderEvent.TURN_LEFT

        self._enc_last_dir = 0

    def __encoder_has_event(self):
        return self._enc_last_dir >= self.enc_step or self._enc_last_dir <= -self.enc_step

    def __tick(self):
        self._sw_tick_process_event()

        diff = entities.UTIME.ticks_diff(entities.UTIME.ticks_ms(), self._enc_last_event_ms)
        if self.__encoder_has_event() and diff > self.enc_fast_ms:

            self._enc_tick_process_turn_event()

        if not self._flag_last_event:
            return

        self.__call_listeners()

        if self._flag_last_event == RotaryEncoderEvent.MULTIPLE_CLICK:
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
                print(f"RotaryEncoder callback error. Event: {self._flag_last_event}, Listener: {listener}, Error: {e}")


class RotaryEncoderRP2(RotaryEncoder):
    timer: entities.TIMER = None
    alive: bool = True

    def __init__(
            self,
            params:dict,
            pin_clk: entities.PIN = None,
            pin_dt: entities.PIN = None,
            pin_sw: entities.PIN = None,

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

    def __delete__(self, instance):
        self.alive = False

        if self.timer is not None:
            self.timer.deinit()

    def toggle_async(self):
        '''activated async_tick on or off.'''

        self.alive != self.alive

# Call one of these, depending upon how this library is being used.
    async def async_tick(self, timeout=1):
        """async_tick is used to process the encoder events. It should be run by entities.UASYNCIO."""
        timeout = entities.DEFAULT_CYCLE
        while True:
            if self.alive:
                self.__tick()
            await entities.UASYNCIO.sleep_ms(timeout)

    def timer_tick(self, timeout=1):
        """
            timer_tick is used to process the encoder events. It automatically creates the system irq timer.
            :link https://docs.micropython.org/en/latest/rp2/quickref.html#timers
        """
        self.timer = entities.TIMER(-1, period=timeout, mode=entities.TIMER.PERIODIC, callback=lambda t: self.__tick())

    def poll(self):
        """poll should be used in an external uasyncio loop. """
        self.__tick()
