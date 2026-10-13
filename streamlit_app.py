
import io
import os
import random
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

st.set_page_config(
    page_title="Lucky Quiz Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE = Path(__file__).resolve().parent
DB = Path(os.getenv("QUIZ_DB_PATH", str(BASE / "quiz.db")))
DB.parent.mkdir(parents=True, exist_ok=True)

SEED = {
    "English": [
        ("Plural of child?", ["Childs", "Children", "Childes", "Child"], 1),
        ("Past tense of go?", ["Goed", "Went", "Gone", "Going"], 1),
        ("Opposite of hot?", ["Warm", "Cold", "Heat", "Cooler"], 1),
        ("Choose the correct spelling.",
         ["Definately", "Definitely", "Definetly", "Definatly"], 1),
    ],
    "Science": [
        ("At what temperature does pure water freeze at standard pressure?",
         ["0°C", "10°C", "50°C", "100°C"], 0),
        ("Which gas is essential for human respiration?",
         ["Oxygen", "Carbon dioxide", "Helium", "Hydrogen"], 0),
        ("Chemical formula of water?",
         ["CO2", "H2O", "O2", "NaCl"], 1),
        ("Which planet is known as the Red Planet?",
         ["Venus", "Mars", "Jupiter", "Saturn"], 1),
    ],
    "Math": [
        ("Square root of 81?", ["7", "8", "9", "10"], 2),
        ("10 + 5 = ?", ["12", "15", "18", "20"], 1),
        ("5 × 6 = ?", ["20", "25", "30", "35"], 2),
        ("12 ÷ 3 = ?", ["3", "4", "5", "6"], 1),
    ]
}


# DATABASE

def conn():
    c = sqlite3.connect(DB, timeout=15)
    c.row_factory = sqlite3.Row
    c.execute("PRAGMA busy_timeout=15000")
    return c


def init():
    with conn() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                difficulty TEXT NOT NULL DEFAULT 'Easy',
                question TEXT NOT NULL,
                a TEXT NOT NULL,
                b TEXT NOT NULL,
                c TEXT NOT NULL,
                d TEXT NOT NULL,
                correct INTEGER NOT NULL CHECK(correct BETWEEN 0 AND 3)
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player TEXT NOT NULL,
                subject TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                finished_at TEXT NOT NULL
            )
        """)

        count = c.execute(
            "SELECT COUNT(*) FROM questions"
        ).fetchone()[0]

        if count == 0:
            for subject, entries in SEED.items():
                for question, opts, correct in entries:
                    c.execute("""
                        INSERT INTO questions
                        (subject,difficulty,question,a,b,c,d,correct)
                        VALUES (?,?,?,?,?,?,?,?)
                    """, (subject, "Easy", question, *opts, correct))


init()


def fetch(sql, args=()):
    with conn() as c:
        return [
            dict(r)
            for r in c.execute(sql, args).fetchall()
        ]


def execute(sql, args=()):
    with conn() as c:
        c.execute(sql, args)


# PDF CERTIFICATE

def certificate(player, subject, score, total, date):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    w, h = A4

    pdf.setFillColor(colors.HexColor("#0f172a"))
    pdf.rect(0, 0, w, h, fill=1, stroke=0)

    pdf.setStrokeColor(colors.HexColor("#38bdf8"))
    pdf.setLineWidth(4)
    pdf.rect(35, 35, w-70, h-70, fill=0, stroke=1)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 28)
    pdf.drawCentredString(
        w/2, h-185, "CERTIFICATE OF COMPLETION"
    )

    pdf.setFont("Helvetica", 15)
    pdf.drawCentredString(
        w/2, h-245, "This certificate is presented to"
    )

    pdf.setFillColor(colors.HexColor("#7dd3fc"))
    pdf.setFont("Helvetica-Bold", 26)

    safe_name = player.encode(
        "latin-1", "replace"
    ).decode("latin-1")[:38]

    pdf.drawCentredString(w/2, h-305, safe_name)

    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica", 16)

    pdf.drawCentredString(
        w/2, h-360,
        f"For completing the {subject[:40]} assessment"
    )

    percentage = round(score / total * 100) if total else 0

    pdf.drawCentredString(
        w/2, h-400,
        f"Score: {score}/{total}  |  {percentage}%"
    )

    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(w/2, h-470, date)

    pdf.drawCentredString(
        w/2, 100,
        "LUCKY QUIZ PRO - Automated completion certificate"
    )

    pdf.save()
    return buffer.getvalue()


# PREMIUM UI

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg,
        #080f20 0%,
        #101c34 60%,
        #0b1223 100%
    );
    color: #e2e8f0;
}

[data-testid="stSidebar"] {
    background: #101a30;
}

h1, h2, h3 {
    color: #f8fafc !important;
}

.hero {
    padding: 32px;
    border: 1px solid #334155;
    border-radius: 22px;
    background: linear-gradient(110deg,#172b51,#102038);
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 2.5rem;
    margin: 0;
    color: #fff;
}

.hero p {
    color: #a5c5e8;
    font-size: 1.05rem;
    margin: 8px 0 0;
}

.metric {
    padding: 18px;
    border-radius: 16px;
    border: 1px solid #34445e;
    background: #17243b;
}

.metric strong {
    font-size: 1.8rem;
    color: #7dd3fc;
}

div.stButton > button[kind="primary"] {
    background: #0284c7;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🎯 Lucky Quiz Pro</h1>
    <p>
        Premium Quiz & Assessment Platform
        · Learn · Compete · Achieve
    </p>
</div>
""", unsafe_allow_html=True)


