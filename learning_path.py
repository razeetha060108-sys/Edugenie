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


def get_learning_recommendations(
    topic: str
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
You are EduGenie, an AI learning
path assistant.

Create a personalized learning path
for this topic:

{topic}

Organize it from beginner to
advanced level.

Include:

1. Beginner concepts
2. Intermediate concepts
3. Advanced concepts
4. Suggested timeline
5. Useful resources such as:
   - Videos
   - Articles
   - Books
   - Documentation
6. Step-by-step guidance
7. Practice suggestions

Make the learning path clear and
easy for a student to follow.
"""

        response = model.generate_content(
            prompt
        )

        if response.text:

            return response.text.strip()

        return (
            "Sorry, learning path could "
            "not be generated."
        )

    except Exception as error:

        return (
            "Learning path error: "
            f"{error}"
        )