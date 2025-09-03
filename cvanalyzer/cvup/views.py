# # views.py
# from django.shortcuts import render, redirect, get_object_or_404
# from django.http import JsonResponse, StreamingHttpResponse
# from django.contrib import messages
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# from .models import CVUpload, InterviewQuestions, ChatSession, ChatMessage
# from .utils import CVProcessor
# import json

# def upload_cv(request):
#     if request.method == 'POST':
#         if 'cv_file' not in request.FILES:
#             messages.error(request, 'Please select a CV file.')
#             return render(request, 'cvup/upload.html')
        
#         cv_file = request.FILES['cv_file']
        
#         # Validate file type
#         allowed_extensions = ['pdf', 'docx', 'doc', 'txt']
#         file_extension = cv_file.name.lower().split('.')[-1]
        
#         if file_extension not in allowed_extensions:
#             messages.error(request, 'Please upload a PDF, DOCX, DOC, or TXT file.')
#             return render(request, 'cvup/upload.html')
        
#         # Create CV upload instance
#         cv_upload = CVUpload.objects.create(
#             user=request.user if request.user.is_authenticated else None,
#             cv_file=cv_file
#         )
        
#         # Process CV
#         processor = CVProcessor()
#         cv_text = processor.extract_text_from_cv(cv_file)
#         cv_upload.cv_text = cv_text
#         cv_upload.save()
        
#         # Generate questions
#         questions_data = processor.generate_interview_questions(cv_text)
        
#         # Save questions to database
#         for difficulty, questions_list in questions_data.items():
#             for q_data in questions_list:
#                 InterviewQuestions.objects.create(
#                     cv_upload=cv_upload,
#                     question=q_data['question'],
#                     answer=q_data['answer'],
#                     difficulty=difficulty,
#                     category=q_data['category']
#                 )
        
#         messages.success(request, 'CV uploaded and questions generated successfully!')
#         return redirect('view_questions', cv_id=cv_upload.id)
    
#     return render(request, 'cvup/upload.html')

# def view_questions(request, cv_id):
#     cv_upload = get_object_or_404(CVUpload, id=cv_id)
#     questions = InterviewQuestions.objects.filter(cv_upload=cv_upload).order_by('difficulty', 'category')
    
#     # Group questions by difficulty
#     questions_by_difficulty = {}
#     for question in questions:
#         if question.difficulty not in questions_by_difficulty:
#             questions_by_difficulty[question.difficulty] = []
#         questions_by_difficulty[question.difficulty].append(question)
    
#     context = {
#         'cv_upload': cv_upload,
#         'questions_by_difficulty': questions_by_difficulty,
#     }
#     return render(request, 'cvup/questions.html', context)

# def chat_interface(request, cv_id):
#     cv_upload = get_object_or_404(CVUpload, id=cv_id)
    
#     # Get or create chat session
#     chat_session, created = ChatSession.objects.get_or_create(
#         cv_upload=cv_upload,
#         user=request.user if request.user.is_authenticated else None
#     )
    
#     # Get chat history
#     chat_messages = ChatMessage.objects.filter(chat_session=chat_session).order_by('created_at')
    
#     context = {
#         'cv_upload': cv_upload,
#         'chat_session': chat_session,
#         'chat_messages': chat_messages,
#     }
#     return render(request, 'cvup/chat.html', context)

# # @csrf_exempt
# # @require_http_methods(["POST"])
# # def send_message_stream(request, cv_id):
# #     """Handle streaming chat messages"""
# #     cv_upload = get_object_or_404(CVUpload, id=cv_id)
    
# #     try:
# #         data = json.loads(request.body)
# #         user_message = data.get('message', '').strip()
        
# #         if not user_message:
# #             return JsonResponse({'error': 'Message cannot be empty'})
        
# #         # Get or create chat session
# #         chat_session, created = ChatSession.objects.get_or_create(
# #             cv_upload=cv_upload,
# #             user=request.user if request.user.is_authenticated else None
# #         )
        
# #         # Get questions context
# #         questions = InterviewQuestions.objects.filter(cv_upload=cv_upload)
# #         questions_context = "\n".join([f"Q: {q.question}\nA: {q.answer}" for q in questions[:10]])
        
