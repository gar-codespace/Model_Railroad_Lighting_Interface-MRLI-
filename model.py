import entities

def play_routine(routine):

    r = entities.ROUTINES[routine].upper()
    play_parameters = getattr(entities, r, entities.DAYTIME)

    print(play_parameters)