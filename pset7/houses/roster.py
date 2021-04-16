from cs50 import SQL
from sys import exit, argv

db = SQL("sqlite:///students.db")

if len(argv) != 2:
    print("Usage: python roster.py 'Gryffindor/Slytherin/Hufflepuff/Ravenclaw'")
    exit(1)
houses = ["Gryffindor", "Slytherin", "Hufflepuff", "Ravenclaw"]
if not argv[1] in houses:
    print("Usage: python roster.py 'Gryffindor/Slytherin/Hufflepuff/Ravenclaw'")
    exit(1)


for row in db.execute("SELECT * FROM students WHERE house = ? ORDER BY last, first", argv[1]):
    if row["middle"] == None:
        print(f"{row['first']} {row['last']}, born {row['birth']}")
    else:
        print(f"{row['first']} {row['middle']} {row['last']}, born {row['birth']}")
