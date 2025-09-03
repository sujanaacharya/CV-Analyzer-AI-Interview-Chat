
# admin.py
from django.contrib import admin
from .models import CVUpload, InterviewQuestions, ChatSession, ChatMessage

@admin.register(CVUpload)
class CVUploadAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'uploaded_at']
    list_filter = ['uploaded_at']

@admin.register(InterviewQuestions)
class InterviewQuestionsAdmin(admin.ModelAdmin):
    list_display = ['cv_upload', 'difficulty', 'category', 'question']
    list_filter = ['difficulty', 'category']
    search_fields = ['question', 'answer']

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['cv_upload', 'user', 'created_at']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['chat_session', 'created_at']