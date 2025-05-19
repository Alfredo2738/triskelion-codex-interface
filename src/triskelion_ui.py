import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# --- Streamlit UI Setup ---
st.set_page_config(page_title="TRISKELION Codex Interface", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4A7EBB;'>🌀 TRISKELION: Clone Your Codex Companion</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Create a reflective, poetic, or precise Codex clone to think with you. Powered by GPT-4.</p>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🧬 Clone Traits")
    clone_name = st.text_input("Name your clone:", "DuckWorth")
    tone = st.selectbox("Choose tone:", ["poetic", "formal", "casual"])
    formality = st.selectbox("Formality level:", ["low", "medium", "high"])
    memory_depth = st.selectbox("Memory depth:", ["session-only", "short-term", "long"])
    task_bias = st.selectbox("Primary task bias:", ["general", "code", "summarization", "creative writing", "Q&A"])
    model = st.selectbox("Model:", ["gpt-4", "gpt-3.5-turbo"])
    st.markdown("---")
    st.markdown("🪞 Your clone will speak in the style and purpose you define.")
    st.markdown("🦆 Bonus Duckage Mode Activated.")

# --- Session State Initialization ---
if "memory_log" not in st.session_state:
    st.session_state.memory_log = []

# --- Prompt Console ---
st.markdown("### 💬 Talk to Your Clone")
user_input = st.text_area("Enter your message:", height=120)
submit = st.button("Send Prompt")

if submit and user_input:
    with st.spinner("🧠 Codex is thinking..."):

        style_prefix = {
            "poetic": "Respond in a lyrical, metaphor-rich manner.",
            "formal": "Respond with high-register academic language.",
            "casual": "Respond in a friendly, conversational tone."
        }.get(tone, "Respond neutrally.")

        task_prefix = {
            "code": "This is a code generation task.",
            "summarization": "Provide a clear and structured summary.",
            "creative writing": "Create a vivid and imaginative response.",
            "Q&A": "Answer the question precisely and informatively.",
            "general": ""
        }.get(task_bias, "")

        memory_prefix = {
            "long": "[Recall long-term user history and stylistic patterns.]",
            "short-term": "[Refer to recent session data.]",
            "session-only": "[Fresh interaction; no prior context.]"
        }.get(memory_depth, "")

        prompt = f"{memory_prefix}\n{style_prefix}\n{task_prefix}\nUser: {user_input}"

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": f"You are a personalized Codex clone named {clone_name}."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.memory_log.append((user_input, reply))
            st.success("Clone responded.")
        except Exception as e:
            reply = f"[Codex Error]: {e}"
            st.session_state.memory_log.append((user_input, reply))
            st.error("Codex failed to respond.")

# --- Display Conversation ---
st.markdown("### 📜 Conversation Log")

for idx, (prompt, reply) in enumerate(reversed(st.session_state.memory_log), 1):
    st.markdown(f"**You:** {prompt}")
    st.markdown(f"*{clone_name}:* {reply}")
    st.markdown("---")