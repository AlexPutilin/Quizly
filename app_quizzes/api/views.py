from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from models import Quiz
from permissions import IsQuizOwner
from serializers import QuizSerializer, QuizCreateSerializer
from services.quiz_generation_service import create_quiz_from_url


class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.prefetch_related("questions")
    permission_classes = [IsAuthenticated, IsQuizOwner]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(user=self.request.user)
        return self.queryset
    
    def get_serializer_class(self):
        if self.action == "create":
            return QuizCreateSerializer
        return QuizSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = create_quiz_from_url(user=request.user, video_url=serializer.validated_data["url"])
        response_data = QuizSerializer(quiz).data
        return Response(response_data, status=status.HTTP_201_CREATED)