# #         # Generate streaming response
# #         processor = CVProcessor()
        
# #         def generate_response():
# #             try:
# #                 full_response = ""
# #                 response_stream = processor.get_chat_response_stream(
# #                     cv_upload.cv_text,
# #                     questions_context,
# #                     user_message
# #                 )
                
# #                 if response_stream:
# #                     for chunk in response_stream:
# #                         if hasattr(chunk, 'text') and chunk.text:
# #                             chunk_text = chunk.text
# #                             full_response += chunk_text
# #                             yield f"data: {json.dumps({'chunk': chunk_text})}\n\n"
                    
# #                     # Save complete message to database
# #                     ChatMessage.objects.create(
# #                         chat_session=chat_session,
# #                         message=user_message,
# #                         response=full_response
# #                     )
                    
# #                     yield f"data: {json.dumps({'done': True, 'message_id': 'completed'})}\n\n"
# #                 else:
# #                     # Fallback to non-streaming
# #                     fallback_response = processor.get_chat_response(
# #                         cv_upload.cv_text,
# #                         questions_context,
# #                         user_message
# #                     )
                    
# #                     chat_message = ChatMessage.objects.create(
# #                         chat_session=chat_session,
# #                         message=user_message,
# #                         response=fallback_response
# #                     )
                    
# #                     yield f"data: {json.dumps({'chunk': fallback_response, 'done': True, 'message_id': chat_message.id})}\n\n"
                    
# #             except Exception as e:
# #                 error_msg = f"Sorry, I encountered an error: {str(e)}"
# #                 yield f"data: {json.dumps({'chunk': error_msg, 'done': True, 'error': True})}\n\n"
        
# #         response = StreamingHttpResponse(
# #             generate_response(),
# #             content_type='text/event-stream'
# #         )
# #         response['Cache-Control'] = 'no-cache'
# #         response['Connection'] = 'keep-alive'
# #         response['X-Accel-Buffering'] = 'no'
# #         return response
        
# #     except Exception as e:
# #         return JsonResponse({'error': str(e)})

# @csrf_exempt
# @require_http_methods(["GET", "POST"])
# def send_message_stream(request, cv_id):
#     """Handle streaming chat messages via GET (SSE) or POST (JSON)"""
#     cv_upload = get_object_or_404(CVUpload, id=cv_id)

#     try:
#         # --- Handle POST ---
#         if request.method == "POST":
#             try:
#                 data = json.loads(request.body)
#             except Exception:
#                 return JsonResponse({'error': 'Invalid JSON body'})

#             user_message = data.get('message', '').strip()

#         # --- Handle GET (SSE style with query params) ---
#         else:  # request.method == "GET"
#             user_message = request.GET.get('message', '').strip()

#         if not user_message:
#             return JsonResponse({'error': 'Message cannot be empty'})

#         # Get or create chat session
#         chat_session, created = ChatSession.objects.get_or_create(
#             cv_upload=cv_upload,
#             user=request.user if request.user.is_authenticated else None
#         )

#         # Get questions context
#         questions = InterviewQuestions.objects.filter(cv_upload=cv_upload)
#         questions_context = "\n".join([f"Q: {q.question}\nA: {q.answer}" for q in questions[:10]])

#         processor = CVProcessor()

#         def generate_response():
#             try:
#                 full_response = ""
#                 response_stream = processor.get_chat_response_stream(
#                     cv_upload.cv_text,
#                     questions_context,
#                     user_message
#                 )

#                 if response_stream:
#                     for chunk in response_stream:
#                         if hasattr(chunk, 'text') and chunk.text:
#                             chunk_text = chunk.text
#                             full_response += chunk_text
#                             yield f"data: {json.dumps({'chunk': chunk_text})}\n\n"

#                     # Save complete message
#                     ChatMessage.objects.create(
#                         chat_session=chat_session,
#                         message=user_message,
#                         response=full_response
#                     )

#                     yield f"data: {json.dumps({'done': True})}\n\n"

#                 else:
#                     # Fallback to non-streaming
#                     fallback_response = processor.get_chat_response(
#                         cv_upload.cv_text,
#                         questions_context,
#                         user_message
#                     )

#                     chat_message = ChatMessage.objects.create(
#                         chat_session=chat_session,
#                         message=user_message,
#                         response=fallback_response
#                     )

