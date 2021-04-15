from cs50 import get_float

dollars = -1
while dollars < 0:
    dollars = get_float("Change owed: $")

cents = 0
cents = round(dollars * 100)

c1 = cents//25
cents = cents%25

c2 = cents//10
cents = cents%10

c3 = cents//5
cents = cents%5

c4 = cents//1

coins = c1 + c2 + c3 + c4
print("", +coins)
