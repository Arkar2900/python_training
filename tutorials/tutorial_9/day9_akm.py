import math


def check_choice(a):
    if a.isdigit() and int(a) > 0 and int(a) < 9:
        return True
    elif a.lower() in 'add' or x.lower() in 'subtract' or x.lower() in 'multiply' or x.lower() in 'divide' or x.lower() in 'power' or x.lower() in 'modulo' or x.lower() in 'square-root' or x.lower() in 'cube':
        return True
    else:
        return False


def check_num(b):
    if b.isdigit():
        return True
    elif b.replace('.', '', 1).isdigit() and b.count('.') < 2:
        return True
    else:
        return False


def req_num1():
    to_loop = True
    while to_loop is True:
        fnum = input("Enter the first number: ")
        if check_num(fnum):
            fnum = float(fnum)
            to_loop = False
        else:
            print("Enter only number to calculate!!")
    to_loop = True
    while to_loop is True:
        snum = input("Enter the second number: ")
        if check_num(snum):
            snum = float(snum)
            to_loop = False
        else:
            print("Enter only number to calculate!!")
    return fnum, snum


def req_num2():
    to_loop = True
    while to_loop is True:
        num = input("Enter a number: ")
        if check_num(num):
            num = float(num)
            to_loop = False
        else:
            print("Enter only number to calculate!!")
    return num


while True:
    print("Select operation.\n 1.Add\n 2.Subtract\n 3.Multiply\n 4.Divide\n 5.power\n 6.modulo\n 7.square-root\n 8.cube\n")
    x = input("Enter a choice: ")
    if check_choice(x):
        if x == '1' or x.lower() in 'add':
            fnum, snum = req_num1()
            result = fnum + snum
            print(fnum, " + ", snum, " = ", result)
        elif x == '2' or x.lower() in 'subtract':
            fnum, snum = req_num1()
            result = fnum - snum
            print(fnum, " - ", snum, " = ", result)
        elif x == '3' or x.lower() in 'multiply':
            fnum, snum = req_num1()
            result = fnum * snum
            print(fnum, " * ", snum, " = ", result)
        elif x == '4' or x.lower() in 'divide':
            fnum, snum = req_num1()
            result = fnum / snum
            print(fnum, " / ", snum, " = ", result)
        elif x == '5' or x.lower() in 'power':
            fnum, snum = req_num1()
            result = fnum ** snum
            print(fnum, " ** ", snum, " = ", result)
        elif x == '6' or x.lower() in 'modulo':
            fnum, snum = req_num1()
            result = fnum % snum
            print(fnum, "  % ", snum, " = ", result)
        elif x == '7' or x.lower() in 'square-root':
            num = req_num2()
            result = math.sqrt(num)
            print("Square root of ", num, " is ", " = ", result)
        elif x == '8' or x.lower() in 'cube':
            num = req_num2()
            result = num * num * num
            print("Cube of ", num, " is ", " = ", result)
    else:
        print("Enter the valid key!!!")
    while True:
        y = input("Let's do next calculation? (yes/no): ")
        if y == "no" or y == 'yes':
            break
        else:
            print("Please enter one of the valid words (yes/no)!!!")
    if y == "no":
        break
    else:
        continue
