import entities
import model
import display_module

#add a definition for each button
# Coroutine: runs the selected method
async def confirm_button():
    while True:
        await entities.ASYNCIO.sleep(0.1)
# Coroutine: runs the selected method
async def back_button():
    while True:
        await entities.ASYNCIO.sleep(0.1)

async def main():
    
    # the display, the rotary encoder and selector button
    dm = display_module.DisplayModule()
    dm.display_splash()

    # create additional buttons
    entities.Button(entities.PICO_PIN['CONFIRM'], "Confirm", handler=model.ConfirmHandler())
    entities.Button(entities.PICO_PIN['BACK'], "Back", handler=model.BackHandler())

    routine = model.Routine()
    entities.ASYNCIO.create_task(routine.run_routine())

    # play harbor sounds
    
    while True:
        
        await entities.ASYNCIO.gather(dm.get_interface().async_tick(),
                                      confirm_button(),
                                      back_button()
                                      )


entities.ASYNCIO.run(main())