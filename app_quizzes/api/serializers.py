from urllib.parse import urlparse, parse_qs
from rest_framework import serializers
from models import Question, Quiz


class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.SerializerMethodField()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options', 'answer', 'created_at', 'updated_at']

    def get_question_options(self, obj):
        return [obj.option_a, obj.option_b, obj.option_c, obj.option_d]
    
    def get_answer(self, obj):
        options = {
            'A': obj.option_a,
            'B': obj.option_b,
            'C': obj.option_c,
            'D': obj.option_d,
        }
        return options.get(obj.answer)


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'video_url', 'questions',]
        read_only_fields = ['id', 'created_at', 'updated_at', 'video_url', 'questions',]


class QuizCreateSerializer(serializers.Serializer):
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
