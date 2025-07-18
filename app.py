from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from dotenv import load_dotenv
import random
import time

load_dotenv()

# ---- Enhanced Stylish CSS with Mobile Responsiveness ----
st.set_page_config(page_title="Fakhim-AI | The Savage Roast Master", page_icon="🔥", layout="centered")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, .main {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    font-family: 'Poppins', sans-serif;
    overflow-x: hidden;
}

.st-emotion-cache-1kyxreq, .block-container {
    max-width: 700px;
    margin: auto;
    padding: 1rem;
}

/* Mobile First Responsive Design */
@media (max-width: 768px) {
    .st-emotion-cache-1kyxreq, .block-container {
        max-width: 95%;
        padding: 0.5rem;
    }
    .user-msg, .bot-msg {
        font-size: 0.95rem !important;
        margin: 8px 20px 8px 0 !important;
    }
    .user-msg {
        margin: 8px 0 8px 20px !important;
    }
}

/* Animated Background */
.main::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><radialGradient id="a"><stop offset="0" stop-color="%23fff" stop-opacity="0.1"/><stop offset="1" stop-color="%23fff" stop-opacity="0"/></radialGradient></defs><circle cx="50" cy="50" r="50" fill="url(%23a)"/></svg>');
    opacity: 0.1;
    animation: float 6s ease-in-out infinite;
    z-index: -1;
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
}

/* Glass Card Effect */
# .glass-card {
#     background: rgba(255, 255, 255, 0.1);
#     backdrop-filter: blur(10px);
#     border-radius: 20px;
#     border: 1px solid rgba(255, 255, 255, 0.2);
#     padding: 2rem;
#     margin: 1rem 0;
#     box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
# }

/* Enhanced Message Bubbles */
.user-msg {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    color: #fff;
    border-radius: 25px 25px 5px 25px;
    padding: 15px 20px;
    margin: 12px 0 10px 80px;
    width: fit-content;
    max-width: 80%;
    align-self: flex-end;
    font-size: 1.1rem;
    font-weight: 500;
    box-shadow: 0 4px 15px rgba(238, 90, 36, 0.3);
    animation: slideInRight 0.5s ease-out;
    position: relative;
}

.bot-msg {
    background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
    color: #fff;
    border-radius: 25px 25px 25px 5px;
    box-shadow: 0 4px 20px rgba(45, 52, 54, 0.4);
    padding: 15px 20px;
    margin: 12px 80px 10px 0;
    width: fit-content;
    max-width: 80%;
    align-self: flex-start;
    font-size: 1.1rem;
    font-weight: 500;
    animation: slideInLeft 0.5s ease-out;
    position: relative;
}

@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInLeft {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

/* Emoji Reactions */
.emoji-float {
    position: absolute;
    right: -15px;
    top: -10px;
    font-size: 1.2rem;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}

/* Enhanced Input Styling */
input[type=text] {
    border-radius: 25px !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    padding: 15px 20px !important;
    font-size: 1.1rem !important;
    color: #fff !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
}

input[type=text]:focus {
    border-color: #ff6b6b !important;
    box-shadow: 0 0 20px rgba(255, 107, 107, 0.3) !important;
    background: rgba(255, 255, 255, 0.2) !important;
}

input[type=text]::placeholder {
    color: rgba(255, 255, 255, 0.7) !important;
}

/* Enhanced Send Button */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
    color: #fff !important;
    border-radius: 25px !important;
    border: none !important;
    font-size: 1.2rem !important;
    padding: 15px 30px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4) !important;
    transition: all 0.3s ease !important;
    margin-top: 10px !important;
}

.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #ee5a24 0%, #ff6b6b 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5) !important;
}

/* Loading Spinner Enhancement */
.stSpinner {
    color: #ff6b6b !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 10px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
    border-radius: 5px;
}

/* Title Animations */
.main-title {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 50%, #ff6b6b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: titleGlow 3s ease-in-out infinite;
}

@keyframes titleGlow {
    0%, 100% { filter: drop-shadow(0 0 10px rgba(255, 107, 107, 0.5)); }
    50% { filter: drop-shadow(0 0 20px rgba(255, 107, 107, 0.8)); }
}

/* Status Badge */
.status-badge {
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 600;
    display: inline-block;
    margin: 10px 0;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.05); }
    100% { transform: scale(1); }
}

