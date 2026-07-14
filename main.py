import entities
import controls

controls.Buttons()

dm = controls.ControlInterface()

entities.SCREEN_STATUS = 'STATUS'

# model.play harbor sounds

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

    #routine = model.Routine()
    #entities.ASYNCIO.create_task(routine.run_routine())

    while True:
        
        await entities.ASYNCIO.gather(dm.get_encoder().async_tick(),
                                      confirm_button(),
                                      bank0_button(),
                                      bank1_button(),
                                      bank2_button()
                                      )


entities.ASYNCIO.run(main())