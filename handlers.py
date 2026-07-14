import entities


# make a handler for each button
class ConfirmHandler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.CURRENT_ROUTINE == 1 or entities.CURRENT_ROUTINE == 2:
            entities.PIN(entities.PICO_PIN['SCENIC']).toggle()

class BackHandler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")

class Bank0Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.CURRENT_ROUTINE == 1:
            entities.PIN(entities.PICO_PIN['BANK0']).toggle()

class Bank1Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.CURRENT_ROUTINE == 1:
            entities.PIN(entities.PICO_PIN['BANK1']).toggle()
            
class Bank2Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.CURRENT_ROUTINE == 1:
            entities.PIN(entities.PICO_PIN['BANK2']).toggle()


    # Left over from the encoder class. These are not used
    # def any_event_listener(self, event, clicks):
    #     print(f"ANY Event ID: {event} Clicks: {clicks}")
# 
    # def turn_left_fast_listener(self):
    #     print(f"Turn Left Fast")
# 
    # def turn_right_fast_listener(self):
    #     print(f"Turn Right Fast")
    # 
    # def multy_click_listener(self, clicks):
    #     print(f"Multiply Clicks: {clicks}")
# 
    # def held_listener(self):
    #     print(f"Held")
# 
    # def released_listener(self):
    #     print(f"Released")