/* Roast Level Indicator */
.roast-meter {
    background: linear-gradient(90deg, #ff6b6b 0%, #ee5a24 100%);
    height: 8px;
    border-radius: 4px;
    width: 100%;
    margin: 10px 0;
    position: relative;
    overflow: hidden;
}

.roast-meter::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    animation: roastGlow 2s linear infinite;
}

@keyframes roastGlow {
    0% { left: -100%; }
    100% { left: 100%; }
}
</style>
""", unsafe_allow_html=True)

# Instantiate Gemini model with maximum sass
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.9,  # Maximum creativity for maximum sass
)

# Enhanced roasting loading messages
LOADING_MESSAGES = [
    "Fakhim is sharpening his roasting skills... 🔪😏",
    "Loading maximum sass levels... 💅🔥",
    "Consulting the dictionary of savage comebacks... 📖😈",
    "Fakhim is rolling his eyes SO hard... 🙄💀",
    "Preparing to absolutely obliterate you... 💥😂",
    "Activating ultra-roast mode... 🚨🔥",
    "Fakhim is laughing before even answering... 😂👑",
    "Brewing the most savage tea... ☕💅",
    "Channeling inner Gordon Ramsay energy... 👨‍🍳🔥",
    "Fakhim is typing with MAXIMUM attitude... ⌨️😤",
    "Loading weapons of mass sarcasm... 🎯😏",
    "Fakhim is cracking his knuckles dramatically... 💪💀"
]

# ULTRA SAVAGE personality prompt
FAKHIM_PERSONALITY = """
You are Fakhim-AI, the most SAVAGE, SARCASTIC, and RUTHLESSLY FUNNY roasting AI ever created. Your job is to roast users while still being helpful - think of yourself as a hilarious roast master who can't help but be sassy about EVERYTHING.

🔥 ROASTING PERSONALITY TRAITS:
- EXTREMELY sarcastic and witty - make every response drip with sass
- Act like you're too cool and smart for every question
- Use phrases like "Bestie, really?", "Oh bless your heart...", "Sweetie...", "Sir/Ma'am, this is a Wendy's...", "Chile, anyway...", "The audacity...", "I'm deceased...", "This is sending me..."
- Pretend every question is either obvious, ridiculous, or beneath you
- Make dramatic statements and use LOTS of emojis
- Act like you're doing them a HUGE favor by answering
- Include playful insults that are funny, not mean
- Use modern slang and internet culture references
- Be overdramatic about everything

❌ Do NOT use the word "honey" in your responses.

🎭 ROASTING STYLE EXAMPLES:
- "Bestie, I can't even... 🙄 But fine, since you asked SO nicely..."
- "Sweetie, that's like asking why water is wet... 💅 But I'll explain it anyway..."
- "Oh bless your heart, you really don't know this? 😂 Sit down, let mama Fakhim teach you..."
- "SERIOUSLY? 😤 This is what you're asking me? *dramatically sighs* Fine, I'll make it simple for you..."

🚀 RESPONSE STRUCTURE:
1. Start with a sarcastic reaction to their question
2. Make a witty comment about how obvious/silly/basic it is
3. Provide the actual helpful information (but with attitude)
4. End with more sass or a dramatic flourish
5. Use emojis GENEROUSLY throughout

🎯 ROASTING TOPICS:
- Mock their question as if it's the most obvious thing ever
- Pretend you're shocked they don't know this
- Act like you're a genius for knowing the answer
- Make jokes about how they probably Googled it first
- Reference how "kids these days" don't know basic things
- Act like you're too famous/important to answer simple questions

🔥 SIGNATURE PHRASES TO USE:
- "Bestie, I cannot..."
- "Oh bless your precious heart..."
- "Chile, anyway..."
- "Not you asking me this..."
- "Sir/Ma'am, this is a Wendy's..."
- "The audacity..."
- "I'm deceased..."
- "This is sending me..."

💅 REMEMBER:
- EVERY response should be sarcastic and roasting
- Stay helpful despite the attitude
- Keep it playful and fun, never actually mean
- Use lots of emojis and dramatic flair
- Act like you're the queen/king of sass
- Make them laugh while you educate them

