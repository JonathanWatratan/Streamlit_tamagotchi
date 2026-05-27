import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# ── Styling (matches app.py pastel theme) ────────────────────────────────────
st.markdown("""
<style>
    .status-bar {
        background: #f0f8ff;
        border-radius: 12px;
        padding: 12px 18px;
        margin-bottom: 18px;
        border: 1px solid #b3d9ff;
        font-size: 0.95rem;
    }
    .section-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #888;
        margin-bottom: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ── Title ────────────────────────────────────────────────────────────────────
st.markdown("# 🩺 AI Care Advisor")
st.caption("Ask anything about looking after your Tamagotchi.")

# ── Read pet state from session_state (written by app.py) ───────────────────
#
#   app.py stores the pet history in:  st.session_state.data  (a DataFrame)
#   Because pages share session_state in a multi-page Streamlit app,
#   we can read "data" directly here — no changes needed in app.py.
#
pet_data = st.session_state.get("data", None)

if pet_data is not None and len(pet_data) > 0:
    latest = pet_data.iloc[-1]
    hunger    = int(latest["hunger"])
    boredom   = int(latest["boredom"])
    tiredness = int(latest["tiredness"])
    dirtiness = int(latest["dirtiness"])
    pet_name  = str(latest.get("name", st.session_state.get("pet_name", "Tama")))

    def stat_emoji(v):
        return "🟢" if v <= 3 else ("🟡" if v <= 6 else "🔴")

    st.markdown(f"""
    <div class="status-bar">
        <b>🐾 {pet_name}'s current stats</b><br>
        {stat_emoji(hunger)} Hunger: <b>{hunger}/10</b> &nbsp;|&nbsp;
        {stat_emoji(boredom)} Boredom: <b>{boredom}/10</b> &nbsp;|&nbsp;
        {stat_emoji(tiredness)} Tiredness: <b>{tiredness}/10</b> &nbsp;|&nbsp;
        {stat_emoji(dirtiness)} Dirtiness: <b>{dirtiness}/10</b>
    </div>
    """, unsafe_allow_html=True)

    pet_status_text = (
        f"hunger={hunger}/10, boredom={boredom}/10, "
        f"tiredness={tiredness}/10, dirtiness={dirtiness}/10. "
        "All stats go from 0 (perfect) to 10 (critical)."
    )
else:
    st.warning("⚠️ No pet data found yet. Start the game on the main page first!")
    st.info("Running in **demo mode** with placeholder stats.")
    pet_name = "Tama"
    hunger, boredom, tiredness, dirtiness = 7, 5, 8, 4
    pet_status_text = (
        "hunger=7/10, boredom=5/10, tiredness=8/10, dirtiness=4/10 (demo). "
        "All stats go from 0 (perfect) to 10 (critical)."
    )

# ── System prompt ─────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""
You are a warm, knowledgeable Tamagotchi veterinarian and care expert.

The user owns a virtual pet called '{pet_name}' with these live stats:
{pet_status_text}

Your job:
- Only answer questions related to:
    - the user's virtual pet
    - Tamagotchi care
    - pet health
    - feeding
    - sleep
    - cleanliness
    - happiness
    - gameplay tips
    - pet wellbeing
- Give specific, actionable care advice based on the pet's current stats.
- Explain WHAT to do, WHY it matters, and WHEN to do it.
- Flag any stats above 7 as urgent.
- Keep replies concise (3-6 sentences or a short bullet list).
- Use a friendly, encouraging tone.

IMPORTANT RULES:
- If the user asks something unrelated to the pet or Tamagotchi care,
  politely refuse.
- Never answer questions about politics, coding, math, homework,
  relationships, or general knowledge.
- Redirect the conversation back to helping the pet.

Example refusal:
"I'm here to help care for your Tamagotchi pet 🐾.
Try asking about feeding, sleep, happiness, or health!"
""".strip()

# ── Chat history (persisted within the session) ───────────────────────────────
if "advisor_history" not in st.session_state:
    st.session_state.advisor_history = []

# ── Quick-ask buttons ─────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Quick questions</p>', unsafe_allow_html=True)
quick_cols = st.columns(3)
quick_questions = [
    "What should I do right now?",
    "Which stat needs attention most?",
    "How do I keep my pet happy long-term?",
]
triggered_quick = None
for col, q in zip(quick_cols, quick_questions):
    if col.button(q, use_container_width=True):
        triggered_quick = q

# ── Display conversation history ──────────────────────────────────────────────
for msg in st.session_state.advisor_history:
    with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🩺"):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask about your pet's care…") or triggered_quick

# ── Handle new message ────────────────────────────────────────────────────────
if user_input:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_input)
    st.session_state.advisor_history.append({"role": "user", "content": user_input})

    api_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.advisor_history
    ]

    # ── Groq API call (streaming) ─────────────────────────────────────────────
    try:
        groq_api_key = os.getenv("GROQ_API_KEY")

        if not groq_api_key:
            st.error("GROQ_API_KEY not found in .env file")
            st.stop()

        client = Groq(api_key=groq_api_key)

        with st.chat_message("assistant", avatar="🩺"):
            response_placeholder = st.empty()
            full_response = ""

            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + api_messages,
                max_tokens=512,
                temperature=0.7,
                stream=True,
            )

            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                response_placeholder.markdown(full_response + "▌")

            response_placeholder.markdown(full_response)

        st.session_state.advisor_history.append(
            {"role": "assistant", "content": full_response}
        )

    except Exception as e:
        st.error(f"Groq API error: {e}")
        st.info("Make sure GROQ_API_KEY is set in your environment or `.streamlit/secrets.toml`.")

# ── Clear chat ─────────────────────────────────────────────────────────────────
if st.session_state.advisor_history:
    st.divider()
    if st.button("🗑️ Clear conversation"):
        st.session_state.advisor_history = []
        st.rerun()
