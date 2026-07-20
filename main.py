import entities
import controls

ui = controls.UserInterface()

# controls.play harbor sounds

async def main():

    entities.ASYNCIO.create_task(ui.run_effect())

    while True:
        
        await entities.ASYNCIO.gather(ui.get_encoder().async_tick())


entities.ASYNCIO.run(main())