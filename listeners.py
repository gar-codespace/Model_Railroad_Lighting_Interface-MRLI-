'''
The confirm and back buttons on the control module.
All the buttons that turn the led banks and layout scenic lighting
on or off are here.
'''

import entities

def confirm_button_listener(button, event):
   if event == entities.Button.PRESSED:
       print(button)
   if event == entities.Button.RELEASED:
       print(button)

def back_button_listener(button, event):
   if event == entities.Button.PRESSED:
       print(button)
   if event == entities.Button.RELEASED:
       print(button)

def bank0_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        print('button 0 released')

def bank1_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK1_S']).toggle()
            print('button 1 released')

def bank2_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK2_S']).toggle()
            print('button 2 released')

def bank3_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK3_S']).toggle()
            print('button 3 released')

def bank4_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK4_S']).toggle()
            print('button 4 released')

def scenic_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['SCENIC_S']).toggle()
            print('button scenic released')
