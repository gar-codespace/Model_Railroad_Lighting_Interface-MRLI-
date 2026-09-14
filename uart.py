import entities
import sound



# Move these to controls
sfx = sound.get_sound_card(uart=entities.UART0, board=entities.SB0)
sfx.initialize_board()
# sfx.reset()

# Move these to sound

# sfx.increment_up()
sfx_group = entities.A3
group_count = len(sfx_group)
selected = entities.RANDINT(0, group_count - 1)
selected = sfx_group[selected]

clip = entities.SFX_LIBRARY[selected][0]
duration = entities.SFX_LIBRARY[selected][1]
description = entities.SFX_LIBRARY[selected][2]
sfx.play_now(clip)
print(f'{description}, {duration} sec')
