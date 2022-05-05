import random
print("Welcome to Rock, Paper, Scissors! Press Enter to start.")
input()
win_list = [0, 0]
# win_list[0] is computer's win count
# win_list[1] is player's win count
choice_list = ['rock', 'paper', 'scissors']
yn_list = ["Y", "N"]
while True:
    player = None
    computer = random.choice(choice_list)
    while player not in choice_list:
        player = input("Let's start ! Rock, Paper, or Scissors?  ").lower()
        if player not in choice_list:
            print("Please enter the valid words!")
    print('\n ')
    print("Your choice: " + player)
    print("Computer's choice: " + computer)
    if player == computer:
        print("\n It's a tie!")
    if player == "rock":
        if computer == "paper":
            win_list[0] += 1
            print("You lose!")
        elif computer == "scissors":
            win_list[1] += 1
            print("You win!")
    elif player == "paper":
        if computer == "scissors":
            win_list[0] += 1
            print("You lose!")
        elif computer == "rock":
            win_list[1] += 1
            print("You win!")
    elif player == "scissors":
        if computer == "rock":
            win_list[0] += 1
            print("You lose!")
        elif computer == "paper":
            win_list[1] += 1
            print("You win!")
    print()
    print("You have ", win_list[1], "wins.")
    print("Computer has ", win_list[0], "wins.")
    print()
    play_agian = None
    while play_agian not in yn_list:
        play_agian = input("Play again? (Y/N)").upper()
    if play_agian == "N":
        print("--------------------------------------------")
        break
    print("--------------------------------------------")
