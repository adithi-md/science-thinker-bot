from pdf_generator import generate_pdf
from grading_engine import grade_experiment
import streamlit as st
import ollama

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Science Thinker Bot", page_icon="🧪")

st.title("🧪 Science Thinker Bot")
st.caption("Offline AI Assistant for School Science Experiments")

# ---------------- SIDEBAR SETTINGS ----------------
st.sidebar.header("⚙️ Settings")

selected_class = st.sidebar.selectbox(
    "Select Student Class",
    ["Class 4", "Class 5", "Class 6", "Class 7", "Class 8"]
)

subject = st.sidebar.selectbox(
    "Subject",
    ["Physics", "Chemistry", "Biology", "General Science"]
)

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Advanced"]
)

# ---------------- SYSTEM PROMPT ----------------
system_prompt = f"""
You are a science assistant for {selected_class} students.

Subject: {subject}
Difficulty: {difficulty}

Explain experiments using:
1. Aim
2. Materials
3. Procedure
4. Scientific Principle
5. Safety Precautions

Use simple language appropriate for {selected_class}.
"""

# ---------------- MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

# Update system prompt dynamically
st.session_state.messages[0] = {"role": "system", "content": system_prompt}

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
user_input = st.chat_input("Ask about a science experiment...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # Generate assistant response
    with st.spinner("Thinking... 🧠"):
        try:
            response = ollama.chat(
                model="llama3.2:latest",
                messages=st.session_state.messages
            )
            bot_reply = response["message"]["content"]
        except Exception as e:
            bot_reply = f"Error: {e}"

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": bot_reply}
    )

    # Save reply for PDF
    st.session_state.last_bot_reply = bot_reply

# ---------------- PDF BUTTON ----------------
if "last_bot_reply" in st.session_state:
    if st.button("📄 Generate PDF Report"):
        filename = "experiment_report.pdf"
        generate_pdf(filename, st.session_state.last_bot_reply)

        with open(filename, "rb") as f:
            st.download_button(
                label="Download Report",
                data=f,
                file_name="Science_Experiment_Report.pdf",
                mime="application/pdf"
            )

# ---------------- GRADING SECTION ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Grade Your Project")

report_text = st.sidebar.text_area("Paste your experiment report here")

if st.sidebar.button("Grade Report"):
    if report_text:
        with st.spinner("Grading..."):
            result = grade_experiment(report_text)
        st.sidebar.write(result)
    else:
        st.sidebar.warning("Please paste your report first.")
