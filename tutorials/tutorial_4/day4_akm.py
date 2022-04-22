# 1
L = list(range(11))
square_list = []
cube_list = []
square = lambda i: i * i
cube = lambda j: j * j * j
for sq in L:
    val = square(sq)
    square_list.append(val)
print(square_list)
for cub in L:
    val = cube(cub)
    cube_list.append(val)
print(cube_list)


# 2
def star_function(x):
    i = 1
    while i < 6:
        print(x * i)
        i = i + 1


star_function("?")
