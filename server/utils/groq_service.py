import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is missing from environment variables.")

client = Groq(api_key=api_key)

# FREE + STABLE MODEL
GROQ_MODEL = "llama-3.1-8b-instant"


def ask_groq(prompt: str):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=GROQ_MODEL,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error calling Groq API: {e}"
