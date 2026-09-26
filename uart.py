import entities
import sound
import model

tx = entities.PIN(0)
rx = entities.PIN(1)

def get_uart(specs:dict, tx=None, rx=None) -> object:

    id = specs['ID']
    baud = specs['BAUD_RATE']

    uart = entities.UART(id, baudrate=baud, tx=tx, rx=rx)

    return uart




uart_bus = get_uart(entities.UART0, tx=tx, rx=rx)
main_sound_card = sound.get_sound_card(entities.MAIN_SOUND_CARD, uart_bus)



main_sound_card.play_now(entities.WELCOME_CLIP)
