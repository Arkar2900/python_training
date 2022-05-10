import random


def req_name():
    print("Player 1")
    p1 = input("Enter the name: ")
    print()
    print()
    print("Player 2: Computer")
    p2 = "Computer"
    return p1, p2


def check_val():
    while True:
        print("Enter 1 for x")
        print("Enter 2 for o")
        print("Enter 3 for Quit")
        val = input()
        if val == '1' or val == '2' or val == '3':
            break
        else:
            print("Please enter the valid key!!!")
            continue
    return val


def com_check_val():
    choices = ['1', '2']
    com_val = random.choice(choices)
    print(com_val)
    return com_val


def show_score(x):
    print('     ----------------------------------')
    print('     		SCOREBOARD')
    print('     ----------------------------------')
    print('     		' + p1 + '     ', x[0])
    print('     		' + p2 + '     ', x[1])


def show_board(a):
    print("\n")
    print("\t     |     |")
    print("\t ", a[0], " | ", a[1], " | ", a[2])
    print('\t_____|_____|_____')
    print("\t     |     |")
    print("\t ", a[3], " | ", a[4], " | ", a[5])
    print('\t_____|_____|_____')
    print("\t     |     |")
    print("\t ", a[6], " | ", a[7], " | ", a[8])
    print("\t     |     |")
    print("\n")


def position_free(y):
    if board_list[y - 1] == ' ':
        return True
    else:
        return False


def req_position():
    global box_num
    while True:
        print("Player " + val + " turn.")
        try:
            box_num = int(input("Which box? : "))
        except ValueError:
            print("This is not a number. Please enter the valid number!")
            continue
        if box_num > 0 and box_num < 10:
            if position_free(box_num):
                board_list[box_num - 1] = val
                break
            else:
                print("This position is not empty!\n \
Please try another position!")
                continue
        else:
            print("Enter the value within the range of 1 - 9 !!!")
            continue


def com_req_position():
    box_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    global box_num
    while True:
        box_num = random.choice(box_list)
        if position_free(box_num):
            board_list[box_num - 1] = val
            break
        else:
            continue


def check_win(list):
    if box_num == 1:
        if(
            list[0] == list[3] and list[0] == list[6] or
            list[0] == list[1] and list[0] == list[2] or
            list[0] == list[4] and list[0] == list[8]
        ):
            return True
    elif box_num == 2:
        if(
            list[1] == list[0] and list[1] == list[2] or
            list[1] == list[4] and list[1] == list[7]
        ):
            return True
    elif box_num == 3:
        if(
            list[2] == list[0] and list[2] == list[1] or
            list[2] == list[4] and list[2] == list[6] or
            list[2] == list[5] and list[2] == list[8]
        ):
            return True
    elif box_num == 4:
        if(
            list[3] == list[0] and list[3] == list[6] or
            list[3] == list[4] and list[3] == list[5]
        ):
            return True
    elif box_num == 5:
        if(
            list[4] == list[0] and list[4] == list[8] or
            list[4] == list[3] and list[4] == list[5] or
            list[4] == list[1] and list[4] == list[7] or
            list[4] == list[2] and list[4] == list[6]
        ):
            return True
    elif box_num == 6:
        if(
            list[5] == list[3] and list[5] == list[4] or
            list[5] == list[2] and list[5] == list[8]
        ):
            return True
    elif box_num == 7:
        if(
            list[6] == list[0] and list[6] == list[3] or
            list[6] == list[4] and list[6] == list[2] or
            list[6] == list[7] and list[6] == list[8]
        ):
            return True
    elif box_num == 8:
        if(
            list[7] == list[1] and list[7] == list[4] or
            list[7] == list[6] and list[7] == list[8]
        ):
            return True
    elif box_num == 9:
        if(
            list[8] == list[0] and list[8] == list[4] or
            list[8] == list[2] and list[8] == list[5] or
            list[8] == list[6] and list[8] == list[7]
        ):
            return True
    else:
        return False


p1, p2 = req_name()
score = [0, 0]
show_score(score)
turn = 0
data1 = {
        "name": p1,
        "score": score[0],
        "choose": 0
        }
data2 = {
        "name": p2,
        "score": score[1],
        "choose": 0
        }
board_list = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
while True:
    if turn == 0:
        print("Turn to choose for " + p1)
        val = check_val()
        if val == '3':
            break
        else:
            if val == '1':
                val = 'x'
            elif val == '2':
                val = 'o'
            data1["choose"] = val
            if data1["choose"] == 'x':
                choose = 'o'
                data2["choose"] = choose
            elif data1["choose"] == 'o':
                choose = 'x'
                data2["choose"] = choose
    else:
        print("Turn to choose for " + p2)
        com_val = com_check_val()
        val = com_val
        if val == '1':
            val = 'x'
        elif val == '2':
            val = 'o'
        data2["choose"] = val
        if data2["choose"] == 'x':
            choose = 'o'
            data1["choose"] = choose
        elif data2["choose"] == 'o':
            choose = 'x'
            data1["choose"] = choose
    show_board(board_list)
    i = 1
    while True:
        if turn == 0:
            req_position()
        else:
            com_req_position()
        show_board(board_list)
        if check_win(board_list):
            print("Player " + val + " won the game!")
            box_num = None
            if val == data1["choose"]:
                data1["score"] += 1
                score[0] = data1["score"]
                board_list = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
            elif val == data2["choose"]:
                data2["score"] += 1
                score[1] = data2["score"]
                board_list = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
                if turn == 0:
                    turn = 1
                else:
                    turn = 0
            break
        else:
            # if noone win the game
            if val == 'x':  # to show x and o alternately
                val = 'o'
            else:
                val = 'x'
            if turn == 0:
                turn = 1
            else:
                turn = 0
            i += 1
            if i == 10:
                print("Draw!!!")
                board_list = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
                box_num = None
                break
            continue
    show_score(score)
