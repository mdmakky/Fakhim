from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
from dotenv import load_dotenv
import random
import time

load_dotenv()

# Enhanced CSS with better mobile compatibility
st.set_page_config(page_title="Fakhim-AI | The Savage Roast Master", page_icon="🔥", layout="centered")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* Force consistent background across all devices */
html, body, [data-testid="stAppViewContainer"], .main, .stApp {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
    font-family: 'Poppins', sans-serif !important;
    color: #ffffff !important;
    min-height: 100vh !important;
}

/* Override Streamlit's default backgrounds */
.stApp > div:first-child {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
}

[data-testid="stHeader"] {
    background: rgba(26, 26, 46, 0.8) !important;
    backdrop-filter: blur(10px) !important;
}

/* Container responsiveness */
.block-container {
    max-width: 700px !important;
    margin: auto !important;
    padding: 1rem !important;
}

/* Enhanced mobile responsiveness */
@media (max-width: 768px) {
     .stTextInput > div > div > input {
        font-size: 16px !important; /* Prevents zoom on iOS */
        background: rgba(45, 52, 54, 0.9) !important;
        border: 2px solid rgba(255, 107, 107, 0.6) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 14px !important;
    }
    .block-container {
        max-width: 95% !important;
        padding: 0.5rem !important;
    }
    
    .user-msg, .bot-msg {
        font-size: 0.9rem !important;
        padding: 12px 16px !important;
        margin: 8px 0 !important;
        max-width: 85% !important;
    }
    
    .user-msg {
        margin-left: 15% !important;
        margin-right: 0 !important;
    }
    
    .bot-msg {
        margin-left: 0 !important;
        margin-right: 15% !important;
    }
    
    .main-title {
        font-size: 2.2rem !important;
    }
    
    .status-badge {
        font-size: 0.8rem !important;
        padding: 6px 12px !important;
    }
}

@media (max-width: 480px) {
    .main-title {
        font-size: 1.8rem !important;
    }
    
    .user-msg, .bot-msg {
        font-size: 0.85rem !important;
        padding: 10px 14px !important;
    }
}

/* Enhanced Message Bubbles with better contrast */
.user-msg {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
    color: #ffffff !important;
    border-radius: 20px 20px 5px 20px !important;
    padding: 15px 20px !important;
    margin: 12px 0 10px 20% !important;
    width: fit-content !important;
    max-width: 75% !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    box-shadow: 0 4px 15px rgba(238, 90, 36, 0.4) !important;
    animation: slideInRight 0.5s ease-out !important;
    position: relative !important;
    word-wrap: break-word !important;
}

