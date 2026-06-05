from django.contrib import admin
from .models import Quiz, Question


class QuizAdmin(admin.ModelAdmin):
    """Admin config for quizzes"""

    list_display = ('id', 'title', 'user', 'created_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user', 'title', 'description', 'video_url')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


class QuestionAdmin(admin.ModelAdmin):
    """Admin config for questions"""

    list_display = ('id', 'quiz', 'question_title', 'answer')
    list_filter = ('quiz',)
    search_fields = ('question_title', 'answer')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('quiz', 'id')


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)