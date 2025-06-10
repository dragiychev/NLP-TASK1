import os
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("🔴 Error: GOOGLE_API_KEY not found in .env file or environment variables.")
    print("Please create a .env file in the project root (eli5_text_simplifier) with your GOOGLE_API_KEY.")
    print("Example .env file content:")
    print("GOOGLE_API_KEY=\"YOUR_API_KEY\"")
else:
    print(f"🔑 API Key loaded: {api_key[:5]}...{api_key[-5:]}") # Print a portion of the key for verification
    try:
        # Initialize the ChatGoogleGenerativeAI model - changed to gemini-1.5-flash-latest
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

        # Send a simple test prompt
        response = llm.invoke("Hello! Can you tell me a fun fact?")

        if response and response.content:
            print("🟢 Gemini API Test Successful!")
            print("   Response from Gemini:")
            print(f"   '{response.content}'")
        else:
            print("🟡 Gemini API Test Potentially Successful, but response was empty or malformed.")
            print(f"   Raw response: {response}")

    except Exception as e:
        print(f"🔴 Error connecting to Gemini API: {e}")
        print("   Please ensure your API key is correct and has the necessary permissions for the 'gemini-1.5-flash-latest' model.")
        print("   You might also want to check your internet connection.")

print("\nScript execution finished.") 