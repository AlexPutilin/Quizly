from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsQuizOwner
from .serializers import QuizSerializer, QuizCreateSerializer
from app_quizzes.models import Quiz
from app_quizzes.services.quiz_generation_service import generate_quiz_from_url


class QuizViewSet(viewsets.ModelViewSet):
    """API for quiz creation, display, modification, and deletion."""

    permission_classes = [IsAuthenticated, IsQuizOwner]

    def get_queryset(self):
        """Return quizzes with related user and questions."""

        queryset = Quiz.objects.select_related('user')
        queryset = queryset.prefetch_related('questions')
        if self.action == "list":
            return queryset.filter(user=self.request.user)
        return queryset
    
    def get_serializer_class(self):
        """Return the serializer for the current action."""

        if self.action == "create":
            return QuizCreateSerializer
        return QuizSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a quiz from a YouTube URL."""

        serializer = QuizCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = generate_quiz_from_url(user=request.user, video_url=serializer.validated_data["url"])
        response_data = QuizSerializer(quiz).data
        return Response(response_data, status=status.HTTP_201_CREATED)