import json
from django.conf import settings
from google import genai


def generate_quiz_from_transcript(transcript):
    """Generates quiz data from a transcript with Gemini."""

    prompt = build_quiz_prompt(transcript)
    response_text = request_gemini_response(prompt)
    cleaned_text = clean_json_reponse(response_text)
    return json.loads(cleaned_text)


def request_gemini_response(prompt):
    """sends the builded prompt to gemini"""

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model=settings.GEMINI_MODEL, 
        contents=prompt
    )
    return response.text


def build_quiz_prompt(transcript):
    """Builds the prompt for quiz generation."""

    return f"""
    Based on the following transcript, generate a quiz in valid JSON format.
    The quiz must follow this exact structure:
    {{
    "title": "Create a concise quiz title based on the topic of the transcript.",
    "description": "Summarize the transcript in no more than 150 characters. Do not include any quiz questions or answers.",
    "questions": [
        {{
        "question_title": "The question goes here.",
        "question_options": ["Option A", "Option B", "Option C", "Option D"],
        "answer": "The correct answer from the above options"
        }}
    ]
    }}

    Requirements:
    - Each question must have exactly 4 distinct answer options.
    - Exactly 10 questions.
    - Only one correct answer is allowed per question, and it must be present in 'question_options'.
    - The output must be valid JSON and parsable as-is (e.g., using Python's json.loads).
    - Do not include explanations, comments, or any text outside the JSON.

    Transkript:
    {transcript}
    """


def clean_json_reponse(response_text):
    """Removes markdown fences from JSON text."""

    cleaned_text = response_text.strip()
    cleaned_text = cleaned_text.replace("```json", "")
    cleaned_text = cleaned_text.replace("```", "")
    return cleaned_text.strip()