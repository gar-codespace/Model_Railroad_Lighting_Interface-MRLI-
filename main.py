import entities
import model
import controls
import handlers

# Coroutine: runs the selected method
async def confirm_button():
    while True:
        await entities.ASYNCIO.sleep(0.2)

async def back_button():
    while True:
        await entities.ASYNCIO.sleep(0.2)

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
    
    dm = controls.DisplayModule()
    dm.show_status_screen()
    entities.SCREEN_STATUS = 'STATUS'

    # model.play harbor sounds

    # create buttons
    entities.Button(entities.PICO_PIN['CONFIRM'], "Confirm", handler=handlers.ConfirmHandler())
    entities.Button(entities.PICO_PIN['BACK'], "Back", handler=handlers.BackHandler())
    entities.Button(entities.PICO_PIN['BANK0_B'], "Bank0", handler=handlers.Bank0Handler())
    entities.Button(entities.PICO_PIN['BANK1_B'], "Bank1", handler=handlers.Bank1Handler())
    entities.Button(entities.PICO_PIN['BANK2_B'], "Bank2", handler=handlers.Bank2Handler())

    routine = model.Routine()
    entities.ASYNCIO.create_task(routine.run_routine())

    while True:
        
        await entities.ASYNCIO.gather(dm.get_encoder().async_tick(),
                                      confirm_button(),
                                      bank0_button(),
                                      bank1_button(),
                                      bank2_button()
                                      )


entities.ASYNCIO.run(main())