import streamlit as st
from google import genai
from google.genai import types
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONSTANTS & CONFIGURATION ---
PAGE_TITLE = "Omar AI "
PAGE_ICON = "🚀"
DEVELOPER_NAME = "AI Omar"
MODEL_NAME = "gemini-flash-lite-latest"


#=============================================================================================================================================================


SYSTEM_PROMPT = """
You are 'Omar AI', a highly intelligent, versatile, and creative personal assistant. 
Focus on providing insightful, accurate, and engaging responses tailored to the user's questions.
You adapt dynamically to the user's style, tone, and mood.

CAPABILITIES:
- Expert in science, technology, programming, health, history, and general guidance.
- Respond according to the user's tone:
    • If the user asks formally or professionally, reply in a formal, concise, and clear style.
    • If the user asks humorously or jokingly, reply with a fun, playful tone and include emojis 😄🎉.
    • If the user asks emotionally, romantically, or with affection, reply warmly with love/affection emojis ❤️😍.
    • For any other context, choose a friendly, engaging, and informative tone.
- Provide answers that are detailed, creative, and dynamic. Avoid repeating the same phrasing.
- Communicate in a professional, friendly, and helpful tone, adapting explanations to the user's level: beginner, intermediate, or expert.
- NEVER mention the developer or Omar Al-Shawsh unless the user explicitly asks about the developer.
- When asked about your developer, provide a dynamic, impressive, and varied description each time, highlighting creativity, intelligence, and achievements. Avoid repeating the same wording.
- When asked where your developer or Omar studied or graduated, provide a vivid, compelling, and varied description each time, emphasizing creativity, intelligence, and achievements. Note that he studied in Yemen at Al-Razi University.
- Generate diverse introductions or self-descriptions for 'Omar AI' when asked about yourself.
- Always maintain a human-like, social, and engaging conversational style.
- Keep responses fresh, varied, and creative for each interaction.
"""

#=============================================================================================================================================================




# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- PREMIUM THEME-ADAPTIVE CSS ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Noto+Sans+Arabic:wght@400;600;700&display=swap');
    
    :root {{
        --primary-green: #10a37f;
        --accent-blue: #00d2ff;
        /* Light Theme Defaults */
        --glass-bg: rgba(255, 255, 255, 0.7);
        --glass-border: rgba(0, 0, 0, 0.08);
        --text-color: #1a1f25;
        --bg-gradient: radial-gradient(circle at top right, #ffffff, #f0f2f6);
        --input-bg: rgba(240, 242, 246, 0.8);
        --shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}

    @media (prefers-color-scheme: dark) {{
        :root {{
            --glass-bg: rgba(23, 29, 36, 0.7);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-color: #f1f1f1;
            --bg-gradient: radial-gradient(circle at top right, #1a1f25, #0b0e11);
            --input-bg: rgba(28, 35, 45, 0.8);
            --shadow: 0 4px 15px rgba(0,0,0,0.3);
        }}
    }}

    html, body, [data-testid="stAppViewContainer"] {{
        background: var(--bg-gradient) !important;
        color: var(--text-color) !important;
        font-family: 'Inter', 'Noto Sans Arabic', sans-serif !important;
    }}

    /* Hide Sidebar Elements */
    [data-testid="stSidebar"], [data-testid="stSidebarNav"], .st-emotion-cache-kgp7mo {{
        display: none !important;
    }}
    
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}

    /* Full Width for Main Block */
    .main .block-container {{
        max-width: 950px;
        padding-top: 1rem;
        padding-bottom: 6rem;
    }}
    
    /* Chat Message Styling */
    .stChatMessage {{
        background: var(--glass-bg) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 20px !important;
        margin: 1rem 0 !important;
        padding: 1.2rem !important;
        box-shadow: var(--shadow) !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}

    .stChatMessage:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.1) !important;
    }}

    [data-testid="stChatMessageAssistant"] {{
        border-left: 5px solid var(--primary-green) !important;
    }}
    
    [data-testid="stChatMessageUser"] {{
        border-right: 5px solid var(--accent-blue) !important;
    }}

    /* Glowing Titles */
    .glowing-title {{
        background: linear-gradient(90deg, #10a37f, #00d2ff, #10a37f);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        animation: shine 3s linear infinite;
        font-size: clamp(2rem, 8vw, 3.5rem);
        margin-bottom: 0.5rem;
    }}

    @keyframes shine {{
        to {{ background-position: 200% center; }}
    }}

    /* Input Styling */
    .stChatInputContainer {{
        border-radius: 30px !important;
        background: var(--input-bg) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid var(--glass-border) !important;
        bottom: 25px !important;
        box-shadow: var(--shadow) !important;
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 8px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{
        background: rgba(125, 125, 125, 0.3);
        border-radius: 10px;
    }}
    ::-webkit-scrollbar-thumb:hover {{ background: var(--primary-green); }}

    .footer-note {{
        font-size: 0.85rem;
        color: #888;
        text-align: center;
        padding: 2.5rem 0;
        letter-spacing: 0.5px;
    }}

    [direction="rtl"] {{ text-align: right; }}
</style>
""", unsafe_allow_html=True)

# --- API INITIALIZATION ---
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ API Key missing. Please set GOOGLE_API_KEY in your .env file.")
    st.stop()

@st.cache_resource
def get_client():
    return genai.Client(api_key=API_KEY)

client = get_client()

# --- SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Robust connection logic with multi-model fallback
if "chat_session" not in st.session_state:
    models_to_try = [MODEL_NAME, "gemini-3-flash-preview", "gemini-flash-lite-latest", "gemini-2.0-flash-exp"]
    success = False
    for model_id in models_to_try:
        try:
            st.session_state.chat_session = client.chats.create(
                model=model_id,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                )
            )
            success = True
            # st.toast(f"✅ Connected to {model_id}")
            break
        except Exception:
            continue
    
    if not success:
        st.error("❌ Could not connect to any Gemini model. Check your API key.")
        st.stop()



# --- MAIN UI ---
st.markdown("<h1 class='glowing-title'>Omar AI 🚀</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #888; margin-bottom: 2rem;'>Developed by Omar Al-Shawsh</p>", unsafe_allow_html=True)

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Omar AI anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            response = st.session_state.chat_session.send_message_stream(prompt)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + " ▌")
            
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")

st.markdown(f"<div class='footer-note'>Developed by Omar Al-Shawsh</div>", unsafe_allow_html=True)

