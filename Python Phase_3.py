from flask import Flask, request, render_template_string
import random

app = Flask(__name__)

questions = {
    "Python": [
        ("Which symbol is used for comments?", ["//", "#", "$"], 2),
        ("Which keyword defines a function?", ["func", "def", "function"], 2),
        ("Which data type stores True or False?", ["int", "bool", "str"], 2)
    ],
    "C++": [
        ("Who developed C++?", ["Bjarne Stroustrup", "James Gosling", "Guido"], 1),
        ("Which symbol ends a statement?", [".", ";", ":"], 2)
    ],
    "General Knowledge": [
        ("Capital of France?", ["Berlin", "Paris", "Rome"], 2),
        ("Largest planet?", ["Earth", "Mars", "Jupiter"], 3)
    ]
}

PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Online Quiz Management System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial;
            background: #eef2ff;
            padding: 20px;
        }
        .box {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 15px;
        }
        h1, h2 { color: #4338ca; text-align: center; }
        input, select, button {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            box-sizing: border-box;
        }
        button {
            background: #4338ca;
            color: white;
            border: 0;
            cursor: pointer;
        }
        .option { display: block; margin: 10px 0; }
    </style>
</head>
<body>
<div class="box">
<h1>Online Quiz System</h1>

{% if result is none %}
<form method="POST">
    <input name="student" placeholder="Enter your name" required>
    <select name="category">
        {% for c in categories %}
        <option>{{ c }}</option>
        {% endfor %}
    </select>

    {% if quiz %}
        <input type="hidden" name="quiz_id" value="{{ quiz_id }}">
        {% for q in quiz %}
            <h3>{{ loop.index }}. {{ q[0] }}</h3>
            {% for option in q[1] %}
                <label class="option">
                    <input style="width:auto" type="radio"
                    name="q{{ loop.index0 }}" value="{{ loop.index0 }}" required>
                    {{ option }}
                </label>
            {% endfor %}
        {% endfor %}
        <button name="submit" value="yes">Submit Quiz</button>
    {% else %}
        <button name="start" value="yes">Start Quiz</button>
    {% endif %}
</form>
{% else %}
    <h2>Quiz Result</h2>
    <p>Student: {{ student }}</p>
    <p>Category: {{ category }}</p>
    <h2>Score: {{ result }}/{{ total }}</h2>
    <h2>Percentage: {{ percentage }}%</h2>
    <a href="/">Try Again</a>
{% endif %}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    categories = list(questions.keys())
    quiz = None
    result = None

    if request.method == "POST":
        student = request.form.get("student", "").strip()
        category = request.form.get("category", "")

        if not student:
            return "Please enter your name.", 400

        if category not in questions:
            return "Invalid category.", 400

        if request.form.get("start"):
            quiz = random.sample(questions[category], len(questions[category]))
            return render_template_string(
                PAGE, categories=categories, quiz=quiz,
                quiz_id=category, result=None
            )

        if request.form.get("submit"):
            category = request.form.get("quiz_id", category)
            if category not in questions:
                return "Invalid quiz.", 400

            quiz = questions[category]
            score = 0

            for i, q in enumerate(quiz):
                answer = request.form.get(f"q{i}")
                if answer is not None and answer.isdigit():
                    if int(answer) == q[2] - 1:
                        score += 1

            total = len(quiz)
            percentage = round(score / total * 100)

            return render_template_string(
                PAGE, categories=categories, quiz=None,
                result=score, total=total,
                percentage=percentage,
                student=student, category=category
            )

    return render_template_string(
        PAGE, categories=categories, quiz=quiz, result=result
    )

if __name__ == "__main__":
    app.run()
