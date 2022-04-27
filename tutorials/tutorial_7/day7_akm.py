# 1
import datetime
from datetime import *
given_date = datetime.now()
given_date = datetime(2022, 4, 27, 10, 0, 0)
given_date = given_date + timedelta(days = 2) + timedelta(hours = 2)
print(given_date)


# 2
date1 = datetime(2022, 4, 27)
date2 = datetime(2047, 3, 21)
date_diff = date2 - date1
print(date_diff)

# 3
given_date = datetime.now()
given_date = given_date + timedelta(3 * 30)
print(given_date)

# 4


def result(number):
    divisors = [1]
    for i in range(2, number):
        if (number % i) == 0:
            divisors.append(i)
    return sum(divisors)


print(result(34))
