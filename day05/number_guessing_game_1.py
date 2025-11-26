import random
random_number = random.randint(1, 20)
guess = int(input("guess the number:" ))
while random_number != guess :
    if random_number > guess:
        print("too small")
    else:
        print("too big")
    guess = int(input("you can try again"))

print("you won")
