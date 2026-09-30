import os

import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-pro"
)


if API_KEY:
    genai.configure(
        api_key=API_KEY
    )


def summarize_text(
    text: str
) -> str:

    if not API_KEY:

        return (
            "Gemini API key is not configured. "
            "Please add GEMINI_API_KEY to the .env file."
        )

    try:

        model = genai.GenerativeModel(
            MODEL_NAME
        )

        prompt = f"""
You are EduGenie, an educational
summarization assistant.

Summarize the following educational
content.

CONTENT:
{text}

Requirements:

- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Make it useful for quick revision.
- Do not add information that is
  not present in the original content.
"""

        response = model.generate_content(
            prompt
        )

        if response.text:

            return response.text.strip()

        return (
            "Sorry, summary could not "
            "be generated."
        )

    except Exception as error:

        return (
            "Summary generation error: "
            f"{error}"
        )     