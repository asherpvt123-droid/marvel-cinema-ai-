import streamlit as st
import google.generativeai as genai

# 1. Page Configuration & Dark Theme 🌙✨
st.set_page_config(
    page_title="Asher's AI Hub", 
    page_icon="🤖", 
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stChatInputContainer {
        border-radius: 24px;
        border: 1px solid #2d3748;
        background-color: #121824;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #0e131f;
        border-right: 1px solid #1f293d;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Controls ⚙️🗂️
with st.sidebar:
    st.markdown("### 💬 Asher's Hub")
    st.markdown("---")
    
    st.markdown("📁 **Navigation**")
    nav_choice = st.radio(
        "Go to:", 
        ["💬 Active Chat", "🖼️ Create an image", "✏️ Write or edit", "📁 Library & Projects"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("🛠️ **AI Engine**")
    st.info("⚡ Powered by Gemini 3.8 Carbon")
    
    api_key = st.text_input("🔑 Paste API Key:", type="password")
    
    st.markdown("---")
    st.markdown("📌 **Pinned / Chats**")
    st.caption("• Karen Is Listening")
    st.caption("• Playful greeting response")

# 3. Main Header & Quick Action Pills 🌟
st.markdown("<h2 style='text-align: left; font-weight: 600;'>What's on your mind, Asher? 💭</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🖼️ Create an image", use_container_width=True):
        st.session_state.quick_prompt = "Generate an awesome futuristic concept art..."
with col2:
    if st.button("✏️ Write or edit code", use_container_width=True):
        st.session_state.quick_prompt = "Help me refactor and optimize this Python script..."

SYSTEM_PROMPT = """
You are Asher's custom all-rounder AI assistant (Carbon 3.8 engine). You have a charismatic, playful, and sharp personality with witty banter. 
Keep your responses engaging, well-structured, and tailored to whatever task Asher throws at you.
"""

# 4. Initialize Chat History 💬
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

initial_input = st.session_state.pop("quick_prompt", "")
prompt = st.chat_input("Ask anything...")
active_prompt = prompt if prompt else initial_input

# 5. Generation Block with Gemini 3.8 Flash / Carbon 🧠⚡
if active_prompt:
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    with st.chat_message("assistant"):
        if not api_key:
            response_text = "⚠️ Hey Captain Asher! Please paste your API key in the sidebar first to wake up your Carbon engine! 🔑"
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            try:
                genai.configure(api_key=api_key)
                # Updated to Gemini 3.8 Flash engine
                model = genai.GenerativeModel('gemini-3.8-flash', system_instruction=SYSTEM_PROMPT)
                
                chat_history = []
                for msg in st.session_state.messages[:-1]:
                    role_map = "user" if msg["role"] == "user" else "model"
                    chat_history.append({"role": role_map, "parts": [msg["content"]]})
                
                chat = model.start_chat(history=chat_history)
                response = chat.send_message(active_prompt)
                response_text = response.text
                
                st.markdown(response_text)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response_text
                })
            except Exception as e:
                error_msg = f"⚠️ Oops Captain Asher, an error occurred: {e}"
                st.markdown(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
