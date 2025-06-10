import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

# --- Environment Setup ---
# Load environment variables from .env file, specifically for GOOGLE_API_KEY.
load_dotenv()

# Retrieve the Gemini API key from environment variables.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Ensure the API key is available, otherwise raise an error.
if not GOOGLE_API_KEY:
    raise ValueError("🔴 Error: GOOGLE_API_KEY not found. Please ensure it's in your .env file or environment variables.")

# --- LangChain Core Components ---

# 1. Initialize the Language Model (LLM)
# We use ChatGoogleGenerativeAI with the 'gemini-2.0-flash' model.
# The API key is passed directly. Temperature is set to 0.7 for a balance of creativity and factual grounding.
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY, temperature=0.7)

# 2. Define the Prompt Template for ELI5
# This template instructs the LLM to explain a given text in simple terms, suitable for a 5-year-old.
# It emphasizes using short sentences, easy words, and avoiding jargon, focusing on the main idea.
eli5_prompt_template_text = """
Explain the following text like I'm 5 years old. Make it very simple, use short sentences, and easy words. 
Do not use any complex words or jargon. Focus on the main idea.

Text to explain: 
{user_text}

Simplified Explanation for a 5-year-old:
"""

# Create a PromptTemplate object from the defined string.
# 'user_text' is the variable that will be filled with the complex text provided by the user.
eli5_prompt_template = PromptTemplate(
    input_variables=["user_text"],
    template=eli5_prompt_template_text
)

# 3. Create an LLMChain
# This chain combines the LLM and the prompt template.
# When invoked, it will format the prompt with user input and pass it to the LLM.
# Note: LLMChain is deprecated in LangChain 0.1.17. For future development, consider using LCEL (LangChain Expression Language),
# for example: `chain = eli5_prompt_template | llm | StrOutputParser()`
eli5_chain = LLMChain(llm=llm, prompt=eli5_prompt_template)

# --- Main Functionality ---

# 4. Function to get the simplified explanation
def get_eli5_explanation(complex_text: str) -> str:
    """
    Takes complex text as input, processes it through the ELI5 LangChain, 
    and returns a simplified explanation suitable for a 5-year-old.

    Args:
        complex_text: The string containing the complex text to be simplified.

    Returns:
        A string containing the simplified explanation, or an error/message if input is invalid or an issue occurs.
    """
    # Handle empty or whitespace-only input to avoid unnecessary API calls.
    if not complex_text or not complex_text.strip():
        return "Please provide some text to simplify!"
    
    try:
        # Invoke the chain with the user's complex text.
        # The input is a dictionary where the key matches the input_variable in the prompt template.
        response = eli5_chain.invoke({"user_text": complex_text})
        
        # Extract the actual text from the response.
        # LLMChain typically returns a dictionary with a 'text' key containing the LLM's output.
        if isinstance(response, dict) and 'text' in response:
            return response['text'].strip()
        # Fallback for other possible response structures (e.g., AIMessage directly, though less common with LLMChain).
        elif hasattr(response, 'content'): 
             return response.content.strip()
        else:
            # Log and return an error if the response structure is not as expected.
            print(f"Unexpected response structure: {response}")
            return "Sorry, I couldn't simplify the text properly. The response structure was unexpected."

    except Exception as e:
        # Catch any exceptions during the API call or processing and return a user-friendly error message.
        print(f"🔴 Error during simplification: {e}")
        return f"Sorry, an error occurred while trying to simplify the text: {str(e)}"

# --- Testing Block ---

# 5. Test this core logic (Example usage)
# This block executes only when the script is run directly (not imported as a module).
if __name__ == "__main__":
    print("Testing ELI5 Agent Core Logic...")
    
    # Define a list of example complex texts for testing.
    example_texts = [
        "The Heisenberg Uncertainty Principle states that there is a fundamental limit to the precision with which certain pairs of physical properties of a particle, known as complementary variables, such as position x and momentum p, can be known.",
        "Photosynthesis is a process used by plants, algae, and certain bacteria to harness energy from sunlight and turn it into chemical energy.",
        "Blockchain is a distributed ledger technology that underlies cryptocurrencies like Bitcoin. It consists of a growing list of records, called blocks, that are securely linked together using cryptography. Each block typically contains a cryptographic hash of the previous block, a timestamp, and transaction data.",
        "The Federal Reserve System, often referred to as the Fed, is the central banking system of the United States. It was created in 1913 with the enactment of the Federal Reserve Act, largely in response to a series of financial panics, particularly the Panic of 1907."
    ]

    # Loop through the example texts, get their ELI5 explanations, and print them.
    for i, text in enumerate(example_texts):
        print(f"\n--- Example {i+1} ---")
        print(f"Original Text: {text}")
        simplified_text = get_eli5_explanation(text)
        print(f"ELI5 Explanation: {simplified_text}")

    # Test with empty input to ensure a graceful response.
    print("\n--- Test with empty input ---")
    print(f"ELI5 Explanation: {get_eli5_explanation('')}")

    # Test with whitespace input.
    print("\n--- Test with whitespace input ---")
    print(f"ELI5 Explanation: {get_eli5_explanation('   ')}") 