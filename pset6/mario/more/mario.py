from cs50 import get_int

n = 0
while n < 1 or n > 8:
    n = get_int("Height: ")
for i in range(0, n, 1):

    for s in range(n - 1, i, -1):
        print(" ", end="")

    for l in range(-1, i, 1):
        print("#", end="")

    print("  ", end="")

    for l in range(-1, i, 1):
        print("#", end="")

    print()