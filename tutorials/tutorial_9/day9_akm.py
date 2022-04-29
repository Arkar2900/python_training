from cmath import sqrt


contin = True
while contin is True:
    print("Select operation.\n 1.Add\n 2.Subtract\n 3.Multiply\n 4.Divide\n 5.power\n 6.modulo\n 7.square-root\n 8.cube\n")
    x = int(input("Enter a choice: "))
    if x > 0 and x < 7:
        fnum = int(input("Enter first number: "))
        snum = int(input("Enter second number: "))
        if x == 1:
            result = fnum + snum
            print(fnum, " + ", snum, " = ", result)
        elif x == 2:
            result = fnum - snum
            print(fnum, " - ", snum, " = ", result)
        elif x == 3:
            result = fnum * snum
            print(fnum, " * ", snum, " = ", result)
        elif x == 4:
            result = fnum / snum
            print(fnum, " / ", snum, " = ", result)
        elif x == 5:
            result = fnum ** snum
            print(fnum, "  to the power ", snum, " = ", result)
        elif x == 6:
            result = fnum % snum
            print(fnum, "  % ", snum, " = ", result)
    elif x > 6 and x < 9:
        num = int(input("Enter a number: "))
        if x == 7:
            result = sqrt(num)
            print("Square root of ", num, " is ", " = ", result)
        elif x == 8:
            result = num * num * num
            print("Cube of ", num, " is ", result)
    else:
        print("Enter the value within a range of 1 to 8!!!")
    y = input("Let's do next calculation? (yes/no): ")
    if y == "yes":
        contin = True
    elif y == "no":
        contin = False
    else:
        print("Please enter one of the valid words (yes/no)!!!")
