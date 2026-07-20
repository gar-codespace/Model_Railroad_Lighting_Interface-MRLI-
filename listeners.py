import entities

def bank0_button_listener(button, event):
    if event == entities.Button.PRESSED:
        print('bank0 button pressed')
    if event == entities.Button.RELEASED:
        print('bank0 button released')