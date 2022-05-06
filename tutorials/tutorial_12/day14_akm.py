import time
import datetime


def count_up():
    start_time = 0
    stop_time = 0
    while True:
        try:
            start_time = int(input("Enter start time (sec): "))
            stop_time = int(input("Enter end time (sec): "))
            if stop_time <= 0 or start_time <= 0:
                print("The input time should be positive number!")
                continue
            break
        except ValueError:
            print("Enter the valid numbers only!!")
            continue
    for i in range(start_time, stop_time + start_time, 1):
        print(str(datetime.timedelta(seconds=i)))
        time.sleep(1)
    print("Time's up!")


def count_down():
    start_time = 0
    stop_time = 0
    while True and start_time <= 0 and start_time - stop_time <= 0:
        try:
            start_time = int(input("Enter start time (sec): "))
            stop_time = int(input("Enter end time (sec): "))
            if stop_time < 0 or start_time < 0:
                print("The input time should be positive number!")
                continue
            if start_time <= 0 or start_time - stop_time < 0:
                print("Start time should not be zero and \
(start time - end time) should not be zero or less than zero!")
                start_time = 0
                stop_time = 0
                continue
            break
        except ValueError:
            print("Enter the valid numbers only!!")
            continue
    for i in range(start_time, start_time-stop_time, -1):
        print(str(datetime.timedelta(seconds=i)))
        time.sleep(1)
    print("Time's up!")


check_list = ['yes', 'no', 1, 2]
while True:
    user_choice = 0
    while user_choice not in check_list:
        try:
            user_choice = int(input("Enter 1 for Count Up Timer and \
Enter 2 for Count Down Timer: "))
        except ValueError:
            print("It is not the number.", end=" ")
        if user_choice not in check_list:
            print("Please enter a valid key (1 or 2)!")
    if user_choice == 1:
        count_up()
    else:
        count_down()
    do_again = None
    while do_again not in check_list:
        do_again = input("Do you want to use \
the program again? (yes/no):").lower()
        if do_again not in check_list:
            print("Plese enter yes or no word only!")
    if do_again == 'no':
        break
