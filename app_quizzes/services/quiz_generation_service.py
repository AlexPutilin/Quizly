import tempfile
from django.db import transaction
from models import Question, Quiz
from .gemini_service import create_quiz_data
from .transcription_service import transcribe_audio
from .youtube_service import download_youtube_audio


def generate_quiz_from_url(user, video_url):
    """Creates a quiz from a YouTube URL."""

    with tempfile.TemporaryDirectory() as temp_dir:
        audio_path = download_youtube_audio(video_url, temp_dir)
        transcript = transcribe_audio(audio_path)
    quiz_data = create_quiz_data(transcript)
    validate_quiz_data(quiz_data)
    return save_quiz(user, video_url, quiz_data)


def save_quiz(user, video_url, quiz_data):
    """Saves generated quiz data to the database."""
    
    with transaction.atomic():
        quiz_object = Quiz.objects.create(
            user=user,
            title=quiz_data['title'],
            description=quiz_data['description'],
            video_url=video_url
        )
        create_questions(quiz_object, quiz_data['questions'])
    return quiz_object


def create_questions(quiz_object, questions):
    """Saves all questions from a quiz"""

    question_objects = []
    for question_data in questions:
        question_objects.append(
            Question(
                quiz=quiz_object,
                question_title=question_data['question_title'],
                question_options=question_data['question_options'],
                answer=question_data['answer']
            )
        )
    Question.objects.bulk_create(question_objects)


def validate_quiz_data(quiz_data):
    """Checks the basic structure of the gemini result."""

    if not isinstance(quiz_data, dict):
        raise ValueError('Gemini did not provide a valid JSON object.')

    if len(quiz_data.get('questions', [])) != 10:
        raise ValueError('Gemini must provide exactly 10 questions.')

    for question_data in quiz_data['questions']:
        validate_question_data(question_data)


def validate_question_data(question_data):
    """Checks a single question from a quiz"""

    options = question_data.get('question_options', [])
    answer = question_data.get('answer')

    if len(options) != 4:
        raise ValueError('Each question must have exactly 4 answer options.')

    if len(set(options)) != 4:
        raise ValueError('Answer options must be unique.')

    if answer not in options:
        raise ValueError('The correct answer must be among the options.')