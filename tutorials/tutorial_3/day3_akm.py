# 1
number1 = 40
number2 = 40
if number1 * number2 < 500:
    print('The result is ', number1 * number2)
else:
    print('The result is ', number1 + number2)


# 2
arr1 = [1, 2, 3, 4, 5]
arr2 = [4, 5, 7, 9, 10]
dupli = False
for x in arr1:
    for y in arr2:
        if x == y:
            dupli = True
            break
    if dupli is True:
        break
if dupli is True:
    print(" Two lists are duplicated")
else:
    print(" Two lists are not duplicated")