#                     yield f"data: {json.dumps({'chunk': fallback_response, 'done': True, 'message_id': chat_message.id})}\n\n"

#             except Exception as e:
#                 error_msg = f"Sorry, I encountered an error: {str(e)}"
#                 yield f"data: {json.dumps({'chunk': error_msg, 'done': True, 'error': True})}\n\n"

#         response = StreamingHttpResponse(
#             generate_response(),
#             content_type='text/event-stream'
#         )
#         response['Cache-Control'] = 'no-cache'
#         response['Connection'] = 'keep-alive'
#         response['X-Accel-Buffering'] = 'no'
#         return response

#     except Exception as e:
#         return JsonResponse({'error': str(e)})



# @csrf_exempt
# @require_http_methods(["POST"])
# def send_message(request, cv_id):
#     """Handle non-streaming chat messages (fallback)"""
#     cv_upload = get_object_or_404(CVUpload, id=cv_id)
    
#     try:
#         data = json.loads(request.body)
#         user_message = data.get('message', '').strip()
        
#         if not user_message:
#             return JsonResponse({'error': 'Message cannot be empty'})
        
#         # Get or create chat session
#         chat_session, created = ChatSession.objects.get_or_create(
#             cv_upload=cv_upload,
#             user=request.user if request.user.is_authenticated else None
#         )
        
#         # Get questions context
#         questions = InterviewQuestions.objects.filter(cv_upload=cv_upload)
#         questions_context = "\n".join([f"Q: {q.question}\nA: {q.answer}" for q in questions[:10]])
        
#         # Generate response
#         processor = CVProcessor()
#         ai_response = processor.get_chat_response(
#             cv_upload.cv_text,
#             questions_context,
#             user_message
#         )
        
#         # Save message
#         chat_message = ChatMessage.objects.create(
#             chat_session=chat_session,
#             message=user_message,
#             response=ai_response
#         )
        
#         return JsonResponse({
#             'response': ai_response,
#             'message_id': chat_message.id
#         })
        
#     except Exception as e:
#         return JsonResponse({'error': str(e)})

# def home(request):
#     recent_uploads = CVUpload.objects.all().order_by('-uploaded_at')[:5]
#     context = {'recent_uploads': recent_uploads}
#     return render(request, 'cvup/home.html', context)


