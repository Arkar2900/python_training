# 1
class Person:
    def __init__(per, fname, lname):
        per.firstname = fname
        per.lastname = lname

    def printname(per):
        print(per.firstname)


emp = Person("Arkar", "Myo")
emp.printname()


class Employee(Person):
    def __init__(per, fname, lname):
        super().__init__(fname, lname)


emp2 = Employee("Leo", "John")
emp2.printname()


# 2
l = list(range(1, 11))
myiter = iter(l)
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
