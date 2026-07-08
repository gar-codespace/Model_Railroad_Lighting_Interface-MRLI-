import entities
import model
import interface

async def main():
    
    # the display, the rotary encoder and selector button
    control_interface = interface.Controller(entities.P_ROTARY).get_interface()
    
    entities.ASYNCIO.create_task(model.run_routine())
    
    while True:
        
        await control_interface.async_tick()


entities.ASYNCIO.run(main())