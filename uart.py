import entities
import sound



# Move these to controls
sfx = sound.get_sound_card(uart=entities.UART0, board=entities.SB0)
sfx.vol = 100

# sfx.reset()
sfx.play(0)
