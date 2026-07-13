import entities

# the left and right listeners are swapped
def turn_left_listener():
    print('Left')

def turn_right_listener():
    print('Right')

def single_click_listener():
        print('Select')

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
