from sys import argv, exit
import re
import csv
import itertools

if len(argv) != 3:
    print("Usage: python dnar.py data.csv sequence.txt")
    exit(1)

if not ".csv" in argv[1]:
    exit(1)

if not ".txt" in argv[2]:
    exit(1)

with open(argv[1], "r") as csvfile:
    csvr = list(csv.reader(csvfile))
    csvr[0].remove("name")
    r = csvr[0]

with open(argv[2], "r") as txtfile:
    dnar = txtfile.read()

strs = []

for i in range(len(r)):
    match = 0
    maxmatch = 0
    pos = 0
    prevpos = 0

    while pos < len(dnar):
        pos = dnar.find(r[i], pos)
        if pos == -1:
            match = 0
            break

        elif (pos != -1) and prevpos == 0:
            match += 1
            maxmatch = match
            prevpos = pos

        elif (pos != -1) and ((pos - len(r[i])) == prevpos):
            match += 1
            maxmatch = match
            prevpos = pos

        elif (pos != -1) and ((pos - len(r[i])) != prevpos):
            match = 1
            prevpos = pos

            if maxmatch < match:
                maxmatch = match
        pos += 1

    strs.append(maxmatch)

strs = list(map(str, strs))

wonamecsv = list(csvr)
wonamecsv.pop(0)

for who in wonamecsv:
    if who[1:] == strs:
        print(f"{who[0]}")
        break
    elif who == wonamecsv[-1]:
        print("No match")