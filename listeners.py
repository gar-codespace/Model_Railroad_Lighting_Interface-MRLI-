'''
All the buttons that turn the led banks and layout scenic lighting on or off.
'''

import entities


def BANK_0_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['BANK_0_S']).toggle()
        entities.STATIC['BANK_0'][index] = entities.PIN(entities.PICO_PIN['BANK_0_S']).value()
        print('button 0 released')

def BANK_1_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]
        
        entities.PIN(entities.PICO_PIN['BANK_1_S']).toggle()
        entities.STATIC['BANK_1'][index] = entities.PIN(entities.PICO_PIN['BANK_1_S']).value()
        print('button 1 released')

def BANK_2_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['BANK_2_S']).toggle()
        entities.STATIC['BANK_2'][index] = entities.PIN(entities.PICO_PIN['BANK_2_S']).value()
        print('button 2 released')

def BANK_3_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['BANK_3_S']).toggle()
        entities.STATIC['BANK_3'][index] = entities.PIN(entities.PICO_PIN['BANK_3_S']).value()
        print('button 3 released')

def BANK_4_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['BANK_4_S']).toggle()
        entities.STATIC['BANK_4'][index] = entities.PIN(entities.PICO_PIN['BANK_4_S']).value()
        print('button 4 released')

def scenic_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        index = entities.CURRENT_EFFECT[2]

        entities.PIN(entities.PICO_PIN['SCENIC_S']).toggle()
        entities.STATIC['SCENIC'][index] = entities.PIN(entities.PICO_PIN['SCENIC_S']).value()
        print('button scenic released')
