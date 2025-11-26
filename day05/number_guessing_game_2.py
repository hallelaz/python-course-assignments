import random
random_number = random.randint(1, 20)

while True:
    guess = input("guess the number (or 'x' to exit): ")

    if guess == "x" or guess == "X":
        print("you left the game")
        break

    guess = int(guess)

    if guess < random_number:
        print("too small")
    elif guess > random_number:
        print("too big")
    else:
        print("you won")
        break