import streamlit as st
import random
import time
import pandas as pd
import os
import json

st.set_page_config(page_title="Lucky Quiz Game", page_icon="🎯")

QUESTIONS_FILE = "questions.json"
LEADERBOARD_FILE = "leaderboard.csv"

default_questions = {
    "English": [
        {"q": "Plural of child?", "options": ["Childs", "Children", "Childes", "Child"], "ans": "Children"},
        {"q": "Past tense of go?", "options": ["goed", "went", "gone", "going"], "ans": "went"},
        {"q": "Opposite of hot?", "options": ["Warm", "Cold", "Heat", "Cooler"], "ans": "Cold"},
    ],
    "Science": [
        {"q": "Water freezes at?", "options": ["0°C", "10°C", "50°C", "100°C"], "ans": "0°C"},
        {"q": "Which gas do we breathe in?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "ans": "Oxygen"},
        {"q": "Chemical formula of water?", "options": ["CO2", "H2O", "O2", "NaCl"], "ans": "H2O"},
    ],
    "Math": [
        {"q": "Square root of 81?", "options": ["7", "8", "9", "10"], "ans": "9"},
        {"q": "10 + 5 = ?", "options": ["12", "15", "18", "20"], "ans": "15"},
        {"q": "5 × 6 = ?", "options": ["20", "25", "30", "35"], "ans": "30"},
    ]
}

def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "w") as f:
            json.dump(default_questions, f, indent=4)
    with open(QUESTIONS_FILE, "r") as f:
        return json.load(f)

def save_questions(data):
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(data, f, indent=4)

if not os.path.exists(LEADERBOARD_FILE):
    pd.DataFrame(columns=["Name", "Subject", "Score"]).to_csv(LEADERBOARD_FILE, index=False)

questions_data = load_questions()

if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.q_no = 0
    st.session_state.score = 0
    st.session_state.feedback = ""
    st.session_state.questions = []
    st.session_state.start_time = time.time()

st.title("🎯 Lucky Quiz Game")

name = st.text_input("Enter Your Name")
subject = st.selectbox("Select Subject", list(questions_data.keys()))

if st.button("Start Quiz"):
    if name.strip() == "":
        st.warning("Please enter your name first")
    else:
        st.session_state.started = True
        st.session_state.q_no = 0
        st.session_state.score = 0
        st.session_state.feedback = ""
        st.session_state.subject = subject
        st.session_state.questions = random.sample(
            questions_data[subject],
            len(questions_data[subject])
        )
        st.session_state.start_time = time.time()
        st.rerun()

if st.session_state.started:
    questions = st.session_state.questions

    total_time = 60
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = total_time - elapsed

    st.warning(f"⏳ Time Left: {remaining} seconds")

    if remaining <= 0:
        st.error("⏰ Time Over!")
        st.session_state.started = False

    elif st.session_state.q_no < len(questions):
        q = questions[st.session_state.q_no]

        st.subheader(f"Q{st.session_state.q_no + 1}: {q['q']}")

        selected = st.radio(
            "Choose Answer:",
            q["options"],
            key=st.session_state.q_no
        )

        if st.button("Submit Answer"):
            if selected == q["ans"]:
                st.session_state.score += 1
                st.session_state.feedback = "✅ Correct!"
            else:
                st.session_state.feedback = f"❌ Wrong! Correct Answer: {q['ans']}"

            st.session_state.q_no += 1
            st.rerun()

        if st.session_state.feedback:
            st.info(st.session_state.feedback)

    else:
        score = st.session_state.score
        total = len(questions)

        st.success(f"🎉 {name}, Your Score: {score}/{total}")

        df = pd.read_csv(LEADERBOARD_FILE)

        new_row = {
            "Name": name,
            "Subject": st.session_state.subject,
            "Score": score
        }

        df.loc[len(df)] = new_row
        df.to_csv(LEADERBOARD_FILE, index=False)

        st.subheader("🏆 Leaderboard")
        leaderboard = df.sort_values(by="Score", ascending=False)
        st.dataframe(leaderboard)

        result_text = f"""
Quiz Result

Name: {name}
Subject: {st.session_state.subject}
Score: {score}/{total}
"""

        st.download_button(
            label="📄 Download Result",
            data=result_text,
            file_name="quiz_result.txt",
            mime="text/plain"
        )

        if st.button("Restart Quiz"):
            st.session_state.started = False
            st.session_state.q_no = 0
            st.session_state.score = 0
            st.session_state.feedback = ""
            st.rerun()

