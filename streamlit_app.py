import streamlit as st
import random
import time
import pandas as pd
from fpdf import FPDF
import os

st.set_page_config(page_title="Lucky Quiz Game", page_icon="🎯")

# ---------------- QUESTIONS ---------------- #

questions_data = {
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

# ---------------- FILES ---------------- #

LEADERBOARD_FILE = "leaderboard.csv"

if not os.path.exists(LEADERBOARD_FILE):
    df = pd.DataFrame(columns=["Name", "Subject", "Score"])
    df.to_csv(LEADERBOARD_FILE, index=False)

# ---------------- SESSION ---------------- #

if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.q_no = 0
    st.session_state.score = 0
    st.session_state.feedback = ""
    st.session_state.questions = []
    st.session_state.start_time = time.time()

# ---------------- TITLE ---------------- #

st.title("🎯 Lucky Quiz Game")

# ---------------- USER INFO ---------------- #

name = st.text_input("Enter Your Name")

subject = st.selectbox(
    "Select Subject",
    list(questions_data.keys())
)

# ---------------- START BUTTON ---------------- #

if st.button("Start Quiz"):

    st.session_state.started = True
    st.session_state.q_no = 0
    st.session_state.score = 0
    st.session_state.feedback = ""

    # Random Questions
    st.session_state.questions = random.sample(
        questions_data[subject],
        len(questions_data[subject])
    )

    st.session_state.subject = subject
    st.session_state.start_time = time.time()

# ---------------- QUIZ ---------------- #

if st.session_state.started:

    questions = st.session_state.questions

    # TIMER
    total_time = 60
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = total_time - elapsed

    st.warning(f"⏳ Time Left: {remaining} seconds")

    if remaining <= 0:
        st.error("⏰ Time Over!")
        st.session_state.started = False

    elif st.session_state.q_no < len(questions):

        q = questions[st.session_state.q_no]

        st.subheader(
            f"Q{st.session_state.q_no + 1}: {q['q']}"
        )

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
                st.session_state.feedback = (
                    f"❌ Wrong! Correct Answer: {q['ans']}"
                )

            st.session_state.q_no += 1
            st.rerun()

        if st.session_state.feedback:
            st.success(st.session_state.feedback)

    else:

        score = st.session_state.score
        total = len(questions)

        st.success(
            f"🎉 {name}, Your Score: {score}/{total}"
        )

        # ---------------- SAVE LEADERBOARD ---------------- #

        df = pd.read_csv(LEADERBOARD_FILE)

        new_row = {
            "Name": name,
            "Subject": st.session_state.subject,
            "Score": score
        }

        df.loc[len(df)] = new_row
        df.to_csv(LEADERBOARD_FILE, index=False)

        # ---------------- SHOW LEADERBOARD ---------------- #

        st.subheader("🏆 Leaderboard")

        leaderboard = df.sort_values(
            by="Score",
            ascending=False
        )

        st.dataframe(leaderboard)

        # ---------------- PDF RESULT ---------------- #

        if st.button("Download PDF Result"):

            pdf = FPDF()
            pdf.add_page()

            pdf.set_font("Arial", size=16)

            pdf.cell(200, 10, txt="Quiz Result", ln=True)

            pdf.set_font("Arial", size=12)

            pdf.cell(
                200,
                10,
                txt=f"Name: {name}",
                ln=True
            )

            pdf.cell(
                200,
                10,
                txt=f"Subject: {st.session_state.subject}",
                ln=True
            )

            pdf.cell(
                200,
                10,
                txt=f"Score: {score}/{total}",
                ln=True
            )

            pdf.output("result.pdf")

            with open("result.pdf", "rb") as file:
                st.download_button(
                    label="📄 Download Result PDF",
                    data=file,
                    file_name="Quiz_Result.pdf",
                    mime="application/pdf"
                )

        # ---------------- RESTART ---------------- #

        if st.button("Restart Quiz"):

            st.session_state.started = False
            st.session_state.q_no = 0
            st.session_state.score = 0
            st.session_state.feedback = ""

            st.rerun()

# ---------------- ADMIN PANEL ---------------- #

st.sidebar.title("🔐 Admin Panel")

password = st.sidebar.text_input(
    "Enter Admin Password",
    type="password"
)

if password == "admin123":

    st.sidebar.success("Admin Access Granted")

    st.sidebar.subheader("📊 Quiz Records")

    df = pd.read_csv(LEADERBOARD_FILE)

    st.sidebar.dataframe(df)

else:
    st.sidebar.info("Enter password to access admin panel")