# SESSION STATE

if "quiz" not in st.session_state:
    st.session_state.quiz = None

if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False


# NAVIGATION

with st.sidebar:
    st.title("⚡ Navigation")

    page = st.radio(
        "Workspace",
        [
            "🏠 Dashboard",
            "🎮 Take Quiz",
            "🏆 Leaderboard",
            "🔐 Admin Studio"
        ],
        label_visibility="collapsed"
    )

    st.divider()
    st.caption("Lucky Quiz Pro • Version 1.0")


# DASHBOARD

if page == "🏠 Dashboard":

    stats = fetch("""
        SELECT
        (SELECT COUNT(*) FROM questions) AS questions,
        (SELECT COUNT(DISTINCT subject) FROM questions) AS subjects,
        (SELECT COUNT(*) FROM attempts) AS attempts
    """)[0]

    cols = st.columns(3)

    labels = [
        "Question Bank",
        "Subjects",
        "Completed Quizzes"
    ]

    values = [
        stats["questions"],
        stats["subjects"],
        stats["attempts"]
    ]

    for col, label, value in zip(cols, labels, values):
        col.markdown(
            f'<div class="metric">{label}<br>'
            f'<strong>{value}</strong></div>',
            unsafe_allow_html=True
        )

    st.write("")
    st.subheader("Welcome to your learning arena")

    st.write(
        "Choose **Take Quiz** to begin an assessment. "
        "Every completed attempt receives a result report "
        "and downloadable certificate."
    )

    st.info(
        "Admin can manage the question bank, export data, "
        "and review quiz activity from Admin Studio."
    )


# QUIZ ENGINE

