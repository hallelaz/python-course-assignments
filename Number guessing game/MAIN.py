import tkinter as tk
from GAME_LOGIC import NEW_GAME, CHECK_GUESS, TOGGLE_DEBUG, MOVE_NUMBER, RESET_NUMBER

GAME_STATE = NEW_GAME()

def SUBMIT_GUESS():
    USER_INPUT = ENTRY.get()

    if USER_INPUT == "":
        RESULT_LABEL.config(text="ENTER A NUMBER")
        return

    try:
        GUESS = int(USER_INPUT)
    except ValueError:
        RESULT_LABEL.config(text="ONLY NUMBERS!")
        return

    RESULT = CHECK_GUESS(GUESS, GAME_STATE)
    RESULT_LABEL.config(text=RESULT)

    if GAME_STATE["DEBUG"]:
        DEBUG_LABEL.config(text=f"DEBUG: {GAME_STATE['NUMBER']}")

def TOGGLE_DEBUG_MODE():
    TOGGLE_DEBUG(GAME_STATE)

    if GAME_STATE["DEBUG"]:
        DEBUG_LABEL.config(text=f"DEBUG: {GAME_STATE['NUMBER']}")
    else:
        DEBUG_LABEL.config(text="")

def MOVE_NUMBER_BUTTON():
    MOVE_NUMBER(GAME_STATE)
    RESULT_LABEL.config(text="NUMBER MOVED")

def RESET_GAME():
    RESET_NUMBER(GAME_STATE)
    RESULT_LABEL.config(text="NEW NUMBER GENERATED")
    DEBUG_LABEL.config(text="")

WINDOW = tk.Tk()
WINDOW.title("NUMBER GUESSING GAME")
WINDOW.geometry("350x300")

TITLE_LABEL = tk.Label(WINDOW, text="GUESS THE NUMBER", font=("Arial", 16))
TITLE_LABEL.pack(pady=10)

ENTRY = tk.Entry(WINDOW)
ENTRY.pack(pady=5)

SUBMIT_BUTTON = tk.Button(WINDOW, text="GUESS", command=SUBMIT_GUESS)
SUBMIT_BUTTON.pack(pady=5)

RESULT_LABEL = tk.Label(WINDOW, text="")
RESULT_LABEL.pack(pady=5)

DEBUG_LABEL = tk.Label(WINDOW, text="", fg="red")
DEBUG_LABEL.pack(pady=5)

DEBUG_BUTTON = tk.Button(WINDOW, text="TOGGLE DEBUG", command=TOGGLE_DEBUG_MODE)
DEBUG_BUTTON.pack(pady=5)

MOVE_BUTTON = tk.Button(WINDOW, text="MOVE NUMBER", command=MOVE_NUMBER_BUTTON)
MOVE_BUTTON.pack(pady=5)

RESET_BUTTON = tk.Button(WINDOW, text="NEW GAME", command=RESET_GAME)
RESET_BUTTON.pack(pady=10)

WINDOW.mainloop()
