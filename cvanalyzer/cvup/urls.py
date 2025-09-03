# urls.py (cvup/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_cv, name='upload_cv'),
    path('questions/<int:cv_id>/', views.view_questions, name='view_questions'),
    path('chat/<int:cv_id>/', views.chat_interface, name='chat_interface'),
    
    path("api/send-message-stream/<int:cv_id>/", views.send_message_stream, name="send_message_stream"),
    path("api/send-message/<int:cv_id>/", views.send_message, name="send_message"),
    
    path("api/send-message-polling/<int:cv_id>/", views.send_message_polling, name="send_message_polling"),
    path("api/message-status/<int:cv_id>/<int:message_id>/", views.get_message_status, name="get_message_status"),
]