elif page == "🎮 Take Quiz":

    quiz = st.session_state.quiz

    if quiz is None:

        st.subheader("🚀 Set up your assessment")

        subjects = [
            r["subject"]
            for r in fetch(
                "SELECT DISTINCT subject FROM questions ORDER BY subject"
            )
        ]

        if not subjects:
            st.warning("No questions available.")
            st.stop()

        with st.form("setup"):

            player = st.text_input(
                "Your name",
                max_chars=50
            )

            subject = st.selectbox(
                "Subject",
                subjects
            )

            difficulty = st.selectbox(
                "Difficulty",
                ["All", "Easy", "Medium", "Hard"]
            )

            count = st.slider(
                "Number of questions",
                1, 30, 5
            )

            minutes = st.select_slider(
                "Time limit (minutes)",
                options=[1, 2, 3, 5, 10, 15],
                value=5
            )

            start = st.form_submit_button(
                "Start assessment →",
                type="primary",
                use_container_width=True
            )

        if start:

            sql = "SELECT * FROM questions WHERE subject=?"
            args = (subject,)

            if difficulty != "All":
                sql += " AND difficulty=?"
                args = (subject, difficulty)

            pool = fetch(sql, args)

            if not player.strip():
                st.error("Please enter your name.")

            elif not pool:
                st.error("No questions match these filters.")

            else:

                chosen = random.sample(
                    pool,
                    min(count, len(pool))
                )

                for q in chosen:
                    opts = [q[k] for k in "abcd"]
                    q["correct_text"] = opts[q["correct"]]
                    random.shuffle(opts)
                    q["display_options"] = opts

                st.session_state.quiz = {
                    "player": player.strip(),
                    "subject": subject,
                    "questions": chosen,
                    "answers": {},
                    "index": 0,
                    "deadline": time.time() + minutes * 60,
                    "started_at": time.time(),
                    "saved": False,
                    "finished": False
                }

                st.rerun()

    else:

        qs = quiz["questions"]

        remaining = max(
            0,
            int(quiz["deadline"] - time.time())
        )

        if remaining == 0:
            quiz["finished"] = True

        if not quiz["finished"] and quiz["index"] < len(qs):

            i = quiz["index"]
            q = qs[i]

            st.progress(
                i / len(qs),
                text=f"Question {i+1} of {len(qs)}"
            )

            st.warning(
                f"⏳ Time remaining: "
                f"{remaining//60:02d}:{remaining%60:02d}"
            )

            st.subheader(q["question"])

            with st.form(f"answer_{i}"):

                choice = st.radio(
                    "Choose one answer",
                    q["display_options"],
                    index=None
                )

                submitted = st.form_submit_button(
                    "Submit & continue",
                    type="primary"
                )

            if submitted:

                if time.time() >= quiz["deadline"]:
                    quiz["finished"] = True
                    st.rerun()

                elif choice is None:
                    st.warning("Select an answer first.")

                else:
                    quiz["answers"][i] = choice
                    quiz["index"] += 1

                    if quiz["index"] >= len(qs):
                        quiz["finished"] = True

                    st.rerun()

            if st.button("Finish early"):
                quiz["finished"] = True
                st.rerun()

        else:

            quiz["finished"] = True

            score = sum(
                quiz["answers"].get(i) == q["correct_text"]
                for i, q in enumerate(qs)
            )

            total = len(qs)
            pct = 100 * score / total if total else 0

            duration = int(
                time.time() - quiz["started_at"]
            )

            if not quiz["saved"]:

                execute("""
                    INSERT INTO attempts
                    (player,subject,score,total,duration,finished_at)
                    VALUES (?,?,?,?,?,?)
                """, (
                    quiz["player"],
                    quiz["subject"],
                    score,
                    total,
                    duration,
                    datetime.now(timezone.utc).strftime(
                        "%Y-%m-%d %H:%M UTC"
                    )
                ))

                quiz["saved"] = True

            if pct == 100:
                st.balloons()

            st.subheader("📊 Assessment complete")

            a, b, c = st.columns(3)

            a.metric("Score", f"{score}/{total}")
            b.metric("Accuracy", f"{pct:.0f}%")
            c.metric("Time used", f"{duration}s")

            if pct >= 80:
                st.success("Excellent work!")
            else:
                st.info("Good effort — review your answers below.")

            with st.expander(
                "🔎 Review answers",
                expanded=True
            ):

                for i, q in enumerate(qs):

                    given = quiz["answers"].get(
                        i,
                        "Not answered"
                    )

                    correct = given == q["correct_text"]

                    st.markdown(
                        f"**{i+1}. {q['question']}**"
                    )

                    st.write(
                        f"Your answer: {given} "
                        f"{'✅' if correct else '❌'}"
                    )

                    if not correct:
                        st.caption(
                            "Correct answer: " + q["correct_text"]
                        )

            date = datetime.now(timezone.utc).strftime(
                "%d %B %Y"
            )

            st.download_button(
                "📄 Download PDF certificate",
                certificate(
                    quiz["player"],
                    quiz["subject"],
                    score,
                    total,
                    date
                ),
                file_name="Lucky_Quiz_Certificate.pdf",
                mime="application/pdf"
            )

            if st.button(
                "🔁 Start a new quiz",
                type="primary"
            ):
                st.session_state.quiz = None
                st.rerun()


