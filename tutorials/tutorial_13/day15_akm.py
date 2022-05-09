import random


print("\nWelcome from our Number Guessing Game\n")
guess = None
check_num = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
num = 0
i = 3
while True:
    num = random.randrange(0, 11)
    guess = "nothing"
    is_in_range = False
    while not is_in_range:
        guess = input("Enter number: ")
        if guess not in check_num:
            print("Please enter only the integer \
number within the range (0-10)!")
            is_in_range = False
        else:
            is_in_range = True
    if int(guess) == num:
        print("You won. The number is ", num, ".")
    else:
        i -= 1
        if i > 1:
            print("Try again. You have ", i, " \
times left to guess number.")
            continue
        elif i == 1:
            print("Try again. You have ", i, " \
time left to guess number.")
            continue
        elif i == 0:
            print("You lost. You have no time left to guess number.")
            print("The number is ", num, ".")
            i = 3
    while True:
        check_list = ["Y", "N"]
        play_again = input("Do you want to play again? (Y/N): ").upper()
        if play_again not in check_list:
            print("Please enter the valid key!")
            continue
        else:
            break
    if play_again == check_list[1]:
        break
