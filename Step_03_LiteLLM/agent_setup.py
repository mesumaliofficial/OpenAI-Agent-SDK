import os
from dotenv import find_dotenv, load_dotenv
from litellm import completion

load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")

def handle_gemini(message: str):
    try:
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": message}],
            api_key=gemini_api_key
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {e}"
