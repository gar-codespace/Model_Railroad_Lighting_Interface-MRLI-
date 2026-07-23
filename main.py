import entities
import controls

async def main():

    ui = controls.UserInterface()
    # controls.play harbor sounds

    while True:
        
        await entities.ASYNCIO.gather(ui.get_encoder().async_tick(),
                                      # ui.get_confirm_button(),
                                      # ui.get_back_button(),
                                      ui.get_bank_buttons()
                                      )

entities.ASYNCIO.run(main())