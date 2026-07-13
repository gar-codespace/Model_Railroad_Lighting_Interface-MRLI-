import entities
import model
import controls

#add a definition for each button
# Coroutine: runs the selected method
async def confirm_button():
    while True:
        await entities.ASYNCIO.sleep(0.2)

# async def back_button():
#     while True:
#         await entities.ASYNCIO.sleep(0.2)

async def bank0_button():
    while True:
        await entities.ASYNCIO.sleep(0.2)

async def bank1_button():
    while True:
        await entities.ASYNCIO.sleep(0.2)

async def bank2_button():
    while True:
        await entities.ASYNCIO.sleep(0.2)

async def main():
    
    # dm = controls.DisplayModule() # display and encoder
    # dm.display_splash()
    
    main_display = controls.Display(entities.MAIN_DISPLAY_PARAMETERS).get_display()
    controls.DisplayScreens(main_display).welcome_screen()



    # create buttons
    entities.Button(entities.PICO_PIN['CONFIRM'], "Confirm", handler=controls.ConfirmHandler())
    entities.Button(entities.PICO_PIN['BACK'], "Back", handler=controls.BackHandler())
    entities.Button(entities.PICO_PIN['BANK0_B'], "Bank0", handler=controls.Bank0Handler())
    entities.Button(entities.PICO_PIN['BANK1_B'], "Bank1", handler=controls.Bank1Handler())
    entities.Button(entities.PICO_PIN['BANK2_B'], "Bank2", handler=controls.Bank2Handler())

    routine = model.Routine()
    entities.ASYNCIO.create_task(routine.run_routine())

    model.scenic_lights()

    # model.play harbor sounds
    
    while True:
        
        await entities.ASYNCIO.gather(controls.Encoder().get_interface().async_tick(),
                                      confirm_button(),
                                      bank0_button(),
                                      bank1_button(),
                                      bank2_button()
                                      )


entities.ASYNCIO.run(main())