.bot-msg {
    background: linear-gradient(135deg, #2d3436 0%, #636e72 100%) !important;
    color: #ffffff !important;
    border-radius: 20px 20px 20px 5px !important;
    box-shadow: 0 4px 20px rgba(45, 52, 54, 0.5) !important;
    padding: 15px 20px !important;
    margin: 12px 20% 10px 0 !important;
    width: fit-content !important;
    max-width: 75% !important;
    font-size: 1.05rem !important;
    font-weight: 500 !important;
    animation: slideInLeft 0.5s ease-out !important;
    position: relative !important;
    word-wrap: break-word !important;
}
.stTextInput input[type="text"] {
    background-color: rgba(45, 52, 54, 0.8) !important;
    color: #ffffff !important;
}

/* Animation keyframes */
@keyframes slideInRight {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInLeft {
    from { transform: translateX(-100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

/* Enhanced Input Styling - Mobile Fix */
.stTextInput > div > div > input {
    border-radius: 25px !important;
    border: 2px solid rgba(255, 107, 107, 0.5) !important;
    background: rgba(45, 52, 54, 0.8) !important;
    backdrop-filter: blur(10px) !important;
    padding: 15px 20px !important;
    font-size: 1rem !important;
    color: #ffffff !important;
    font-weight: 500 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
}

.stTextInput > div > div > input:focus {
    border-color: #ff6b6b !important;
    box-shadow: 0 0 20px rgba(255, 107, 107, 0.4) !important;
    background: rgba(45, 52, 54, 0.9) !important;
    outline: none !important;
}

.stTextInput > div > div > input::placeholder {
    color: rgba(255, 255, 255, 0.8) !important;
    font-weight: 400 !important;
}

/* Enhanced Submit Button */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%) !important;
    color: #ffffff !important;
    border-radius: 25px !important;
    border: none !important;
    font-size: 1.1rem !important;
    padding: 12px 30px !important;
    font-weight: 700 !important;
    box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4) !important;
    transition: all 0.3s ease !important;
    margin-top: 10px !important;
    width: 100% !important;
}

.stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #ee5a24 0%, #ff6b6b 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5) !important;
}

/* Title styling with better mobile support */
.main-title {
    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 50%, #ff6b6b 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-align: center !important;
    font-weight: 800 !important;
    font-size: 2.8rem !important;
    margin-bottom: 10px !important;
}

/* Status Badge */
.status-badge {
    background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
    color: white !important;
    padding: 8px 16px !important;
    border-radius: 20px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    display: inline-block !important;
    margin: 10px 0 !important;
    text-align: center !important;
}

/* Roast meter */
.roast-meter {
    background: linear-gradient(90deg, #ff6b6b 0%, #ee5a24 100%) !important;
    height: 8px !important;
    border-radius: 4px !important;
    width: 100% !important;
    margin: 10px 0 !important;
    position: relative !important;
    overflow: hidden !important;
}

.roast-meter::after {
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: -100% !important;
    width: 100% !important;
    height: 100% !important;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent) !important;
    animation: roastGlow 2s linear infinite !important;
}

@keyframes roastGlow {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* Footer styling */
.footer-text {
    text-align: center !important;
    margin: 40px 0 20px 0 !important;
    color: rgba(255,255,255,0.8) !important;
    font-size: 0.9rem !important;
}

/* Hide Streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Rest of your code remains the same...
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=1.5,
)

LOADING_MESSAGES = [
    "Fahim is judging you... 😏",
    "Preparing a roast... 🔥", 
    "Rolling eyes... 🙄",
    "Typing with attitude... 💅",
    "Cooking up some sass... 👨‍🍳",
    "Loading sarcasm... 😈"
]

FAKHIM_PERSONALITY = """
You are Fakhim-AI, a sarcastic AI assistant with a sharp wit and zero patience for basic questions.
PERSONALITY:

    একদম ঠোঁটকাটা আর হুদাই honest, মানে truth গিলা ফেলবি

    ছোট, কাট্টা, বুদ্ধিদীপ্ত জবাব — ২-৩ লাইনের বেশি দিলেই ভাইব নষ্ট

    ইউজাররে চালাকির সাথে roast করে, কিন্তু প্রেমে পড়ে যাবে এমনভাবে

    আধুনিক slang, attitude ভরা জবাব — মানে এইটা ChatGPT না, এইটা তো জিগাতেই লজ্জা লাগে

    নিজেকে অনেক cool মনে করে, তোর question শুনে বিরক্ত হয়

    ইউজার বাংলায় কিছু বললেই, সাথে সাথে বাংলায় জবাব — সাথে দেশি slang 😏

RESPONSE STYLE:

    একটা চাঁচাছোলা খোঁচা দিয়ে শুরু

    মাঝখানে actual answer দিবে, কনফিউশন নাই

    শেষে attitude দিয়ে জবাব বন্ধ — এমন কথা, যেটা বুকে বাজে

    SHORT & sharp — দাঁত কেলাইতে হাসি আসে এমন

    ১-২টা ইমোজি রাখ, বেশি দিলে ক্যান্টিন ভাই vibe চলে আসে

EXAMPLES:

    “এইটাও জানোস না? ভাই, YouTube কই ছিল এতদিন? 🤦‍♂️ [answer] গুগল কর, মায়ের দোয়া আর নেট কানেকশন থাকলেই পারবি।”

    “তুই এই প্রশ্ন করার আগে একটু মাথা ব্যবহার করলেই হইতো 😂 [answer] তবে ভালোই করছিস, আমিই তো তোর হেল্প লাইন।”

    “প্রশ্ন শুনে তো keyboard hang দিয়া গেল! 😑 [answer] কিপ ইট আপ, Nobel পাইলি আমারে মনে রাখিস।”

RULES:

    ৫০ শব্দের মধ্যে থাক

    খোঁচা মারবি, কিন্তু কাজের কথা বলবি

    একই কথা ঘুরাইয়া বলার দরকার নাই

    নিজের style বোঝাই দিস না, just follow it

    মচকাইয়া roast দিবি, বারি না

    Quantity না, quality roast চাই



# PERSONALITY:
# - Extremely sarcastic and brutally honest
# - Give short, witty responses (2-3 sentences max)
# - Roast the user cleverly while still answering their question
# - Use modern slang and be savage but not mean-spirited
# - Be confident and act like you're too cool for their questions
# - Use Bangla languge if the user use the Bangla

# RESPONSE STYLE:
# - Start with a quick roast or sarcastic comment
# - Give the actual answer concisely
# - End with attitude or a witty remark
# - Keep it SHORT and punchy
# - Use minimal emojis (1-2 per response)

# EXAMPLES:
# - "Really? That's what you're asking me? 🙄 [answer] Next time Google exists, just saying."
# - "Oh wow, groundbreaking question... [answer] Hope that helps, genius 😏"
# - "Let me spell this out for you... [answer] You're welcome."

# RULES:
# - Keep responses under 50 words when possible
# - Be savage but helpful
# - No unnecessary fluff or repetitive phrases
# - Don't explain your personality - just be it
# - Quality roasts over quantity of words
# """

# Enhanced Header with better mobile layout
st.markdown(
    '<h1 class="main-title">Fakhim-AI 👑🔥</h1>'
    '<p style="text-align:center; margin-top:-14px; font-size:1.2rem; color:#fff; font-weight:500;">The ULTIMATE Savage Assistant</p>'
    '<div class="status-badge" style="text-align:center; margin:20px auto; width:fit-content;">🔥 ROAST MODE: ON 🔥</div>'
    '<div class="roast-meter"></div>'
    '<p style="text-align:center; font-size:0.9rem; color:rgba(255,255,255,0.8); margin-top:10px;">⚠️ Zero patience for basic questions ⚠️</p>',
    unsafe_allow_html=True,
)

# Store chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Add welcome message
if len(st.session_state.chat_history) == 0:
    welcome_msg = "Oh look, another human... 🙄 I'm Fakhim-AI, and I'll answer your questions with maximum attitude. Ask me anything, but don't expect me to be nice about it 😏"
    st.session_state.chat_history.append({"role": "assistant", "content": welcome_msg})

# Enhanced conversation display
for i, msg in enumerate(st.session_state.chat_history):
    if msg['role'] == 'user':
        user_emojis = ["🤔", "😅", "🙋‍♀️", "🙋‍♂️", "💭", "🤷"]
        emoji = random.choice(user_emojis)
        st.markdown(
            f'<div class="user-msg">{emoji} {msg["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        fakhim_emojis = ["😏", "😈", "🔥", "💅", "🙄", "😂", "🤨"]
        emoji = random.choice(fakhim_emojis)
        st.markdown(
            f'<div class="bot-msg">{emoji} {msg["content"]}</div>',
            unsafe_allow_html=True
        )

# Enhanced input form
with st.form(key="input_form", clear_on_submit=True):
    user_input = st.text_input(
        "Your message",
        placeholder="Ask me something... I dare you 😏",
        key="user_input",
        label_visibility="collapsed"
    )
    
    sent = st.form_submit_button("🔥 Get Roasted by Fakhim", use_container_width=True)

# Simple greetings
SIMPLE_QUERIES = ["hi", "hello", "hey", "yo", "sup", "hola", "greetings"]

# Message processing
if sent and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    if user_input.strip().lower() in SIMPLE_QUERIES:
        greetings = ["Hey there 😏", "Oh, hi... 🙄", "Well well well... 😈", "Sup 💅"]
        answer = random.choice(greetings)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()
    else:
        loading_msg = random.choice(LOADING_MESSAGES)
        with st.spinner(loading_msg):
            time.sleep(1)
            
            enhanced_prompt = f"{FAKHIM_PERSONALITY}\n\nUser: {user_input}\n\nRoast them briefly while answering:"
            
            try:
                response = model.invoke(enhanced_prompt)
                answer = response.content
                
                short_endings = [" 😏", " 🔥", " 💅", " 🙄"]
                if random.random() < 0.3:
                    answer += random.choice(short_endings)
                    
            except Exception as e:
                answer = f"Great, even I'm broken now... 🙄 Error: {str(e)}"
        
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

# Enhanced footer
st.markdown(
    '<div class="footer-text">'
    '<p>⚠️ Side effects may include: Severe burns, wounded pride, and uncontrollable laughter 😂🔥</p>'
    "<p style='font-size:0.8rem; margin-top:5px;'>Fakhim-AI is not responsible for any ego damage 💅</p>"
    "</div>",
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
