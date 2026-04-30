import streamlit as st

st.set_page_config(page_title="Lucky Quiz Game", page_icon="🎯")

# ---------------- QUESTIONS ---------------- #

easy_questions = [
    {"q": "What is the plural of 'child'?", "options": ["Childs", "Children", "Childes", "Child"], "ans": "Children"},
    {"q": "What is the opposite of 'hot'?", "options": ["Warm", "Cold", "Heat", "Cooler"], "ans": "Cold"},
    {"q": "Water freezes at?", "options": ["0°C", "10°C", "50°C", "100°C"], "ans": "0°C"},
    {"q": "What is the past tense of 'go'?", "options": ["goed", "went", "gone", "going"], "ans": "went"},
    {"q": "Which gas do we breathe in?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "ans": "Oxygen"},
    {"q": "Fill in the blank: She ___ playing.", "options": ["am", "are", "is", "be"], "ans": "is"},
    {"q": "Which planet is known as Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "ans": "Mars"},
    {"q": "What is the plural of 'book'?", "options": ["Bookes", "Books", "Bookies", "Book"], "ans": "Books"},
    {"q": "Opposite of 'day'?", "options": ["Light", "Night", "Morning", "Sun"], "ans": "Night"},
    {"q": "Human body has how many eyes?", "options": ["1", "2", "3", "4"], "ans": "2"},
]

medium_questions = [
    {"q": "Identify the noun: Ali reads a book.", "options": ["reads", "Ali and book", "a", "reads a"], "ans": "Ali and book"},
    {"q": "Change into past tense: He plays cricket.", "options": ["He played cricket.", "He play cricket.", "He playing cricket.", "He plays cricket."], "ans": "He played cricket."},
    {"q": "Which organ pumps blood?", "options": ["Lungs", "Brain", "Heart", "Kidney"], "ans": "Heart"},
    {"q": "Square root of 81?", "options": ["7", "8", "9", "10"], "ans": "9"},
    {"q": "Synonym of 'happy'?", "options": ["Sad", "Angry", "Glad", "Weak"], "ans": "Glad"},
    {"q": "Which gas do plants absorb?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "ans": "Carbon Dioxide"},
    {"q": "Fill in the blank: They ___ going.", "options": ["is", "am", "are", "was"], "ans": "are"},
    {"q": "Earth is a?", "options": ["Star", "Planet", "Moon", "Comet"], "ans": "Planet"},
    {"q": "Correct sentence: He go to school.", "options": ["He goes to school.", "He go school.", "He going school.", "He gone school."], "ans": "He goes to school."},
    {"q": "Boiling point of water?", "options": ["50°C", "100°C", "150°C", "200°C"], "ans": "100°C"},
]

hard_questions = [
    {"q": "Change into passive voice: Ali writes a letter.", "options": ["A letter is written by Ali.", "A letter was written by Ali.", "Ali is written by a letter.", "A letter writes Ali."], "ans": "A letter is written by Ali."},
    {"q": "Speed of light is?", "options": ["3×10^8 m/s", "3×10^6 m/s", "3×10^5 m/s", "3×10^7 m/s"], "ans": "3×10^8 m/s"},
    {"q": "Change into indirect speech: He said, 'I am ill.'", "options": ["He said that he was ill.", "He said that he is ill.", "He said I am ill.", "He says he was ill."], "ans": "He said that he was ill."},
    {"q": "Which vitamin is obtained from sunlight?", "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "ans": "Vitamin D"},
    {"q": "Identify the tense: She has completed her work.", "options": ["Past Simple", "Present Perfect", "Future Simple", "Present Continuous"], "ans": "Present Perfect"},
    {"q": "Which organ controls the human body?", "options": ["Heart", "Brain", "Lungs", "Kidney"], "ans": "Brain"},
    {"q": "Change into interrogative: He is reading.", "options": ["Is he reading?", "He is reading?", "Does he reading?", "Was he read?"], "ans": "Is he reading?"},
    {"q": "Unit of force is?", "options": ["Joule", "Newton", "Watt", "Volt"], "ans": "Newton"},
    {"q": "Correct sentence: Neither Ali nor his friends is present.", "options": ["Neither Ali nor his friends are present.", "Neither Ali nor his friends am present.", "Neither Ali nor his friends was present.", "No correction"], "ans": "Neither Ali nor his friends are present."},
    {"q": "Chemical formula of water?", "options": ["CO2", "H2O", "O2", "NaCl"], "ans": "H2O"},
]

# ---------------- SESSION STATE ---------------- #

if "started" not in st.session_state:
    st.session_state.started = False
if "q_no" not in st.session_state:
    st.session_state.q_no = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = ""
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

# ---------------- HOME SCREEN ---------------- #

st.title("🎯 Lucky Matric Quiz Game")
st.write("English + Science MCQs for Matric Students")

name = st.text_input("Enter your name:")

level = st.selectbox("Select Difficulty Level:", ["Easy", "Medium", "Hard"])

if st.button("Start Quiz"):
    st.session_state.started = True
    st.session_state.q_no = 0
    st.session_state.score = 0
    st.session_state.level = level
    st.session_state.player_name = name if name.strip() != "" else "Student"
    st.rerun()

# ---------------- QUIZ LOGIC ---------------- #

if st.session_state.started:

    if st.session_state.level == "Easy":
        questions = easy_questions
    elif st.session_state.level == "Medium":
        questions = medium_questions
    else:
        questions = hard_questions

    st.info(f"Level: {st.session_state.level}")
    st.write(f"Question {st.session_state.q_no + 1} of {len(questions)}")
    st.write(f"Score: {st.session_state.score}")

    if st.session_state.q_no < len(questions):
        q = questions[st.session_state.q_no]

        st.subheader(f"Q{st.session_state.q_no + 1}: {q['q']}")

        selected = st.radio(
            "Choose an option:",
            q["options"],
            key=f"question_{st.session_state.q_no}"
        )

        if st.button("Next"):
            if selected == q["ans"]:
                st.session_state.score += 1

            st.session_state.q_no += 1
            st.rerun()

    else:
        st.success(
            f"{st.session_state.player_name}, your final score is: "
            f"{st.session_state.score}/{len(questions)} 🎉"
        )

        if st.session_state.score >= 8:
            st.balloons()
            st.write("Excellent performance!")
        elif st.session_state.score >= 5:
            st.write("Good effort! Keep practicing.")
        else:
            st.write("Needs improvement. Try again!")

        if st.button("Restart"):
            st.session_state.started = False
            st.session_state.q_no = 0
            st.session_state.score = 0
            st.session_state.level = ""
            st.session_state.player_name = ""
            st.rerun()
