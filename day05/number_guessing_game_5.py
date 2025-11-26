import random
random_number = random.randint(1, 20)
debug_mode = False

while True:
    if debug_mode:
        print(random_number)

    guess = input("guess the number ")

    if guess == "x":
        print("you left the game")
        break

    if guess == "d":
        debug_mode = not debug_mode
        continue

    if guess == "s":
        print (random_number)
        break
    if guess == "m":
        random_number = random_number - random.randint(-2, 2)
        continue

    guess = int(guess)

    if guess < random_number:
        print("too small")
    elif guess > random_number:
        print("too big")
    else:
        print("you won")
        break