import entities


class RunRoutine():

    def __init__(self, routine):
        # routine is passed in as an integer, the key of the ROUTINES library

        # Switch control
        self.p_switches = entities.P_SWITCHES
        self.switch0 = entities.PIN(self.p_switches[0], entities.PIN.OUT)
        self.switch1 = entities.PIN(self.p_switches[1], entities.PIN.OUT)
        self.switch2 = entities.PIN(self.p_switches[2], entities.PIN.OUT)
        self.switch3 = entities.PIN(self.p_switches[3], entities.PIN.OUT)
        self.switch4 = entities.PIN(self.p_switches[4], entities.PIN.OUT)
        self.switch5 = entities.PIN(self.p_switches[5], entities.PIN.OUT) # the lights in the model buildings

        # LED Control
        self.p_leds = entities.P_LEDS
        self.red = entities.PIN(self.p_leds['red'])
        self.green = entities.PIN(self.p_leds['green'])
        self.blue = entities.PIN(self.p_leds['blue'])
        self.warm = entities.PIN(self.p_leds['warm'])
        self.white = entities.PIN(self.p_leds['white'])

        # Routine
        self.routine = entities.ROUTINES[routine]
        r = entities.ROUTINES[routine].upper()
        self.run_parameters = getattr(entities, r, 'Daytime')

        self.name = self.run_parameters['name']
        self.duration = self.run_parameters['duration'] * 60 # Seconds
        self.loop = self.run_parameters['loop']

    def start_switches(self):

        self.switch0.value(self.run_parameters['bank0'][0])
        self.switch1.value(self.run_parameters['bank1'][0])
        self.switch2.value(self.run_parameters['bank2'][0])
        self.switch3.value(self.run_parameters['bank3'][0])
        self.switch4.value(self.run_parameters['bank4'][0])
        self.switch5.value(self.run_parameters['lights'][0])

    def start_leds(self):

        self.red.value(self.routine['red'][0])
        self.green.value(self.routine['green'][0])
        self.blue.value(self.routine['blue'][0])
        self.warm.value(self.routine['warm'][0])
        self.white.value(self.routine['white'][0])

    def run(self):

        self.start_switches()
        #self.start_leds()

        # midpoint = (self.duration / 2) - 2
        #entities.UTIME.sleep(1)
        print(self.run_parameters['name'])
        print(self.run_parameters['duration'])
        print(self.run_parameters['loop'])
