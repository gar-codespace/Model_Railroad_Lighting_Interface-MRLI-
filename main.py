import entities
import controls

async def main():

    ui = controls.UserInterface()
    #pwm = entities.PWM(entities.PIN(15), freq=1000)
    #pwm.duty_u16(25000)
    # controls.play harbor sounds

    while True:
        
        await entities.ASYNCIO.gather(ui.get_encoder().async_tick(),
                                      ui.get_confirm_button(),
                                      # ui.get_back_button(),
                                      ui.get_led_bank_buttons(),
                                      )

entities.ASYNCIO.run(main())