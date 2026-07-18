import entities
import controls
import routine

ui = controls.UserInterface()

# controls.play harbor sounds

async def main():

    r = routine.Routine()
    #entities.ASYNCIO.create_task(r.run_standin_routine())
    entities.ASYNCIO.create_task(ui.run_routine())

    while True:
        
        await entities.ASYNCIO.gather(ui.get_encoder().async_tick())


entities.ASYNCIO.run(main())