from cs50 import get_string

letters = 0
words = 1
sentences = 0
text = get_string("Text: ")
n = len(text)

for i in range(0, n, 1):
    if text[i] >= 'a' and text[i] <= 'z':
        letters += 1

    if text[i] >= 'A' and text[i] <= 'Z':
        letters += 1

    if text[i] == ' ':
        words += 1

    if text[i] == '.':
        sentences += 1

    if text[i] == '!':
        sentences += 1

    if text[i] == '?':
        sentences += 1

avgl = (letters / words) * 100
avgs = (sentences / words) * 100
grade = 0.0588 * avgl - 0.296 * avgs - 15.8

if grade < 1:
    print("Before Grade 1")

elif grade >= 16:
    print("Grade 16+")

else:
    print("Grade ", + round(grade))

