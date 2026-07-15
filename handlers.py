import entities


# make a handler for each button
# class ConfirmHandler:
#     def buttonPressed(self, name):
#         print(f"Handler: Button {name} pressed")
#     def buttonReleased(self, name):
#         print(f"Handler: Button {name} released")

# class BackHandler:
#     def buttonPressed(self, name):
#         print(f"Handler: Button {name} pressed")
#     def buttonReleased(self, name):
#         print(f"Handler: Button {name} released")

class Bank0Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['BANK0']).toggle()

class Bank1Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['BANK1']).toggle()
            
class Bank2Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['BANK2']).toggle()

class ScenicHandler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['SCENIC']).toggle()