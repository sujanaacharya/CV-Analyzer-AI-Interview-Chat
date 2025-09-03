CV Analyzer AI Interview Chat

An AI-powered web application that allows users to upload their CVs, automatically generates interview questions based on the CV, and provides an AI chatbot interface for practicing interview questions and receiving guidance.

Features

CV Upload: Upload PDF, DOCX, DOC, or TXT files.

Automatic Question Generation: Generates interview questions across different difficulty levels (frequent, common, hard, indepth) based on the uploaded CV.

AI Chat Interface: Chat with an AI assistant to get tips, answer questions, and practice interview responses.

Chat History: Stores previous chat messages linked to each CV.

Web Interface: Built with Django templates and styled with Bootstrap.

Tech Stack

Backend: Django, Python

AI Integration: Google Gemini API (via google.generativeai)

Frontend: HTML, CSS, JavaScript, Bootstrap

Database: Django ORM (default SQLite, can be configured)

File Handling: PyPDF2 for PDFs, python-docx for Word documents

Installation

Clone the repository:

git clone https://github.com/sujanaacharya/CV-Analyzer-AI-Interview-Chat.git
cd CV-Analyzer-AI-Interview-Chat


Create a virtual environment:

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Linux/Mac


Install dependencies:

pip install -r requirements.txt


Set up environment variables in a .env file:

GEMINI_API_KEY=your_google_gemini_api_key


Apply migrations:

python manage.py migrate


Run the development server:

python manage.py runserver


Open http://127.0.0.1:8000/ in your browser.

Usage

Upload a CV from the home page.

The system will generate interview questions automatically.

Go to the Chat interface to interact with the AI assistant for interview practice.

Chat history is saved for each uploaded CV.

Notes

Ensure your Google Gemini API key is valid and set correctly in .env.

The streaming AI chat requires modern browsers that support EventSource.

Currently designed for development/testing. For production, a proper WSGI/ASGI server is recommended.

License

MIT License

checkout the full working of the system : https://drive.google.com/file/d/1l1de_fConclYSVstZ0mDa08GUo7itAc6/view?usp=sharing
