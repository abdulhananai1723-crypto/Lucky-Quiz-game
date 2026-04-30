import streamlit as st
import time

st.set_page_config(page_title="Lucky Quiz Game", page_icon="🎯")

# ---------------- QUESTIONS ---------------- #

easy_questions = [
    {"q": "What is the plural of 'child'?", "options": ["Childs", "Children", "Childes", "Child"], "ans": "Children"},
    {"q": "Water freezes at?", "options": ["0°C", "10°C", "50°C", "100°C"], "ans": "0°C"},
    {"q": "Which gas do we breathe in?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "ans": "Oxygen"},
    {"q": "Which planet is known as Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "ans": "Mars"},
    {"q": "Opposite of 'day'?", "options": ["Light", "Night", "Morning", "Sun"], "ans": "Night"},
    {"q": "Human body has how many eyes?", "options": ["1", "2", "3", "4"], "ans": "2"},
    {"q": "Fill in the blank: She ___ playing.", "options": ["am", "are", "is", "be"], "ans": "is"},
    {"q": "Past tense of go?", "options": ["goed", "went", "gone", "going"], "ans": "went"},
    {"q": "Plural of book?", "options": ["Bookes", "Books", "Bookies", "Book"], "ans": "Books"},
    {"q": "Opposite of hot?", "options": ["Warm", "Cold", "Heat", "Cooler"], "ans": "Cold"},
]

medium_questions = [
    {"q": "Which organ pumps blood?", "options": ["Lungs", "Brain", "Heart", "Kidney"], "ans": "Heart"},
    {"q": "Square root of 81?", "options": ["7", "8", "9", "10"], "ans": "9"},
    {"q": "Synonym of 'happy'?", "options": ["Sad", "Angry", "Glad", "Weak"], "ans": "Glad"},
    {"q": "Which gas do plants absorb?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "ans": "Carbon Dioxide"},
    {"q": "Earth is a?", "options": ["Star", "Planet", "Moon", "Comet"], "ans": "Planet"},
    {"q": "Boiling point of water?", "options": ["50°C", "100°C", "150°C", "200°C"], "ans": "100°C"},
    {"q": "Correct sentence: He go to school.", "options": ["He goes to school.", "He go school.", "He going school.", "He gone school."], "ans": "He goes to school."},
    {"q": "Fill in the blank: They ___ going.", "options": ["is", "am", "are", "was"], "ans": "are"},
    {"q": "Identify noun: Ali reads a book.", "options": ["reads", "Ali and book", "a", "reads a"], "ans": "Ali and book"},
    {"q": "Past tense: He plays cricket.", "options": ["He played cricket.", "He play cricket.", "He playing cricket.", "He plays cricket."], "ans": "He played cricket."},
]

hard_questions = [
    {"q": "Speed of light is?", "options": ["3×10^8 m/s", "3×10^6", "3×10^5", "3×10^7"], "ans": "3×10^8 m/s"},
    {"q": "Vitamin from sunlight?", "options": ["A", "B", "C", "D"], "ans": "D"},
    {"q": "Unit of force?", "options": ["Joule", "Newton", "Watt", "Volt"], "ans": "Newton"},
    {"q": "Chemical formula of water?", "options": ["CO2", "H2O", "O2", "NaCl"], "ans": "H2O"},
    {"q": "Which organ controls body?", "options": ["Heart", "Brain", "Lungs", "Kidney"], "ans": "Brain"},
    {"q": "Passive: Ali writes a letter.", "options": ["A letter is written by Ali.", "A letter was written by Ali.", "Ali is written by a letter.", "A letter writes Ali."], "ans": "A letter is written by Ali."},
    {"q": "Indirect: He said, I am ill.", "options": ["He said that he was ill.", "He said that he is ill.", "He said I am ill.", "He says he was ill."], "ans": "He said that he was ill."},
    {"q": "Tense: She has completed work.", "options": ["Past", "Present Perfect", "Future", "Continuous"], "ans": "Present Perfect"},
    {"q": "Correct sentence?", "options": ["Neither Ali nor his friends are present.", "Neither Ali nor his friends is present.", "Neither Ali nor his friends am present.", "No correction"], "ans": "Neither Ali nor his friends are present."},
    {"q": "Interrogative: He is reading.", "options": ["Is he reading?", "He is reading?", "Does he reading?", "Was he read?"], "ans": "Is he reading?"},
]

# ---------------- SESSION ---------------- #

if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.q_no = 0
    st.session_state.score = 0
    st.session_state.level = ""
    st.session_state.feedback = ""

# ---------------- UI ---------------- #

st.title("🎯 Lucky Quiz Game")

name = st.text_input("Enter your name:")
level = st.selectbox("Select Level", ["Easy", "Medium", "Hard"])

if st.button("Start Quiz"):
    st.session_state.started = True
    st.session_state.q_no = 0
    st.session_state.score = 0
    st.session_state.level = level
    st.session_state.feedback = ""

# ---------------- GAME ---------------- #

if st.session_state.started:

    if st.session_state.level == "Easy":
        questions = easy_questions
    elif st.session_state.level == "Medium":
        questions = medium_questions
    else:
        questions = hard_questions

    # Show feedback
    if st.session_state.feedback:
        st.success(st.session_state.feedback)

    if st.session_state.q_no < len(questions):

        q = questions[st.session_state.q_no]

        st.subheader(f"Q{st.session_state.q_no + 1}: {q['q']}")

        selected = st.radio("Choose:", q["options"], key=st.session_state.q_no)

        if st.button("Submit"):

            if selected == q["ans"]:
                st.session_state.score += 1
                st.session_state.feedback = "🎉 Congratulations! Correct Answer!"
            else:
                st.session_state.feedback = f"❌ Wrong! Correct answer is: {q['ans']}"

            st.session_state.q_no += 1
            time.sleep(1)
            st.rerun()

    else:
        st.success(f"{name}, Your Score: {st.session_state.score}/{len(questions)} 🎉")

        if st.button("Restart"):
            st.session_state.started = False
            st.session_state.q_no = 0
            st.session_state.score = 0
            st.session_state.feedback = ""
            st.rerun()
