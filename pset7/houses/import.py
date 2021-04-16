from cs50 import SQL
from sys import exit, argv
import csv

db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("Usage: python import.py characters.csv")
    exit(1)

with open(argv[1], "r") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        split = row["name"].split()

        if len(split) == 3:
            first = split[0]
            middle = split[1]
            last = split[2]
        else:
            first = split[0]
            middle = None
            last = split[1]


        house = row["house"]
        birth = row["birth"]

        db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)", first, middle, last, house, birth)