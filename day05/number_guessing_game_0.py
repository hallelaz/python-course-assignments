import random
random_number = random.randint(1, 20)
guess = int(input("guess the number:" ))

if random_number == guess:
    print ("good guss its the same number")
elif random_number > guess:
    print  ("too small")
elif random_number < guess:
    print  ("too big")

