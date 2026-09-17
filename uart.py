import entities
import sound



# Move these to controls
main_sound_card = sound.get_sound_card(entities.MAIN_SOUND_CARD)
main_sound_card.initialize_board()

# Move these to sound


sfx_group = entities.A3
group_count = len(sfx_group)
selected = entities.RANDINT(0, group_count - 1)
selected = sfx_group[selected]

clip = entities.SFX_LIBRARY[selected][0]
duration = entities.SFX_LIBRARY[selected][1]
description = entities.SFX_LIBRARY[selected][2]
main_sound_card.play(clip)

print(f'{description}, {duration} sec')