# LEADERBOARD

elif page == "🏆 Leaderboard":

    st.subheader("🏆 Top performers")

    df = pd.DataFrame(fetch("""
        SELECT
            player,
            subject,
            score,
            total,
            ROUND(100.0*score/total,1) AS accuracy,
            duration,
            finished_at
        FROM attempts
        ORDER BY accuracy DESC, duration ASC, finished_at DESC
    """))

    if df.empty:
        st.info("No completed attempts yet.")

    else:

        subjects = ["All"] + sorted(
            df.subject.unique().tolist()
        )

        chosen = st.selectbox(
            "Filter by subject",
            subjects
        )

        if chosen != "All":
            df = df[df.subject == chosen]

        st.dataframe(
            df.head(100),
            hide_index=True,
            use_container_width=True
        )


# ADMIN STUDIO

elif page == "🔐 Admin Studio":

    st.subheader("🔐 Administrator Studio")

    try:
        admin_password = st.secrets.get(
            "ADMIN_PASSWORD",
            os.getenv("ADMIN_PASSWORD", "")
        )
    except Exception:
        admin_password = os.getenv(
            "ADMIN_PASSWORD", ""
        )

    if not admin_password:
        st.error(
            "Admin password is not configured. "
            "Set ADMIN_PASSWORD in Streamlit Secrets."
        )
        st.stop()

    if not st.session_state.admin_ok:

        with st.form("login"):

            pwd = st.text_input(
                "Administrator password",
                type="password"
            )

            if st.form_submit_button(
                "Sign in",
                type="primary"
            ):

                import hmac

                if hmac.compare_digest(
                    pwd,
                    admin_password
                ):
                    st.session_state.admin_ok = True
                    st.rerun()

                else:
                    st.error("Incorrect password.")

        st.stop()

    if st.button("Sign out"):
        st.session_state.admin_ok = False
        st.rerun()

    tab1, tab2, tab3 = st.tabs([
        "📝 Question Bank",
        "➕ Add / Edit",
        "📈 Results & Export"
    ])

    # QUESTION BANK

    with tab1:

        rows = fetch(
            "SELECT * FROM questions ORDER BY subject,id"
        )

        st.dataframe(
            pd.DataFrame(rows),
            hide_index=True,
            use_container_width=True
        )

        ids = {
            f"#{r['id']} · {r['subject']} · {r['question'][:65]}": r["id"]
            for r in rows
        }

        if ids:

            selection = st.selectbox(
                "Select question to delete",
                list(ids)
            )

            confirm = st.checkbox(
                "I confirm deletion of this question"
            )

            if st.button(
                "Delete selected question",
                disabled=not confirm
            ):

                execute(
                    "DELETE FROM questions WHERE id=?",
                    (ids[selection],)
                )

                st.success("Question deleted.")
                st.rerun()

        st.download_button(
            "Export questions CSV",
            pd.DataFrame(rows).to_csv(
                index=False
            ).encode("utf-8-sig"),
            "questions.csv",
            "text/csv"
        )

        upload = st.file_uploader(
            "Import questions CSV "
            "(subject,difficulty,question,a,b,c,d,correct)",
            type="csv"
        )

        if upload is not None and st.button("Import CSV"):

            try:

                imported = pd.read_csv(upload).fillna("")

                required = [
                    "subject",
                    "difficulty",
                    "question",
                    "a", "b", "c", "d",
                    "correct"
                ]

                missing = set(required) - set(imported.columns)

                if missing:
                    raise ValueError(
                        "Missing columns: " + ", ".join(missing)
                    )

                clean = []

                for _, r in imported.iterrows():

                    vals = [
                        str(r[k]).strip()
                        for k in required[:-1]
                    ]

                    idx = int(r["correct"])

                    if (
                        not all(vals)
                        or idx not in range(4)
                        or vals[1] not in ("Easy", "Medium", "Hard")
                    ):
                        raise ValueError("Invalid question row")

                    clean.append((*vals, idx))

                with conn() as c:
                    c.executemany("""
                        INSERT INTO questions
                        (subject,difficulty,question,a,b,c,d,correct)
                        VALUES (?,?,?,?,?,?,?,?)
                    """, clean)

                st.success(
                    f"Imported {len(clean)} questions."
                )

                st.rerun()

            except Exception as e:
                st.error(f"Import failed: {e}")

    # ADD AND EDIT

    with tab2:

        existing = fetch(
            "SELECT * FROM questions ORDER BY id"
        )

        choices = ["Create new question"] + [
            f"Edit #{r['id']}: {r['question'][:55]}"
            for r in existing
        ]

        choice = st.selectbox(
            "Action",
            choices
        )

        old = None

        if choice != "Create new question":

            selected_id = int(
                choice.split("#")[1].split(":")[0]
            )

            old = next(
                r for r in existing
                if r["id"] == selected_id
            )

        with st.form("question_form"):

            subject = st.text_input(
                "Subject",
                value=old["subject"] if old else "General"
            )

            levels = ["Easy", "Medium", "Hard"]

            difficulty = st.selectbox(
                "Difficulty",
                levels,
                index=levels.index(old["difficulty"]) if old else 0
            )

            question = st.text_area(
                "Question",
                value=old["question"] if old else ""
            )

            options = []

            for letter in "ABCD":

                value = (
                    old[letter.lower()]
                    if old else ""
                )

                option = st.text_input(
                    f"Option {letter}",
                    value=value,
                    key=f"option_{letter}"
                )

                options.append(option)

            correct = st.selectbox(
                "Correct option",
                ["A", "B", "C", "D"],
                index=old["correct"] if old else 0
            )

            if st.form_submit_button(
                "Save question",
                type="primary"
            ):

                if (
                    not subject.strip()
                    or not question.strip()
                    or not all(x.strip() for x in options)
                ):
                    st.error("Fill all fields.")

                elif len(set(x.strip() for x in options)) != 4:
                    st.error(
                        "All four options must be different."
                    )

                else:

                    args = (
                        subject.strip(),
                        difficulty,
                        question.strip(),
                        *(x.strip() for x in options),
                        "ABCD".index(correct)
                    )

                    if old:

                        execute("""
                            UPDATE questions
                            SET subject=?,difficulty=?,question=?,
                                a=?,b=?,c=?,d=?,correct=?
                            WHERE id=?
                        """, args + (old["id"],))

                    else:

                        execute("""
                            INSERT INTO questions
                            (subject,difficulty,question,a,b,c,d,correct)
                            VALUES (?,?,?,?,?,?,?,?)
                        """, args)

                    st.success("Question saved.")
                    st.rerun()

    # RESULTS AND EXPORT

    with tab3:

        attempts = pd.DataFrame(
            fetch(
                "SELECT * FROM attempts ORDER BY id DESC"
            )
        )

        if attempts.empty:
            st.info("No attempts recorded.")

        else:

            st.metric(
                "Total completed attempts",
                len(attempts)
            )

            st.dataframe(
                attempts,
                hide_index=True,
                use_container_width=True
            )

            st.download_button(
                "Download results CSV",
                attempts.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                "quiz_results.csv",
                "text/csv"
            )
