import random
import csv
import os

questions = {
    "Python": [
        ("Which symbol is used for comments?", ["//", "#", "$"], 2),
        ("Which keyword defines a function?", ["func", "def", "function"], 2),
        ("Which data type stores True or False?", ["int", "bool", "str"], 2)
    ],
    "C++": [
        ("Who developed C++?", ["Bjarne Stroustrup", "James Gosling", "Guido"], 1),
        ("Which symbol ends a statement?", [".", ";", ":"], 2),
        ("Which function starts execution?", ["start()", "main()", "run()"], 2)
    ],
    "General Knowledge": [
        ("Capital of France?", ["Berlin", "Paris", "Rome"], 2),
        ("Largest planet?", ["Earth", "Mars", "Jupiter"], 3),
        ("Red Planet?", ["Venus", "Mars", "Saturn"], 2)
    ]
}

name = input("Enter Student Name: ")

print("\nSelect Category:")
categories = list(questions.keys())

for i, category in enumerate(categories, 1):
    print(f"{i}. {category}")

while True:
    try:
        choice = int(input("Enter choice: "))
        if 1 <= choice <= len(categories):
            category = categories[choice - 1]
            break
        print("Invalid choice. Try again.")
    except ValueError:
        print("Enter a number.")

quiz = questions[category].copy()
random.shuffle(quiz)

score = 0

for i, (question, options, correct) in enumerate(quiz, 1):
    print(f"\nQ{i}. {question}")

    for j, option in enumerate(options, 1):
        print(f"{j}. {option}")

    while True:
        try:
            answer = int(input("Your answer: "))
            if 1 <= answer <= len(options):
                break
            print("Choose a valid option.")
        except ValueError:
            print("Please enter a number.")

    if answer == correct:
        score += 1

total = len(quiz)
percentage = score / total * 100

print("\n===== QUIZ RESULT =====")
print("Student:", name)
print("Category:", category)
print("Score:", score, "/", total)
print(f"Percentage: {percentage:.0f}%")

file_exists = os.path.exists("results.csv")

with open("results.csv", "a", newline="") as file:
    writer = csv.writer(file)

    if not file_exists or os.path.getsize("results.csv") == 0:
        writer.writerow(["Student", "Category", "Score", "Total", "Percentage"])

    writer.writerow([name, category, score, total, f"{percentage:.0f}%"])

print("\nResult saved successfully!")
