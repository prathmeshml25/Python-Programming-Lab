import streamlit as st
import random
import csv
import os

st.set_page_config(
    page_title="Online Quiz Management System",
    page_icon="📝"
)

QUESTIONS = {
    "Python": [
        ("Which symbol is used for comments?", ["//", "#", "$"], 1),
        ("Which keyword defines a function?", ["func", "def", "function"], 1),
        ("Which data type stores True or False?", ["int", "bool", "str"], 1),
        ("Which method adds an item to a list?", ["add()", "append()", "push()"], 1)
    ],
    "C++": [
        ("Who developed C++?", ["Bjarne Stroustrup", "James Gosling", "Guido"], 0),
        ("Which symbol ends a statement?", [".", ";", ":"], 1),
        ("Which function starts execution?", ["start()", "main()", "run()"], 1)
    ],
    "General Knowledge": [
        ("Capital of France?", ["Berlin", "Paris", "Rome"], 1),
        ("Largest planet?", ["Earth", "Mars", "Jupiter"], 2),
        ("Red Planet?", ["Venus", "Mars", "Saturn"], 1)
    ]
}

st.title("📝 Online Quiz Management System")
st.write("Welcome! Select a category and test your knowledge.")

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "student" not in st.session_state:
    st.session_state.student = ""

if "category" not in st.session_state:
    st.session_state.category = ""

if "score" not in st.session_state:
    st.session_state.score = None

if st.session_state.quiz is None and not st.session_state.submitted:
    with st.form("start_form"):
        name = st.text_input("Enter Student Name")
        category = st.selectbox("Select Category", list(QUESTIONS.keys()))
        start = st.form_submit_button("Start Quiz")

    if start:
        if not name.strip():
            st.warning("Please enter your name.")
        else:
            quiz = QUESTIONS[category].copy()
            random.shuffle(quiz)

            st.session_state.student = name.strip()
            st.session_state.category = category
            st.session_state.quiz = quiz
            st.session_state.answers = {}
            st.rerun()

if st.session_state.quiz is not None and not st.session_state.submitted:
    st.subheader(f"Student: {st.session_state.student}")
    st.write(f"Category: {st.session_state.category}")

    with st.form("quiz_form"):
        for i, (question, options, correct) in enumerate(st.session_state.quiz):
            st.markdown(f"**Q{i + 1}. {question}**")

            answer = st.radio(
                f"Choose your answer for Q{i + 1}",
                options,
                index=None,
                key=f"question_{i}"
            )

            st.session_state.answers[i] = answer

        submitted = st.form_submit_button("Submit Quiz")

    if submitted:
        score = 0

        for i, (question, options, correct) in enumerate(st.session_state.quiz):
            if st.session_state.answers.get(i) == options[correct]:
                score += 1

        st.session_state.score = score
        st.session_state.submitted = True

        total = len(st.session_state.quiz)
        percentage = round(score / total * 100)

        filename = "results.csv"
        file_exists = os.path.exists(filename)

        with open(filename, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists or os.path.getsize(filename) == 0:
                writer.writerow(["Student", "Category", "Score", "Total", "Percentage"])

            writer.writerow([
                st.session_state.student,
                st.session_state.category,
                score,
                total,
                f"{percentage}%"
            ])

        st.rerun()

if st.session_state.submitted:
    score = st.session_state.score
    total = len(st.session_state.quiz)
    percentage = round(score / total * 100)

    st.success("Quiz Submitted Successfully!")

    st.subheader("📊 Your Result")
    st.write(f"**Student:** {st.session_state.student}")
    st.write(f"**Category:** {st.session_state.category}")

    st.metric("Score", f"{score}/{total}")
    st.metric("Percentage", f"{percentage}%")

    if st.button("Try Another Quiz"):
        st.session_state.quiz = None
        st.session_state.submitted = False
        st.session_state.answers = {}
        st.session_state.score = None
        st.rerun()

st.divider()
st.caption("Online Quiz Management System | Python Project Phase 3")
