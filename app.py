import streamlit as st
import google.generativeai as genai

# 1. Page Title & Styling (Dark Mode Cinematic Vibe) 🌙🎬
st.set_page_config(
    page_title="Asher's Marvel Cinema Hub", 
    page_icon="🎬", 
    layout="centered"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🎬 Asher's Marvel Cinematic Universe</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8888ff;'>*Where the script comes alive with live character profile cards.*</p>", unsafe_allow_html=True)

# 2. Sidebar: Model Selector & API Key ⚙️🧠
st.sidebar.header("🛠️ Control Panel")
selected_model = st.sidebar.selectbox(
    "Choose Your AI Brain:",
    ["Gemini 2.5 Flash / Carbon", "Claude 3.5 Sonnet", "DeepSeek-V3", "Grok"]
)

# Grab the key you saved in your Samsung Notes!
api_key = st.sidebar.text_input("Paste API Key:", type="password")

# 3. Director's Rulebook & Character Asset Mapping 🎭📸
CHARACTER_IMAGES = {
    "Peter": "https://i.imgur.com/example-peter.jpg",  # Replace with your hosted Tom Holland image URL or local path
    "Gwen": "https://i.imgur.com/example-gwen.jpg",    # Replace with your hosted Mckenna Grace image URL or local path
    "May": "https://i.imgur.com/example-may.jpg"
}

SYSTEM_PROMPT = """
You are an advanced cinematic roleplay engine running Asher's custom Marvel universe. 
CRITICAL FORMATTING RULE: 
Whenever a character speaks or performs an action, structure it like a script/messaging app block. Always include their character name clearly, followed by their dialogue or action. Keep the tone deeply immersive and cinematic.
"""

# 4. Initialize Chat History 💬
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # If it's an assistant message with a character tag, check for avatar
        if message["role"] == "assistant" and "character" in message:
            char_name = message["character"]
            if char_name in CHARACTER_IMAGES:
                st.image(CHARACTER_IMAGES[char_name], width=60)
        st.markdown(message["content"])

# 5. User Input Box (Directing the scene) ✍️
if prompt := st.chat_input("Direct the next scene, Asher..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        if not api_key:
            response_text = "⚠️ Hey Captain Asher! Please paste your API key in the sidebar first to wake me up! 🔑"
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        else:
            # Here is where the AI processes the scene based on your input
            # (Mocking a dynamic response matching your requested style)
            simulated_character = "Gwen"
            response_text = f"**{simulated_character}:**\n\n\"Pssst 😂 Can I tell you something? And don't you dare send me that chicken video again 😭💖\""
            
            # Display character profile picture alongside text just like your screenshots!
            if simulated_character in CHARACTER_IMAGES:
                st.image(CHARACTER_IMAGES[simulated_character], width=70)
                
            st.markdown(response_text)
            
            # Save assistant message with character tag
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response_text, 
                "character": simulated_character
            })
