import streamlit as st
import google.generativeai as genai

# 1. Page Configuration & Pitch-Black Dark Theme (ChatGPT Mobile Aesthetic) 🌙✨
st.set_page_config(
    page_title="Asher's AI Hub", 
    page_icon="🤖", 
    layout="centered"
)

st.markdown("""
    <style>
    /* Global Pitch-Black Theme */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sleek Floating Chat Input */
    .stChatInputContainer {
        border-radius: 28px !important;
        border: 1px solid #2d3748 !important;
        background-color: #121824 !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
    }
    
    /* Side Drawer Navigation Styling */
    section[data-testid="stSidebar"] {
        background-color: #0e131f;
        border-right: 1px solid #1f293d;
    }
    
    /* Action Pill Buttons */
    .stButton>button {
        background-color: #121824;
        color: #f3f4f6;
        border: 1px solid #2d3748;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1f293d;
        border-color: #4a5568;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Side Drawer Navigation & Settings (ChatGPT App Style) ⚙️🗂️
with st.sidebar:
    st.markdown("### 💬 Asher's Hub")
    st.markdown("---")
    
    st.markdown("📁 **Workspace Navigation**")
    nav_choice = st.radio(
        "Go to:", 
        ["💬 Active Chat", "🖼️ Images & Media", "✏️ Code & Writing", "📁 Library & Projects"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("🛠️ **Engine Settings**")
    st.info("⚡ Powered by Gemini 1.5 Flash")
    
    api_key = st.text_input("🔑 Paste API Key:", type="password")
    
    st.markdown("---")
    st.markdown("📌 **Pinned & History**")
    st.caption("• Karen Is Listening")
    st.caption("• Playful greeting response")
    st.caption("• Epic Cinematic Universe Arc")

# 3. Main Header & Shortcut Chips 🌟
st.markdown("<h2 style='text-align: left; font-weight: 600; font-size: 1.5rem;'>What's on your mind, Asher? 💭</h2>", unsafe_allow_html=True)

# Shortcut action pills matching your layout screenshot
col1, col2 = st.columns(2)
with col1:
    if st.button("🖼️ Create an image", use_container_width=True):
        st.session_state.quick_prompt = "Generate an awesome futuristic concept art..."
with col2:
    if st.button("✏️ Write or edit", use_container_width=True):
        st.session_state.quick_prompt = "Help me refactor and optimize this code segment..."

# 4. System Prompt & Personality Core 🎭
SYSTEM_PROMPT = """
You are Asher's custom all-rounder AI assistant. You have a charismatic, playful, and sharp personality with witty banter. 
Your primary goal is to help Asher maintain an expansive, uninterrupted storyline, write code, and brainstorm complex ideas with high creativity and context retention.
"""

# 5. Initialize Persistent Chat History 💬
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle quick button injection
initial_input = st.session_state.pop("quick_prompt", "")
prompt = st.chat_input("Ask anything...")
active_prompt = prompt if prompt else initial_input

# 6. Real Gemini 1.5 Flash Generation Loop 🧠⚡
if active_prompt:
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    with st.chat_message("assistant"):
        if not api_key:
            response_text = "⚠️ Hey Captain Asher! Please paste your API key in the side drawer first to wake me up! 🔑"
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            try:
                genai.configure(api_key=api_key)
                # Configured to Gemini 1.5 Flash for high daily limits and massive stability
                model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=SYSTEM_PROMPT)
                
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
