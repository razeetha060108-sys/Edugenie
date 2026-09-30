import json
import os
import re

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


def clean_json_block(text: str) -> str:

    text = text.strip()

    text = re.sub(
        r"^```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"^```\s*",
        "",
        text
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def generate_quiz(
    passage: str
):

    if not API_KEY:

        return {
            "error":
                "Gemini API key is not configured."
        }

    try:

        model = genai.GenerativeModel(
            MODEL_NAME
        )

        prompt = f"""
You are EduGenie, an educational
quiz generator.

Create exactly THREE multiple-choice
questions from the passage below.

PASSAGE:
{passage}

Rules:

1. Create exactly 3 questions.
2. Each question must have exactly
   4 options.
3. There must be exactly one correct
   answer.
4. Options should be plausible.
5. Include the correct answer.
6. Include a short explanation.
7. Return ONLY valid JSON.
8. Do not use Markdown code fences.

Return exactly this structure:

[
  {{
    "question": "Question here",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "correct_answer": "Option A",
    "explanation": "Explanation here"
  }}
]
"""

        response = model.generate_content(
            prompt
        )

        if not response.text:

            return {
                "error":
                    "Gemini returned an empty response."
            }

        cleaned = clean_json_block(
            response.text
        )

        questions = json.loads(
            cleaned
        )

        if not isinstance(
            questions,
            list
        ):

            return {
                "error":
                    "Invalid quiz format."
            }

        if len(questions) != 3:

            return {
                "error":
                    "Quiz must contain exactly 3 questions."
            }

        for question in questions:

            if len(
                question.get(
                    "options",
                    []
                )
            ) != 4:

                return {
                    "error":
                        "Each question must contain exactly 4 options."
                }

        return questions

    except json.JSONDecodeError:

        return {
            "error":
                "Could not parse Gemini quiz response as JSON."
        }

    except Exception as error:

        return {
            "error":
                f"Quiz generation error: {error}"
        }