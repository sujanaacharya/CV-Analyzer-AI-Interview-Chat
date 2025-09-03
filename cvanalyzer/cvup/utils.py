
# utils.py - CV Processing and Gemini Integration
import google.generativeai as genai
from django.conf import settings
import PyPDF2
from docx import Document
import json
import re

class CVProcessor:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    
    def extract_text_from_pdf(self, pdf_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error reading PDF: {str(e)}"
    
    def extract_text_from_docx(self, docx_file):
        """Extract text from DOCX file"""
        try:
            doc = Document(docx_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            return f"Error reading DOCX: {str(e)}"
    
    def extract_text_from_cv(self, cv_file):
        """Extract text from CV file based on extension"""
        file_extension = cv_file.name.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return self.extract_text_from_pdf(cv_file)
        elif file_extension in ['docx', 'doc']:
            return self.extract_text_from_docx(cv_file)
        elif file_extension == 'txt':
            return cv_file.read().decode('utf-8')
        else:
            return "Unsupported file format"
    
    def generate_interview_questions(self, cv_text):
        """Generate interview questions based on CV content"""
        prompt = f"""
        Based on the following CV content, generate interview questions in different categories and difficulty levels.
        
        CV Content:
        {cv_text}
        
        Please generate questions in the following format as JSON:
        {{
            "frequent": [
                {{"question": "question text", "answer": "sample answer", "category": "category name"}},
                ...
            ],
            "common": [
                {{"question": "question text", "answer": "sample answer", "category": "category name"}},
                ...
            ],
            "hard": [
                {{"question": "question text", "answer": "sample answer", "category": "category name"}},
                ...
            ],
            "indepth": [
                {{"question": "question text", "answer": "sample answer", "category": "category name"}},
                ...
            ]
        }}
        
        Categories should include: Technical, Behavioral, Experience-based, Skills-based, Project-related, etc.
        Generate 5-7 questions per difficulty level.
        Make answers detailed and personalized based on the CV content.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean the response to extract JSON
            response_text = response.text
            # Remove markdown formatting if present
            response_text = re.sub(r'```json\s*|\s*```', '', response_text)
            return json.loads(response_text)
        except Exception as e:
            print(f"Error generating questions: {str(e)}")
            return self.get_default_questions()
    
    def get_chat_response_stream(self, cv_text, questions_context, user_message):
        """Generate streaming response for chat based on CV and questions"""
        prompt = f"""
        You are an interview preparation assistant. You have access to:
        1. The user's CV content
        2. Previously generated interview questions
        
        CV Content:
        {cv_text}
        
        Questions Context:
        {questions_context}
        
        User Message: {user_message}
        
        Please provide a helpful response related to interview preparation, focusing on:
        - Answering questions about the generated interview questions
        - Providing tips based on the user's CV
        - Helping with interview preparation strategies
        - Only discuss topics related to the CV content and interview preparation
        
        Keep responses concise but informative.
        """
        
        try:
            response = self.model.generate_content(prompt, stream=True)
            return response
        except Exception as e:
            return None
    
    def get_chat_response(self, cv_text, questions_context, user_message):
        """Generate response for chat based on CV and questions (non-streaming fallback)"""
        prompt = f"""
        You are an interview preparation assistant. You have access to:
        1. The user's CV content
        2. Previously generated interview questions
        
        CV Content:
        {cv_text}
        
        Questions Context:
        {questions_context}
        
        User Message: {user_message}
        
        Please provide a helpful response related to interview preparation, focusing on:
        - Answering questions about the generated interview questions
        - Providing tips based on the user's CV
        - Helping with interview preparation strategies
        - Only discuss topics related to the CV content and interview preparation
        
        Keep responses concise but informative.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def get_default_questions(self):
        """Fallback questions if API fails"""
        return {
            "frequent": [
                {"question": "Tell me about yourself.", "answer": "This is a common opening question...", "category": "Behavioral"},
                {"question": "What are your strengths?", "answer": "Focus on relevant strengths...", "category": "Behavioral"},
            ],
            "common": [
                {"question": "Why do you want this job?", "answer": "Connect your goals with the role...", "category": "Behavioral"},
                {"question": "Where do you see yourself in 5 years?", "answer": "Show ambition and alignment...", "category": "Behavioral"},
            ],
            "hard": [
                {"question": "Describe a challenging project you worked on.", "answer": "Use STAR method...", "category": "Experience-based"},
            ],
            "indepth": [
                {"question": "How would you handle a difficult team situation?", "answer": "Show leadership and problem-solving...", "category": "Behavioral"},
            ]
        }
