from transformers import pipeline


# Model will be loaded only when needed
_model = None


def get_explanation_model():

    global _model

    if _model is None:

        _model = pipeline(
            "text-generation",
            model="MBZUAI/LaMini-Flan-T5-783M",
            device=-1
        )

    return _model


def explain_topic(
    topic: str
) -> str:

    try:

        model = get_explanation_model()

        prompt = f"""
Explain the following topic to a beginner.

Topic:
{topic}

Give:

1. Simple definition
2. Easy explanation
3. Important points
4. One simple example

Use simple and clear language.
"""

        result = model(
            prompt,
            max_new_tokens=400,
            do_sample=False
        )

        if result:

            return result[0][
                "generated_text"
            ].strip()

        return (
            "Sorry, explanation could "
            "not be generated."
        )

    except Exception as error:

        return (
            "Error while generating "
            f"explanation: {error}"
        )