import json
from pathlib import Path

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Campus | Student Management",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_FILE = Path(__file__).resolve().parent / "school_data.json"
EMPTY_DATA = {"students": [], "teachers": []}


st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

      :root {
        --ink: #17243b;
        --muted: #74819a;
        --line: #e8edf4;
        --violet: #635bdb;
        --teal: #29a99a;
      }
      html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
      [data-testid="stAppViewContainer"] { background: #f5f7fb; }
      [data-testid="stHeader"] { background: rgba(245, 247, 251, .88); }
      [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #17243b 0%, #202e49 100%);
      }
      [data-testid="stSidebar"] * { color: #edf1ff; }
      [data-testid="stSidebar"] [data-testid="stRadio"] label {
        border-radius: 10px; padding: 7px 10px; margin: 2px 0;
      }
      [data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background: rgba(255,255,255,.09);
      }
      .block-container { max-width: 1380px; padding-top: 1.7rem; padding-bottom: 3rem; }
      h1, h2, h3 { color: var(--ink); font-family: 'Manrope', sans-serif; }
      h2 { letter-spacing: -.035em; }
      p, label, [data-testid="stCaptionContainer"] { color: var(--muted); }
      .brand { display:flex; align-items:center; gap:12px; margin: 10px 0 28px; }
      .brand-mark {
        width:42px; height:42px; display:grid; place-items:center; border-radius:14px;
        background:linear-gradient(135deg,#8179ff,#4e48c4); font-size:21px;
        box-shadow:0 8px 22px rgba(99,91,219,.34);
      }
      .brand-name { font:800 17px 'Manrope',sans-serif; color:#fff; letter-spacing:-.03em; }
      .brand-sub { color:#aab5cf; font-size:11px; letter-spacing:.12em; text-transform:uppercase; margin-top:1px; }
      .side-note { color:#9eabc5; font-size:12px; line-height:1.6; margin-top:28px; }
      .hero {
        display:flex; align-items:center; justify-content:space-between; gap:20px;
        padding:27px 31px; margin:0 0 25px; border-radius:22px; color:#fff;
        background:radial-gradient(circle at 84% 10%,rgba(143,137,255,.48),transparent 27%),
                   linear-gradient(115deg,#202c49 0%,#393a76 55%,#625bd3 100%);
        box-shadow:0 15px 38px rgba(40,47,91,.13);
      }
      .hero h1 { color:white; font-size:30px; line-height:1.15; margin:5px 0 7px; letter-spacing:-.045em; }
      .hero p { color:#d7dcf3; margin:0; font-size:14px; }
      .hero-kicker { color:#bfc4ff; font-size:11px; font-weight:700; letter-spacing:.15em; text-transform:uppercase; }
      .hero-chip { white-space:nowrap; border:1px solid rgba(255,255,255,.22); background:rgba(255,255,255,.1); border-radius:999px; padding:10px 15px; color:#f5f5ff; font-size:12px; }
      .section-title { margin: 5px 0 2px; font:700 18px 'Manrope',sans-serif; color:var(--ink); }
      .section-copy { color:var(--muted); font-size:13px; margin-bottom:17px; }
      .metric-card {
        background:#fff; border:1px solid var(--line); border-radius:17px; padding:18px 20px;
        min-height:119px; box-shadow:0 5px 18px rgba(27,42,71,.035);
      }
      .metric-label { color:#7d89a0; font-size:12px; font-weight:600; }
      .metric-value { color:var(--ink); font:800 28px 'Manrope',sans-serif; margin:7px 0 2px; letter-spacing:-.04em; }
      .metric-note { color:#9aa4b6; font-size:11px; }
      .surface {
        background:#fff; border:1px solid var(--line); border-radius:17px; padding:20px 22px;
        box-shadow:0 5px 18px rgba(27,42,71,.035); margin-bottom:15px;
      }
      [data-testid="stForm"] {
        background:#fff; border:1px solid var(--line); border-radius:17px; padding:20px 22px;
        box-shadow:0 5px 18px rgba(27,42,71,.035);
      }
      .stButton > button, [data-testid="stFormSubmitButton"] > button {
        border:0; border-radius:10px; background:linear-gradient(100deg,#655dde,#514ac5);
        color:#fff; font-weight:700; padding:.55rem 1.15rem; box-shadow:0 6px 14px rgba(99,91,219,.18);
      }
      .stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
        border:0; color:#fff; background:linear-gradient(100deg,#554ecb,#433daf);
      }
      [data-testid="stTextInput"] input, [data-testid="stNumberInput"] input {
        border-radius:9px;
      }
      [data-testid="stDataFrame"] { border:1px solid var(--line); border-radius:12px; overflow:hidden; }
      div[data-testid="stAlert"] { border-radius:12px; }
      @media (max-width: 700px) {
        .hero { padding:22px; align-items:flex-start; flex-direction:column; }
        .hero h1 { font-size:25px; }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


def load_data():
    if not DATA_FILE.exists():
        return {"students": [], "teachers": []}

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            saved = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(f"{DATA_FILE.name} contains invalid JSON: {error}") from error

    if not isinstance(saved, dict):
        raise ValueError(f"{DATA_FILE.name} must contain a JSON object.")

    data = {"students": saved.get("students", []), "teachers": saved.get("teachers", [])}
    if not isinstance(data["students"], list) or not isinstance(data["teachers"], list):
        raise ValueError("The students and teachers entries in the data file must be lists.")
    return data


def save_data(data):
    temporary_file = DATA_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    temporary_file.replace(DATA_FILE)


def id_matches(saved_id, requested_id):
    """Match numeric IDs from both older string-based files and new integer values."""
    try:
        return int(saved_id) == int(requested_id)
    except (TypeError, ValueError):
        return str(saved_id).strip() == str(requested_id).strip()


def valid_email(email):
    email = email.strip()
    return " " not in email and email.count("@") == 1 and "." in email.rsplit("@", 1)[-1]


def grade_values(student):
    grades = student.get("grades", {})
    if not isinstance(grades, dict):
        return {}
    valid = {}
    for subject, mark in grades.items():
        try:
            valid[str(subject)] = float(mark)
        except (TypeError, ValueError):
            continue
    return valid


def average_grade(student):
    grades = grade_values(student)
    return sum(grades.values()) / len(grades) if grades else None


def display_name(student):
    return f"{student.get('name', 'Unnamed student')} · #{student.get('roll_no', '—')}"


def metric_card(label, value, note, icon):
    st.markdown(
        f"""
        <div class="metric-card">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span class="metric-label">{label}</span><span style="font-size:19px">{icon}</span>
          </div>
          <div class="metric-value">{value}</div>
          <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, description):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-copy">{description}</div>', unsafe_allow_html=True)


def student_table(students):
    rows = []
    for student in students:
        average = average_grade(student)
        rows.append({
            "Student": student.get("name", "—"),
            "Roll number": student.get("roll_no", "—"),
            "Age": student.get("age", "—"),
            "Email": student.get("email", "—"),
            "Subjects": len(grade_values(student)),
            "Average": f"{average:.1f}" if average is not None else "—",
        })
    return pd.DataFrame(rows)


try:
    data = load_data()
except ValueError as error:
    st.error(str(error))
    st.info("Fix the data file and reload the page. The app has not overwritten it.")
    st.stop()

students = [item for item in data["students"] if isinstance(item, dict)]
teachers = [item for item in data["teachers"] if isinstance(item, dict)]

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-mark">🎓</div>
          <div><div class="brand-name">Campus</div><div class="brand-sub">School workspace</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("MANAGEMENT")
    page = st.radio(
        "Choose a section",
        ["Overview", "Students", "Teachers", "Gradebook"],
        label_visibility="collapsed",
    )
    st.markdown(
        f"<div class='side-note'>Your school records are saved locally in <b>{DATA_FILE.name}</b>.<br><br>Students <b>{len(students)}</b> &nbsp; · &nbsp; Teachers <b>{len(teachers)}</b></div>",
        unsafe_allow_html=True,
    )

hero_content = {
    "Overview": ("A clearer view of your school", "Keep student, teacher, and grade records together in one simple workspace.", "SCHOOL OVERVIEW"),
    "Students": ("Student records", "Register learners and find their details and academic summaries.", "STUDENT DIRECTORY"),
    "Teachers": ("Teacher directory", "Add staff records and keep subject assignments close at hand.", "STAFF DIRECTORY"),
    "Gradebook": ("Gradebook", "Record marks by subject and see each student’s current average.", "ACADEMIC RECORDS"),
}
hero_title, hero_description, hero_kicker = hero_content[page]
st.markdown(
    f"""
    <div class="hero">
      <div><div class="hero-kicker">{hero_kicker}</div><h1>{hero_title}</h1><p>{hero_description}</p></div>
      <div class="hero-chip">✦ &nbsp; School management</div>
    </div>
    """,
    unsafe_allow_html=True,
)


if page == "Overview":
    grade_count = sum(len(grade_values(student)) for student in students)
    averages = [average_grade(student) for student in students]
    averages = [value for value in averages if value is not None]
    school_average = sum(averages) / len(averages) if averages else None

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        metric_card("Students", len(students), "Learners in the directory", "👩‍🎓")
    with kpi2:
        metric_card("Teachers", len(teachers), "Staff members registered", "👩‍🏫")
    with kpi3:
        metric_card("Grade entries", grade_count, "Marks recorded by subject", "📚")
    with kpi4:
        metric_card("School average", f"{school_average:.1f}" if school_average is not None else "—", "Across students with grades", "✨")

    st.write("")
    left, right = st.columns([1.45, 1])
    with left:
        page_header("Student snapshot", "A quick look at the latest student records.")
        if students:
            st.dataframe(student_table(list(reversed(students))[:8]), hide_index=True, use_container_width=True)
        else:
            st.info("No students yet. Open Students to register the first learner.")
    with right:
        page_header("Grade activity", "Subjects that currently have marks recorded.")
        subject_totals = {}
        for student in students:
            for subject, mark in grade_values(student).items():
                subject_totals.setdefault(subject, []).append(mark)
        if subject_totals:
            subject_rows = [
                {"Subject": subject, "Entries": len(marks), "Average": f"{sum(marks) / len(marks):.1f}"}
                for subject, marks in sorted(subject_totals.items())
            ]
            st.dataframe(pd.DataFrame(subject_rows), hide_index=True, use_container_width=True)
        else:
            st.markdown('<div class="surface" style="color:#8792a7">Grade summaries will appear here once marks are added.</div>', unsafe_allow_html=True)


elif page == "Students":
    form_col, list_col = st.columns([0.78, 1.22], gap="large")
    with form_col:
        page_header("Add a student", "Enter the learner’s details to create a record.")
        with st.form("student_registration", clear_on_submit=True):
            name = st.text_input("Full name")
            age_col, roll_col = st.columns(2)
            with age_col:
                age = st.number_input("Age", min_value=1, max_value=120, step=1)
            with roll_col:
                roll_no = st.number_input("Roll number", min_value=1, step=1)
            email = st.text_input("Email address")
            submitted = st.form_submit_button("Register student", use_container_width=True)

        if submitted:
            if not name.strip() or not email.strip():
                st.error("Please enter the student’s name and email.")
            elif not valid_email(email):
                st.error("Please enter a valid email address.")
            elif any(id_matches(item.get("roll_no"), roll_no) for item in students):
                st.error(f"Roll number {roll_no} is already in use.")
            else:
                data["students"].append({
                    "name": name.strip(), "age": int(age), "email": email.strip(),
                    "roll_no": int(roll_no), "grades": {},
                })
                save_data(data)
                st.success(f"{name.strip()} has been registered.")
                students = [item for item in data["students"] if isinstance(item, dict)]

    with list_col:
        page_header("Directory", f"{len(students)} student record{'s' if len(students) != 1 else ''}.")
        search = st.text_input("Search students", placeholder="Search by name, email, or roll number", label_visibility="collapsed")
        filtered = [
            student for student in students
            if search.strip().lower() in " ".join(str(student.get(key, "")) for key in ("name", "email", "roll_no")).lower()
        ]
        if filtered:
            st.dataframe(student_table(filtered), hide_index=True, use_container_width=True)
            selected_label = st.selectbox("View student details", [display_name(item) for item in filtered])
            selected = filtered[[display_name(item) for item in filtered].index(selected_label)]
            grades = grade_values(selected)
            detail_col1, detail_col2 = st.columns(2)
            with detail_col1:
                st.markdown(f"**{selected.get('name', '—')}**  \nRoll number: {selected.get('roll_no', '—')}  \nAge: {selected.get('age', '—')}  \nEmail: {selected.get('email', '—')}")
            with detail_col2:
                avg = average_grade(selected)
                st.markdown(f"**Average:** {f'{avg:.1f}' if avg is not None else 'No grades yet'}")
                if grades:
                    st.caption(" · ".join(f"{subject}: {mark:g}" for subject, mark in grades.items()))
                else:
                    st.caption("No subject marks have been added yet.")
        else:
            st.info("No matching students. Try a different search or register a learner.")


elif page == "Teachers":
    form_col, list_col = st.columns([0.78, 1.22], gap="large")
    with form_col:
        page_header("Add a teacher", "Enter the staff member’s details and assigned subject.")
        with st.form("teacher_registration", clear_on_submit=True):
            name = st.text_input("Full name")
            age = st.number_input("Age", min_value=18, max_value=120, step=1)
            email = st.text_input("Email address")
            subject = st.text_input("Subject taught")
            emp_id = st.number_input("Employee ID", min_value=1, step=1)
            submitted = st.form_submit_button("Register teacher", use_container_width=True)

        if submitted:
            if not name.strip() or not email.strip() or not subject.strip():
                st.error("Please complete all fields.")
            elif not valid_email(email):
                st.error("Please enter a valid email address.")
            elif any(id_matches(item.get("emp_id"), emp_id) for item in teachers):
                st.error(f"Employee ID {emp_id} is already in use.")
            else:
                data["teachers"].append({
                    "name": name.strip(), "age": int(age), "email": email.strip(),
                    "subject": subject.strip(), "emp_id": int(emp_id),
                })
                save_data(data)
                st.success(f"{name.strip()} has been registered.")
                teachers = [item for item in data["teachers"] if isinstance(item, dict)]

    with list_col:
        page_header("Directory", f"{len(teachers)} teacher record{'s' if len(teachers) != 1 else ''}.")
        if teachers:
            teacher_rows = [
                {"Teacher": item.get("name", "—"), "Employee ID": item.get("emp_id", "—"),
                 "Subject": item.get("subject", "—"), "Age": item.get("age", "—"), "Email": item.get("email", "—")}
                for item in teachers
            ]
            st.dataframe(pd.DataFrame(teacher_rows), hide_index=True, use_container_width=True)
            selected_label = st.selectbox("View teacher details", [f"{item.get('name', 'Unnamed teacher')} · #{item.get('emp_id', '—')}" for item in teachers])
            selected_index = [f"{item.get('name', 'Unnamed teacher')} · #{item.get('emp_id', '—')}" for item in teachers].index(selected_label)
            selected = teachers[selected_index]
            st.markdown(f"**{selected.get('name', '—')}**  \nEmployee ID: {selected.get('emp_id', '—')}  \nSubject: {selected.get('subject', '—')}  \nAge: {selected.get('age', '—')}  \nEmail: {selected.get('email', '—')}")
        else:
            st.info("No teachers have been registered yet.")


elif page == "Gradebook":
    if not students:
        st.info("Register a student first. Their grade records will appear here.")
    else:
        labels = [display_name(item) for item in students]
        selected_label = st.selectbox("Choose a student", labels)
        selected_index = labels.index(selected_label)
        selected = students[selected_index]
        current_grades = grade_values(selected)
        average = average_grade(selected)

        summary_col, form_col = st.columns([0.7, 1.3], gap="large")
        with summary_col:
            page_header("Student summary", "Current academic snapshot for this learner.")
        with form_col:
            page_header("Add or update a grade", "Saving another mark for the same subject updates its current value.")
            with st.form("grade_entry", clear_on_submit=True):
                subject = st.text_input("Subject", placeholder="For example, Mathematics")
                marks = st.number_input("Marks", min_value=0.0, max_value=100.0, step=0.5)
                submitted = st.form_submit_button("Save grade", use_container_width=True)
            if submitted:
                if not subject.strip():
                    st.error("Enter a subject before saving the grade.")
                else:
                    data_student = next(
                        item for item in data["students"]
                        if isinstance(item, dict) and id_matches(item.get("roll_no"), selected.get("roll_no"))
                    )
                    data_student.setdefault("grades", {})[subject.strip()] = float(marks)
                    save_data(data)
                    st.success(f"Saved {marks:g} marks for {subject.strip()}.")
                    current_grades = grade_values(data_student)
                    average = average_grade(data_student)
                    selected = data_student

        with summary_col:
            metric_card("Current average", f"{average:.1f}" if average is not None else "—", f"{len(current_grades)} subject{'s' if len(current_grades) != 1 else ''} recorded", "📈")

        st.write("")
        page_header("Subject marks", f"Grades for {selected.get('name', 'this student')}.")
        current_grades = grade_values(selected)
        if current_grades:
            grade_rows = [{"Subject": subject, "Marks": marks} for subject, marks in current_grades.items()]
            st.dataframe(pd.DataFrame(grade_rows), hide_index=True, use_container_width=True)
        else:
            st.info("No grades recorded for this student yet.")
