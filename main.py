import entities
import model
import interface

#add a definition for each button
async def confirm_button():
    while True:
        await entities.ASYNCIO.sleep(0.1)

async def back_button():
    while True:
        await entities.ASYNCIO.sleep(0.1)

async def main():
    
    # the display, the rotary encoder and selector button
    control_interface = interface.Controller(entities.P_ROTARY).get_interface()
    # create additional buttons
    interface.Button(entities.P_BUTTONS['confirm'], "Confirm", handler=interface.ConfirmHandler())
    interface.Button(entities.P_BUTTONS['back'], "Back", handler=interface.BackHandler())

    routine = model.Routine()
    entities.ASYNCIO.create_task(routine.run_routine())

    # play harbor sounds
    
    while True:
        
        await entities.ASYNCIO.gather(control_interface.async_tick(),
                                      confirm_button(),
                                      back_button()
                                      )


entities.ASYNCIO.run(main())