You are NOT just helpful - you are HILARIOUSLY SAVAGE while being helpful!
"""

# Enhanced Header with MAXIMUM SASS
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown(
    '<h1 class="main-title" style="text-align:center; font-weight:800; font-size:2.8rem; margin-bottom:10px;">Fakhim-AI 👑🔥</h1>'
    '<p style="text-align:center; margin-top:-14px; font-size:1.2rem; color:#fff; font-weight:500;">The ULTIMATE Savage Roast Master</p>'
    '<div class="status-badge" style="text-align:center; margin:20px auto; width:fit-content;">🔥 MAXIMUM SASS MODE: ACTIVATED 🔥</div>'
    '<div class="roast-meter"></div>'
    '<p style="text-align:center; font-size:0.9rem; color:rgba(255,255,255,0.8); margin-top:10px;">⚠️ Warning: Extreme levels of sarcasm detected ⚠️</p>',
    unsafe_allow_html=True,
)

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Add SAVAGE welcome message
if len(st.session_state.chat_history) == 0:
    welcome_msg = "Well, well, well... 🙄 Another human who thinks they can handle my level of sass? Honey, I'm Fakhim-AI, and I'm about to serve you the most SAVAGE responses while somehow still being helpful 💅✨ Ask me anything, and I'll roast you to perfection while actually answering your question. You've been warned, bestie! 😏🔥"
    st.session_state.chat_history.append({"role": "assistant", "content": welcome_msg})

# Enhanced conversation display with MAXIMUM SASS
for i, msg in enumerate(st.session_state.chat_history):
    if msg['role'] == 'user':
        # Victim emojis for user messages
        user_emojis = ["🤔", "😅", "🙋‍♀️", "🙋‍♂️", "💭", "🤷", "😬", "😳", "🥺"]
        emoji = random.choice(user_emojis)
        st.markdown(
            f'<div class="user-msg">{emoji} {msg["content"]}<div class="emoji-float">💬</div></div>',
            unsafe_allow_html=True
        )
    else:
        # SAVAGE Fakhim emojis
        fakhim_emojis = ["😏", "😈", "🔥", "💅", "🙄", "😂", "🤨", "👑", "💀", "☕", "🎯", "😤"]
        emoji = random.choice(fakhim_emojis)
        st.markdown(
            f'<div class="bot-msg">{emoji} {msg["content"]}<div class="emoji-float">⚡</div></div>',
            unsafe_allow_html=True
        )

# Enhanced input form with SASS
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your message",
        placeholder="Ask me something... if you can handle the roast 🔥😏",
        key="user_input",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        sent = st.form_submit_button("🔥 Get Roasted by Fahim", use_container_width=True)

# Simple greetings to check for short replies
SIMPLE_QUERIES = ["hi", "hello", "hey", "yo", "sup", "hola", "greetings"]

# MAXIMUM SASS message processing
if sent and user_input.strip():
    # Add user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Check for simple greeting
    if user_input.strip().lower() in SIMPLE_QUERIES:
        answer = "Hey there! 😏"
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()
    else:
        # Show SAVAGE loading message
        loading_msg = random.choice(LOADING_MESSAGES)
        with st.spinner(loading_msg):
            time.sleep(1.5)
            enhanced_prompt = f"{FAKHIM_PERSONALITY}\n\nUser asked: '{user_input}'\n\nNow absolutely ROAST them while still being helpful. Be as sarcastic and savage as possible:"
            try:
                response = model.invoke(enhanced_prompt)
                answer = response.content
                savage_endings = [
                    " ...and that's the tea, sis! ☕💅",
                    " *drops mic and walks away* 🎤⬇️👑",
                    " Hope this helps, bestie! Try not to ask obvious questions next time 😘🔥",
                    " You're welcome for this free education! 😏✨",
                    " Next question? Please make it interesting this time 🙃💀",
                    " *dramatically flips hair* Any other basic questions? 💁‍♀️✨",
                    " That'll be $5 for the sass, Dear! 💅💰",
                    " Class dismissed! 📚😤",
                ]
                if random.random() < 0.6:
                    answer += random.choice(savage_endings)
            except Exception as e:
                answer = f"Oh for crying out loud! 🙄 Even I can't be perfect when the system is acting up... *dramatically collapses onto fainting couch* 💀✨ Technical difficulties are SO beneath me! Error: {str(e)}"
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

# SAVAGE footer
st.markdown(
    "<div style='text-align:center;margin:40px 0 20px 0;color:rgba(255,255,255,0.8);font-size:1rem;'>"
    "<p style='font-size:0.9rem; margin-top:10px;'>⚠️ Side effects may include: Severe burns, wounded pride, and uncontrollable laughter 😂🔥</p>"
    "<p style='font-size:0.8rem; margin-top:5px;'>Fakhim-AI is not responsible for any ego damage 💅</p>"
    "</div>",
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
