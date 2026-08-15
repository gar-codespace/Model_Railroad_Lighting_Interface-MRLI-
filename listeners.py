'''
All the buttons that turn the led banks and layout scenic lighting
on or off are here.
'''

import entities


def bank0_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['BANK0_S']).toggle()
        entities.STATIC['BANK0'][index] = entities.PIN(entities.PICO_PIN['BANK0_S']).value()
        print('button 0 released')

def bank1_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]
        
        entities.PIN(entities.PICO_PIN['BANK1_S']).toggle()
        entities.STATIC['BANK1'][index] = entities.PIN(entities.PICO_PIN['BANK1_S']).value()
        print('button 1 released')

def bank2_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['BANK2_S']).toggle()
        entities.STATIC['BANK2'][index] = entities.PIN(entities.PICO_PIN['BANK2_S']).value()
        print('button 2 released')

def bank3_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['BANK3_S']).toggle()
        entities.STATIC['BANK3'][index] = entities.PIN(entities.PICO_PIN['BANK3_S']).value()
        print('button 3 released')

def bank4_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['BANK4_S']).toggle()
        entities.STATIC['BANK4'][index] = entities.PIN(entities.PICO_PIN['BANK4_S']).value()
        print('button 4 released')

def scenic_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['SCENIC_S']).toggle()
        entities.STATIC['SCENIC'][index] = entities.PIN(entities.PICO_PIN['SCENIC_S']).value()
        print('button scenic released')
