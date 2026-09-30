import os

from google import genai
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Gemini settings
API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-pro-preview"
)


def answer_question(question: str) -> str:

    if not API_KEY:
        return (
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to the .env file."
        )

    try:

        client = genai.Client(
            api_key=API_KEY
        )

        prompt = f"""
You are EduGenie, an AI educational
assistant for students.

Answer the following question clearly
and accurately.

Question:
{question}

Instructions:

- Give a direct answer.
- Explain difficult terms simply.
- Use examples when useful.
- Keep the answer easy for students
  to understand.
"""

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        if response.text:
            return response.text.strip()

        return (
            "Sorry, I could not generate "
            "an answer."
        )

    except Exception as error:

        return (
            "Error while generating answer: "
            f"{error}"
        )