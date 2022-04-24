# 1
L = list(range(11))
square_list = []
cube_list = []
square = lambda i: i * i
cube = lambda j: j * j * j
for val in L:
    sq_val = square(val)
    cub_val = cube(val)
    square_list.append(sq_val)
    cube_list.append(cub_val)
print(square_list)
print(cube_list)


# 2
def star_function(x):
    i = 1
    while i < 6:
        print(x * i)
        i = i + 1


star_function("*")
star_function("?")
