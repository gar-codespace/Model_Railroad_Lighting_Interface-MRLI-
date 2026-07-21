import entities

def bank0_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL':
            entities.PIN(entities.PICO_PIN['BANK0_S']).toggle()

def bank1_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL':
            entities.PIN(entities.PICO_PIN['BANK1_S']).toggle()

def bank2_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL':
            entities.PIN(entities.PICO_PIN['BANK2_S']).toggle()

def bank3_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL':
            entities.PIN(entities.PICO_PIN['BANK3_S']).toggle()

def bank4_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL':
            entities.PIN(entities.PICO_PIN['BANK4_S']).toggle()

def scenic_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL':
            entities.PIN(entities.PICO_PIN['SCENIC_S']).toggle()