# ---------------- ADMIN PANEL ---------------- #

st.sidebar.title("🔐 Admin Panel")

password = st.sidebar.text_input("Enter Admin Password", type="password")

if password == "admin123":
    st.sidebar.success("Admin Access Granted")

    admin_option = st.sidebar.selectbox(
        "Admin Menu",
        ["View Leaderboard", "Add Question", "Edit Question", "Delete Question"]
    )

    questions_data = load_questions()

    if admin_option == "View Leaderboard":
        st.sidebar.subheader("📊 Quiz Records")
        df = pd.read_csv(LEADERBOARD_FILE)
        st.sidebar.dataframe(df)

    elif admin_option == "Add Question":
        st.sidebar.subheader("➕ Add New Question")

        add_subject = st.sidebar.selectbox(
            "Select Subject",
            list(questions_data.keys())
        )

        new_q = st.sidebar.text_area("Question")
        opt1 = st.sidebar.text_input("Option 1")
        opt2 = st.sidebar.text_input("Option 2")
        opt3 = st.sidebar.text_input("Option 3")
        opt4 = st.sidebar.text_input("Option 4")

        correct = st.sidebar.selectbox(
            "Correct Answer",
            [opt1, opt2, opt3, opt4]
        )

        if st.sidebar.button("Add Question"):
            if new_q and opt1 and opt2 and opt3 and opt4 and correct:
                questions_data[add_subject].append({
                    "q": new_q,
                    "options": [opt1, opt2, opt3, opt4],
                    "ans": correct
                })

                save_questions(questions_data)
                st.sidebar.success("Question Added Successfully!")
                st.rerun()
            else:
                st.sidebar.error("Please fill all fields")

    elif admin_option == "Edit Question":
        st.sidebar.subheader("✏️ Edit Question")

        edit_subject = st.sidebar.selectbox(
            "Select Subject",
            list(questions_data.keys())
        )

        question_list = [
            q["q"] for q in questions_data[edit_subject]
        ]

        selected_question = st.sidebar.selectbox(
            "Select Question",
            question_list
        )

        index = question_list.index(selected_question)
        old_q = questions_data[edit_subject][index]

        updated_q = st.sidebar.text_area(
            "Update Question",
            value=old_q["q"]
        )

        updated_opt1 = st.sidebar.text_input(
            "Option 1",
            value=old_q["options"][0]
        )

        updated_opt2 = st.sidebar.text_input(
            "Option 2",
            value=old_q["options"][1]
        )

        updated_opt3 = st.sidebar.text_input(
            "Option 3",
            value=old_q["options"][2]
        )

        updated_opt4 = st.sidebar.text_input(
            "Option 4",
            value=old_q["options"][3]
        )

        updated_correct = st.sidebar.selectbox(
            "Correct Answer",
            [updated_opt1, updated_opt2, updated_opt3, updated_opt4]
        )

        if st.sidebar.button("Update Question"):
            questions_data[edit_subject][index] = {
                "q": updated_q,
                "options": [
                    updated_opt1,
                    updated_opt2,
                    updated_opt3,
                    updated_opt4
                ],
                "ans": updated_correct
            }

            save_questions(questions_data)
            st.sidebar.success("Question Updated Successfully!")
            st.rerun()

    elif admin_option == "Delete Question":
        st.sidebar.subheader("🗑️ Delete Question")

        delete_subject = st.sidebar.selectbox(
            "Select Subject",
            list(questions_data.keys())
        )

        question_list = [
            q["q"] for q in questions_data[delete_subject]
        ]

        selected_delete = st.sidebar.selectbox(
            "Select Question",
            question_list
        )

        if st.sidebar.button("Delete Question"):
            index = question_list.index(selected_delete)
            questions_data[delete_subject].pop(index)
            save_questions(questions_data)
            st.sidebar.success("Question Deleted Successfully!")
            st.rerun()

else:
    st.sidebar.info("Enter password to access admin panel")
