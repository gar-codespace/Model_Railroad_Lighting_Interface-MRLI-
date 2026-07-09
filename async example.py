import entities
import model
import interface

async def main():
    
    # the display, the rotary encoder and selector button
    control_interface = interface.Controller(entities.P_ROTARY).get_interface()
    
    routine = model.Routine()
    entities.ASYNCIO.create_task(routine.run_routine())

    # play harbor sounds
    
    while True:
        
       
        await control_interface.async_tick()


entities.ASYNCIO.run(main())