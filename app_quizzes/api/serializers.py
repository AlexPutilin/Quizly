from urllib.parse import urlparse, parse_qs
from rest_framework import serializers
from models import Question, Quiz


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for individual quiz questions."""

    class Meta:
        model = Question
        fields = [
            'id',
            'question_title',
            'question_options',
            'answer',
            'created_at',
            'updated_at'
        ]
        read_only_fields = fields


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for quiz output and partial updates."""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'updated_at',
            'video_url',
            'questions',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'video_url',
            'questions',
        ]


class QuizCreateSerializer(serializers.Serializer):
    """Serializer for creating quizzes via YouTube URL."""
    
    url = serializers.URLField()

    def validate_url(self, value):
        parsed_url = urlparse(value)
        if not self.has_valid_youtube_video_id(parsed_url):
            raise serializers.ValidationError("Please enter a valid YouTube-URL")
        return value
    
    def has_valid_youtube_video_id(self, parsed_url):
        hostname = parsed_url.hostname or ''
        if hostname == 'youtu.be':
            return bool(parsed_url.path.strip('/'))
        if hostname == 'youtube.com' or hostname.endswith('.youtube.com'):
            query_params = parse_qs(parsed_url.query)
            return bool(query_params.get('v', [''])[0])
        return False
