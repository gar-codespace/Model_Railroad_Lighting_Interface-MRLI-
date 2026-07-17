import entities


class Bank0Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['BANK0_S']).toggle()

class Bank1Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['BANK1_S']).toggle()
            
class Bank2Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['BANK2_S']).toggle()


class Bank3Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['BANK3_S']).toggle()



class Bank4Handler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['BANK4_S']).toggle()


class ScenicHandler:
    def buttonPressed(self, name):
        print(f"Handler: Button {name} pressed")
    def buttonReleased(self, name):
        print(f"Handler: Button {name} released")
        if entities.SCREEN_STATUS == 'STATUS':
            entities.PIN(entities.PICO_PIN['SCENIC_S']).toggle()