# views.py - Fixed version that works with Django development server

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, StreamingHttpResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import CVUpload, InterviewQuestions, ChatSession, ChatMessage
from .utils import CVProcessor
import json
import logging
import time
import threading

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST"])
def send_message_stream(request, cv_id):
    """Handle streaming chat messages - Fixed for development server"""
    cv_upload = get_object_or_404(CVUpload, id=cv_id)
    
    try:
        # Parse request data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create chat session
        chat_session, created = ChatSession.objects.get_or_create(
            cv_upload=cv_upload,
            user=request.user if request.user.is_authenticated else None
        )
        
        # Get questions context
        questions = InterviewQuestions.objects.filter(cv_upload=cv_upload)
        questions_context = "\n".join([f"Q: {q.question}\nA: {q.answer}" for q in questions[:10]])
        
        # Initialize processor
        processor = CVProcessor()
        
        def generate_response():
            try:
                logger.info(f"Starting streaming response for message: {user_message[:50]}...")
                
                full_response = ""
                
                try:
                    # Try to get streaming response
                    response_stream = processor.get_chat_response_stream(
                        cv_upload.cv_text,
                        questions_context,
                        user_message
                    )
                    
                    if response_stream:
                        # Handle streaming response
                        for chunk in response_stream:
                            try:
                                if hasattr(chunk, 'text') and chunk.text:
                                    chunk_text = chunk.text
                                    full_response += chunk_text
                                    
                                    # Send chunk with proper formatting
                                    yield f"data: {json.dumps({'chunk': chunk_text})}\n\n"
                                    
                                    # Small delay to prevent overwhelming the client
                                    time.sleep(0.01)
                                    
                            except Exception as chunk_error:
                                logger.error(f"Error processing chunk: {chunk_error}")
                                continue
                        
                        # Send completion signal
                        yield f"data: {json.dumps({'done': True})}\n\n"
                        
                    else:
                        # Fallback to non-streaming
                        raise Exception("No streaming available")
                        
                except Exception as stream_error:
                    logger.info(f"Streaming failed, using fallback: {stream_error}")
                    
                    # Use non-streaming fallback
                    fallback_response = processor.get_chat_response(
                        cv_upload.cv_text,
                        questions_context,
                        user_message
                    )
                    
                    if fallback_response:
                        full_response = fallback_response
                        # Send complete response as chunks for consistency
                        words = fallback_response.split()
                        chunk_size = 5  # Send 5 words at a time
                        
                        for i in range(0, len(words), chunk_size):
                            chunk = ' '.join(words[i:i+chunk_size])
                            if i + chunk_size < len(words):
                                chunk += ' '
                            yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                            time.sleep(0.1)  # Simulate streaming
                        
                        yield f"data: {json.dumps({'done': True})}\n\n"
                    else:
                        raise Exception("No response generated")
                
                # Save complete message to database
                try:
                    ChatMessage.objects.create(
                        chat_session=chat_session,
                        message=user_message,
                        response=full_response
                    )
                    logger.info("Message saved to database successfully")
                except Exception as save_error:
                    logger.error(f"Error saving message: {save_error}")
                        
            except Exception as e:
                logger.error(f"Error in generate_response: {str(e)}")
                error_msg = "Sorry, I encountered an error while processing your request."
                yield f"data: {json.dumps({'chunk': error_msg, 'done': True, 'error': True})}\n\n"
        
        # Create streaming response with minimal headers for development server
        response = StreamingHttpResponse(
            generate_response(),
            content_type='text/event-stream'
        )
        
        # Only set essential headers that work with development server
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'  # For nginx if used later
        
        # Don't set Connection header as it causes issues with development server
        # response['Connection'] = 'keep-alive'  # This line causes the error
        
        return response
        
    except Exception as e:
        logger.error(f"Error in send_message_stream: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def send_message(request, cv_id):
    """Handle non-streaming chat messages (fallback)"""
    cv_upload = get_object_or_404(CVUpload, id=cv_id)
    
    try:
        # Parse request data
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create chat session
        chat_session, created = ChatSession.objects.get_or_create(
            cv_upload=cv_upload,
            user=request.user if request.user.is_authenticated else None
        )
        
        # Get questions context
        questions = InterviewQuestions.objects.filter(cv_upload=cv_upload)
        questions_context = "\n".join([f"Q: {q.question}\nA: {q.answer}" for q in questions[:10]])
        
        # Generate response
        processor = CVProcessor()
        
        try:
            ai_response = processor.get_chat_response(
                cv_upload.cv_text,
                questions_context,
                user_message
            )
            
            if not ai_response:
                ai_response = "I'm sorry, I couldn't generate a response. Please try again."
            
        except Exception as ai_error:
            logger.error(f"AI response error: {ai_error}")
            ai_response = "I'm experiencing technical difficulties. Please try again later."
        
        # Save message
        try:
            chat_message = ChatMessage.objects.create(
                chat_session=chat_session,
                message=user_message,
                response=ai_response
            )
            
            return JsonResponse({
                'response': ai_response,
                'message_id': chat_message.id,
                'status': 'success'
            })
            
        except Exception as save_error:
            logger.error(f"Error saving message: {save_error}")
            return JsonResponse({
                'response': ai_response,
                'message_id': None,
                'warning': 'Response generated but not saved to database'
            })
            
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


# Alternative: Simple polling-based chat (if streaming continues to be problematic)
@csrf_exempt
@require_http_methods(["POST"])
def send_message_polling(request, cv_id):
    """Alternative polling-based approach"""
    cv_upload = get_object_or_404(CVUpload, id=cv_id)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Get or create chat session
        chat_session, created = ChatSession.objects.get_or_create(
            cv_upload=cv_upload,
            user=request.user if request.user.is_authenticated else None
        )
        
        # Create a pending message
        chat_message = ChatMessage.objects.create(
            chat_session=chat_session,
            message=user_message,
            response="",  # Will be filled later
        )
        
        # Process in background thread
        def process_message():
            try:
                questions = InterviewQuestions.objects.filter(cv_upload=cv_upload)
                questions_context = "\n".join([f"Q: {q.question}\nA: {q.answer}" for q in questions[:10]])
                
                processor = CVProcessor()
                ai_response = processor.get_chat_response(
                    cv_upload.cv_text,
                    questions_context,
                    user_message
                )
                
                # Update the message
                chat_message.response = ai_response or "Sorry, I couldn't generate a response."
                chat_message.save()
                
            except Exception as e:
                logger.error(f"Background processing error: {e}")
                chat_message.response = "Sorry, I encountered an error."
                chat_message.save()
        
        # Start background processing
        thread = threading.Thread(target=process_message)
        thread.daemon = True
        thread.start()
        
        return JsonResponse({
            'message_id': chat_message.id,
            'status': 'processing'
        })
        
    except Exception as e:
        logger.error(f"Error in send_message_polling: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)


@require_http_methods(["GET"])
def get_message_status(request, cv_id, message_id):
    """Get status of a processing message"""
    try:
        chat_message = get_object_or_404(ChatMessage, id=message_id)
        
        if chat_message.response:
            return JsonResponse({
                'status': 'completed',
                'response': chat_message.response
            })
        else:
            return JsonResponse({
                'status': 'processing'
            })
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Keep your existing views
def upload_cv(request):
    if request.method == 'POST':
        if 'cv_file' not in request.FILES:
            messages.error(request, 'Please select a CV file.')
            return render(request, 'cvup/upload.html')
        
        cv_file = request.FILES['cv_file']
        
        # Validate file type
        allowed_extensions = ['pdf', 'docx', 'doc', 'txt']
        file_extension = cv_file.name.lower().split('.')[-1]
        
        if file_extension not in allowed_extensions:
            messages.error(request, 'Please upload a PDF, DOCX, DOC, or TXT file.')
            return render(request, 'cvup/upload.html')
        
        # Create CV upload instance
        cv_upload = CVUpload.objects.create(
            user=request.user if request.user.is_authenticated else None,
            cv_file=cv_file
        )
        
        # Process CV
        processor = CVProcessor()
        cv_text = processor.extract_text_from_cv(cv_file)
        cv_upload.cv_text = cv_text
        cv_upload.save()
        
        # Generate questions
        questions_data = processor.generate_interview_questions(cv_text)
        
        # Save questions to database
        for difficulty, questions_list in questions_data.items():
            for q_data in questions_list:
                InterviewQuestions.objects.create(
                    cv_upload=cv_upload,
                    question=q_data['question'],
                    answer=q_data['answer'],
                    difficulty=difficulty,
                    category=q_data['category']
                )
        
        messages.success(request, 'CV uploaded and questions generated successfully!')
        return redirect('view_questions', cv_id=cv_upload.id)
    
    return render(request, 'cvup/upload.html')

def view_questions(request, cv_id):
    cv_upload = get_object_or_404(CVUpload, id=cv_id)
    questions = InterviewQuestions.objects.filter(cv_upload=cv_upload).order_by('difficulty', 'category')
    
    # Group questions by difficulty
    questions_by_difficulty = {}
    for question in questions:
        if question.difficulty not in questions_by_difficulty:
            questions_by_difficulty[question.difficulty] = []
        questions_by_difficulty[question.difficulty].append(question)
    
    context = {
        'cv_upload': cv_upload,
        'questions_by_difficulty': questions_by_difficulty,
    }
    return render(request, 'cvup/questions.html', context)

def chat_interface(request, cv_id):
    cv_upload = get_object_or_404(CVUpload, id=cv_id)
    
    # Get or create chat session
    chat_session, created = ChatSession.objects.get_or_create(
        cv_upload=cv_upload,
        user=request.user if request.user.is_authenticated else None
    )
    
    # Get chat history
    chat_messages = ChatMessage.objects.filter(chat_session=chat_session).order_by('created_at')
    
    context = {
        'cv_upload': cv_upload,
        'chat_session': chat_session,
        'chat_messages': chat_messages,
    }
    return render(request, 'cvup/chat.html', context)

def home(request):
    recent_uploads = CVUpload.objects.all().order_by('-uploaded_at')[:5]
    context = {'recent_uploads': recent_uploads}
    return render(request, 'cvup/home.html', context)