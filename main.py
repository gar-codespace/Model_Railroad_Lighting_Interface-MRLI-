import entities
import controls
import model

dm = controls.ControlInterface()

# model.play harbor sounds

async def main():

    #routine = model.Routine()
    #entities.ASYNCIO.create_task(routine.run_routine())

    while True:
        
        await entities.ASYNCIO.gather(dm.get_encoder().async_tick())


entities.ASYNCIO.run(main())