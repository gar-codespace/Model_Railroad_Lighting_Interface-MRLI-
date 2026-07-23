import entities
import controls
import listeners


async def main():

    ui = controls.UserInterface()
    # controls.play harbor sounds

    while True:
        
        await entities.ASYNCIO.gather(ui.get_encoder().async_tick(),
                                      ui.get_confirm(),
                                      # ui.get_back(),
                                      listeners.get_bank0(),
                                      listeners.get_bank1(),
                                      listeners.get_bank2(),
                                      listeners.get_bank3(),
                                      listeners.get_bank4(),
                                      listeners.get_scenic())



entities.ASYNCIO.run(main())