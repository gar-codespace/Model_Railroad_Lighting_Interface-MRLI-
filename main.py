import entities
import model
import controls

#add a definition for each button
# Coroutine: runs the selected method
async def confirm_button():
    while True:
        await entities.ASYNCIO.sleep(0.2)
# Coroutine: runs the selected method
async def back_button():
    while True:
        await entities.ASYNCIO.sleep(0.2)

async def main():
    
    # the display and the rotary encoder
    dm = controls.DisplayModule()
    dm.display_splash()

    # create buttons
    entities.Button(entities.PICO_PIN['CONFIRM'], "Confirm", handler=controls.ConfirmHandler())
    entities.Button(entities.PICO_PIN['BACK'], "Back", handler=controls.BackHandler())

    routine = model.Routine()
    entities.ASYNCIO.create_task(routine.run_routine())

    model.building_lights()

    # model.play harbor sounds
    
    while True:
        
        await entities.ASYNCIO.gather(dm.get_interface().async_tick(),
                                      confirm_button(),
                                      back_button()
                                      )


entities.ASYNCIO.run(main())