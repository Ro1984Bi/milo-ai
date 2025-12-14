import os
from mistralai import Mistral
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("MISTRAL_API_KEY")

# Both are FREE models 💸🔥
PRIMARY_MODEL = "open-mistral-nemo"
FALLBACK_MODEL = "open-mistral-7b"

client = Mistral(api_key=api_key)


def ask_mistral(prompt: str):
    """
    Calls Mistral API with fallback and SDK-compatible message parsing.
    Always uses 100% free models.
    """

    # ------------ PRIMARY MODEL ------------
    try:
        print(f"➡️ Using primary model: {PRIMARY_MODEL}")

        chat_response = client.chat.complete(
            model=PRIMARY_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        print("❌ Primary model failed:", type(e).__name__, str(e))
        print("➡️ Switching to fallback:", FALLBACK_MODEL)

    # ------------ FALLBACK MODEL ------------
    try:
        chat_response = client.chat.complete(
            model=FALLBACK_MODEL,
            messages=[{"role": "user", "content": prompt}],
        )

        return chat_response.choices[0].message.content

    except Exception as e2:
        print("❌ Fallback model also failed:", type(e2).__name__, str(e2))
        return f"Mistral error: {type(e2).__name__} - {str(e2)}"
