import random

MIN_NUMBER = 1
MAX_NUMBER = 20

def NEW_GAME():
    return {
        "NUMBER": random.randint(MIN_NUMBER, MAX_NUMBER),
        "DEBUG": False
    }

def CHECK_GUESS(GUESS, GAME_STATE):
    NUMBER = GAME_STATE["NUMBER"]

    if GUESS < NUMBER:
        return "TOO SMALL"
    elif GUESS > NUMBER:
        return "TOO BIG"
    else:
        return "YOU WON"

def TOGGLE_DEBUG(GAME_STATE):
    GAME_STATE["DEBUG"] = not GAME_STATE["DEBUG"]

def MOVE_NUMBER(GAME_STATE):
    GAME_STATE["NUMBER"] -= random.randint(-2, 2)

def RESET_NUMBER(GAME_STATE):
    GAME_STATE["NUMBER"] = random.randint(MIN_NUMBER, MAX_NUMBER)
