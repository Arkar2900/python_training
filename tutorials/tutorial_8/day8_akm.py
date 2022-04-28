# 1
import re


def find_l(y):
    x = re.findall("l", y)
    if len(x) >= 2:
        print("Found! Match Sentence")
    else:
        print("Oops! Nothing is match")


def find_word(y):
    x = re.search("a", y)
    if x is None:
        print("There is no 'a' in the sting")
    else:
        print(x.group())


def find_4(y):
    x = re.search(r"\b4\w+", y)
    if x is None:
        print("The string does not start with 4")
    else:
        print(x.string)


a = input("Enter a string: ")
find_l(a)
find_word(a)
find_4(a)
