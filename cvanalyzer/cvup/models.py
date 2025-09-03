
# models.py
from django.db import models
from django.contrib.auth.models import User
import json

class CVUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cv_file = models.FileField(upload_to='cvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cv_text = models.TextField(blank=True)
    
    def __str__(self):
        return f"CV uploaded at {self.uploaded_at}"

class InterviewQuestions(models.Model):
    DIFFICULTY_CHOICES = [
        ('frequent', 'Frequently Asked'),
        ('common', 'Common'),
        ('hard', 'Hard'),
        ('indepth', 'In-depth'),
    ]
    
    cv_upload = models.ForeignKey(CVUpload, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    category = models.CharField(max_length=100)  # Technical, Behavioral, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.difficulty}: {self.question[:50]}..."

class ChatSession(models.Model):
    cv_upload = models.ForeignKey(CVUpload, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat session for {self.cv_upload}"

class ChatMessage(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message at {self.created_at}"