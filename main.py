import entities
import controls

# controls.Buttons()

dm = controls.ControlInterface()

entities.SCREEN_STATUS = 'ROUTINE'

# model.play harbor sounds


async def main():

    #routine = model.Routine()
    #entities.ASYNCIO.create_task(routine.run_routine())

    while True:
        
        await entities.ASYNCIO.gather(dm.get_encoder().async_tick())


entities.ASYNCIO.run(main())