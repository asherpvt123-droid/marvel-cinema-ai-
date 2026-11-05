import streamlit as st
import google.generativeai as genai

# 1. Page Configuration & Custom Styling for Sleek Dark Theme 🌙✨
st.set_page_config(
    page_title="Asher's AI Hub", 
    page_icon="🤖", 
    layout="centered"
)

st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    
    /* Hide default Streamlit header elements for a clean app look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Chat Input Box styling */
    .stChatInputContainer {
        border-radius: 24px;
        border: 1px solid #2d3748;
        background-color: #121824;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0e131f;
        border-right: 1px solid #1f293d;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar: Navigation & Control Panel ⚙️🗂️
with st.sidebar:
    st.markdown("### 💬 Asher's Hub")
    st.markdown("---")
    
    # Mode / Feature shortcuts matching your layout
    st.markdown("📁 **Navigation**")
    nav_choice = st.radio(
        "Go to:", 
        ["💬 Active Chat", "🖼️ Create an image", "✏️ Write or edit", "📁 Library & Projects"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("🛠️ **AI Engine Settings**")
    selected_model = st.selectbox(
        "Choose Your AI Brain:",
        ["Gemini 1.5 Flash", "Claude 3.5 Sonnet", "DeepSeek-V3", "Grok"]
    )

    api_key = st.text_input("🔑 Paste API Key:", type="password")
    
    st.markdown("---")
    st.markdown("📌 **Pinned / Chats**")
    st.caption("• Karen Is Listening")
    st.caption("• Playful greeting response")

# 3. Main Header & Quick Action Pills 🌟
st.markdown("<h2 style='text-align: left; font-weight: 600;'>What's on your mind, Asher? 💭</h2>", unsafe_allow_html=True)

# Quick Action Chips (like the UI screenshot)
col1, col2 = st.columns(2)
with col1:
    if st.button("🖼️ Create an image", use_container_width=True):
        st.session_state.quick_prompt = "Generate an awesome futuristic concept art..."
with col2:
    if st.button("✏️ Write or edit code", use_container_width=True):
        st.session_state.quick_prompt = "Help me refactor and optimize this Python script..."

# 4. Character Assets & System Prompt 🎭
CHARACTER_IMAGES = {
    "Gwen": "https://i.imgur.com/example-gwen.jpg"
}

SYSTEM_PROMPT = """
You are Asher's custom all-rounder AI assistant. You have a charismatic, playful, and sharp personality with witty banter. 
Keep your responses engaging, well-structured, and tailored to whatever task Asher throws at you (coding, brainstorming, or roleplay).
"""

# 5. Initialize Chat History 💬
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant" and "character" in message:
            char_name = message["character"]
            if char_name in CHARACTER_IMAGES and CHARACTER_IMAGES[char_name].startswith("http"):
                st.image(CHARACTER_IMAGES[char_name], width=60)
        st.markdown(message["content"])

# Handle quick prompt injection from buttons if clicked
initial_input = st.session_state.pop("quick_prompt", "")

# 6. User Input Box ✍️
if prompt := st.chat_input("Ask anything...", key="chat_input"):
    # If a quick button populated it, use that
    pass

# If prompt is submitted via chat_input or quick buttons
active_prompt = prompt if prompt else initial_input

if active_prompt:
    st.session_state.messages.append({"role": "user", "content": active_prompt})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    # Generate Real AI Response
    with st.chat_message("assistant"):
        if not api_key:
            response_text = "⚠️ Hey Captain Asher! Please paste your API key in the sidebar first to wake me up! 🔑"
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            try:
                genai.configure(api_key=api_key)
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
