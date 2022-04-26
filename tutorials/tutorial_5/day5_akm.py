# 1
#desk = "C:/Users/Admin/OneDrive/Desktop/Git_ojt/python_training/tutorials/tutorial_5/"
f = open("meeting.txt", "w")
f.write("Nice to meet you. I'm Tendo Soji. I'm from Japan.")
f.close()


# 2
def count_word(x):
    f = open(x, "r")
    a_string = f.read()
    word_list = a_string.split()
    num_word = len(word_list)
    print(num_word)


count_word("meeting.txt")


# 3
number = input("Enter a number: ")
num = int(number)
if num < 0:
    raise Exception("Sorry, no numbers below zero")
print(num)
