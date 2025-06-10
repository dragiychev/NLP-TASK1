import streamlit as st
from eli5_agent import get_eli5_explanation, GOOGLE_API_KEY # Import core simplification logic and API key for initial check

# --- Page Configuration ---
# Set the title that appears in the browser tab and the favicon.
# Layout "wide" uses the full width of the page.
st.set_page_config(page_title="ELI5 Text Simplifier", page_icon="🧸", layout="wide")

# --- Main UI Elements ---

# Display the main title of the application.
st.title("Explain Like I'm 5 (ELI5) Text Simplifier 🧸")

# Provide a brief welcome message and instructions to the user.
st.markdown("""
Welcome! Paste any complex or technical text into the box below, 
and I'll try to explain it in super simple terms, just like you're 5 years old!
""")

# --- API Key Check ---
# Verify if the GOOGLE_API_KEY was loaded successfully from eli5_agent (which loads it from .env).
# This is a crucial step for the application to function.
if not GOOGLE_API_KEY:
    st.error("🔴 Configuration Error: GOOGLE_API_KEY not found. "
             "Please ensure you have a .env file in the project directory (eli5_text_simplifier) with your API key. "
             "The application will not be able to simplify text without it.")
    st.stop() # Halt execution of the Streamlit app if the API key is missing.

# --- User Input Area ---
st.subheader("Enter the text you want to simplify:")
# Create a text area widget for the user to input their complex text.
# `height` controls the visible size of the text area.
# `placeholder` provides an example text to guide the user.
complex_text_input = st.text_area(
    "Complex Text", 
    height=200, 
    placeholder="e.g., Quantum entanglement is a physical phenomenon that occurs when a pair or group of particles is generated..."
)

# --- State Management for Output ---
# Initialize session state variables to store the explanation and input text.
# This helps persist the output even if other parts of the UI cause a rerun.
if 'explanation' not in st.session_state:
    st.session_state.explanation = ""
if 'input_text' not in st.session_state: # To optionally redisplay or log input
    st.session_state.input_text = ""

# --- Simplification Button and Logic ---
# Create a button labeled "✨ Simplify Text".
# The code block within this `if` statement executes when the button is clicked.
if st.button("✨ Simplify Text"):
    # Check if the input text area is not empty or just whitespace.
    if complex_text_input and complex_text_input.strip():
        st.session_state.input_text = complex_text_input # Store the current input
        # Show a spinner animation while the simplification is in progress.
        with st.spinner("🧠 Thinking like a 5-year-old..."):
            # Call the core simplification function from eli5_agent.py.
            simplified_explanation = get_eli5_explanation(complex_text_input)
            # Store the result in session state.
            st.session_state.explanation = simplified_explanation
    # Handle cases where the input is empty or only whitespace.
    elif not complex_text_input or not complex_text_input.strip():
        st.session_state.explanation = "🤔 Please enter some text for me to simplify!"
        st.session_state.input_text = ""
    else:
        # Clear previous explanation if input is cleared after being filled (edge case)
        st.session_state.explanation = ""
        st.session_state.input_text = ""

# --- Displaying the Result ---
# If an explanation exists in the session state, display it.
if st.session_state.explanation:
    st.subheader("Simplified Explanation (ELI5):")
    # Use st.markdown to display the text, formatting it as a blockquote for better visual separation.
    # Replace newlines in the explanation with markdown blockquote newlines.
    st.markdown(f"> {st.session_state.explanation.replace('\n', '\n> ')}")

# --- Footer ---
# A simple footer acknowledging the technologies used.
st.markdown("---_Powered by LangChain & Gemini_---")

# --- Running Instructions (as comments) ---
# These comments guide the user on how to set up and run the Streamlit application.
# 1. Make sure you have all libraries installed: pip install streamlit langchain langchain_google_genai python-dotenv
# 2. Ensure your .env file with GOOGLE_API_KEY is in the `eli5_text_simplifier` directory.
# 3. Open your terminal in the `eli5_text_simplifier` directory.
# 4. Run: streamlit run app.py 