import streamlit as st
from agents import Agent, CriticAgent
from utils import setup_openai_client, extract_file_text
import openai

st.set_page_config(page_title="⚖️ AI Courtroom Simulation", layout="wide")

# --- Sidebar for OpenAI API Key ---
st.sidebar.header("🔑 API Key Configuration")
openai_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if not openai_key:
    st.warning("Please enter your OpenAI API Key to continue.")
    st.stop()

openai_client = setup_openai_client(openai_key)

# --- Sidebar: File Upload ---
st.sidebar.subheader("📁 Upload Case File (PDF/DOCX)")
uploaded_file = st.sidebar.file_uploader("Choose a case file", type=["pdf", "docx"])

case_context = ""
if uploaded_file:
    case_context = extract_file_text(uploaded_file)
    st.sidebar.success("✅ Case file loaded and processed.")

# --- System Prompts Based on Uploaded File ---
lawyer_prompt = f"You are a sharp and persuasive lawyer presenting strong legal arguments. Use this case as context:\n\n{case_context}"
judge_prompt = f"You are a neutral and wise judge responding with legal logic. Use this case file as context:\n\n{case_context}"
critic_prompt = "You are a legal scholar who evaluates legal arguments and courtroom interactions."

# --- Initialize Agents ---
lawyer = Agent("Lawyer", "Legal Advocate", lawyer_prompt)
judge = Agent("Judge", "Legal Authority", judge_prompt)
critic = CriticAgent(system_prompt=critic_prompt)

# --- Main Title ---
st.title("⚖️ AI Courtroom Simulation (Lawyer vs Judge + Critic)")

# --- User Input ---
initial_msg = st.text_input("💼 Lawyer's Opening Argument", value="NetPlus Pvt Ltd should be held accountable for misinformation on their platform.")

num_rounds = st.slider("🔁 Number of Rounds", 1, 5, 3)

# --- Run Simulation ---
if st.button("🎬 Start Simulation") and initial_msg:
    lawyer_msg = initial_msg
    log = []

    for i in range(num_rounds):
        judge_msg = judge.respond(lawyer_msg, openai)
        lawyer_msg = lawyer.respond(judge_msg, openai)
        critique = critic.evaluate(lawyer_msg, judge_msg, openai)

        log.append((f"💼 Lawyer (Round {i+1})", lawyer_msg))
        log.append((f"👨‍⚖️ Judge (Round {i+1})", judge_msg))
        log.append((f"🧠 Critic Feedback (Round {i+1})", critique))

    st.markdown("## 📜 Courtroom Dialogue & Critique")

    for role, msg in log:
        st.markdown(f"**{role}**:")
        st.markdown(msg)
        st.markdown("---")

    lawyer.reset()
    judge.reset()
