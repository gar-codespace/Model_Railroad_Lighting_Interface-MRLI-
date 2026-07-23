'''
The confirm and back buttons on the control module.
All the buttons that turn the led banks and layout scenic lighting
on or off are here.

Maybe move the get functions to the UI???
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

def get_bank0(): 
    b = entities.Button(entities.PICO_PIN['BANK0_B'], True, bank0_button_listener)
    while(True):
        b.update()
        await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

def bank0_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK0_S']).toggle()
            print('button 0 released')

def get_bank1():
    b = entities.Button(entities.PICO_PIN['BANK1_B'], True, bank1_button_listener)
    while(True):
        b.update()
        await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

def bank1_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK1_S']).toggle()
            print('button 1 released')

def get_bank2():
    b = entities.Button(entities.PICO_PIN['BANK2_B'], True, bank2_button_listener)
    while(True):
        b.update()
        await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

def bank2_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK2_S']).toggle()
            print('button 2 released')

def get_bank3():
    b = entities.Button(entities.PICO_PIN['BANK3_B'], True, bank3_button_listener)
    while(True):
        b.update()
        await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

def bank3_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK3_S']).toggle()
            print('button 3 released')

def get_bank4():
    b = entities.Button(entities.PICO_PIN['BANK4_B'], True, bank4_button_listener)
    while(True):
        b.update()
        await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

def bank4_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['BANK4_S']).toggle()
            print('button 4 released')

def get_scenic():
    b = entities.Button(entities.PICO_PIN['SCENIC_S'], True, scenic_button_listener)
    while(True):
        b.update()
        await entities.ASYNCIO.sleep_ms(entities.DEFAULT_TICK)

def scenic_button_listener(button, event):
    if event == entities.Button.PRESSED:
        pass
    if event == entities.Button.RELEASED:
        if entities.SCREEN_MODE == 'MANUAL' or entities.SCREEN_MODE == 'ADJUST':
            entities.PIN(entities.PICO_PIN['SCENIC_S']).toggle()
            print('button scenic released')
