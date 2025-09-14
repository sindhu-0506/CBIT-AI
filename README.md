CBIT Personal & Learning Assistant Chatbot

A web-based chatbot designed for CBIT students and outsiders to provide instant information about Chaitanya Bharathi Institute of Technology (CBIT) and act as a personal learning assistant. The chatbot uses a knowledge base for college-specific queries and falls back on Google Gemini AI for general learning queries or quizzes.

Features

CBIT Knowledge Base: Provides instant answers about the college—vision, mission, courses, contact info, founder, directors, etc.

Restricted Queries: For sensitive topics like fees, placements, or hostel facilities, it gives the official website and contact information.

Learning Assistant: Assists with programming concepts, general knowledge, and other educational queries via Google Gemini AI.

Quiz Support: Can handle quiz-related questions intelligently.

Responsive UI: Chat interface with messages on left (AI) and right (user), using purple, white, and black shades.

Easy Interaction: Send messages via Enter key or Send button.

Project Structure
CBIT-Chatbot/
├── app.py              # Main Flask backend + Gemini AI integration
├── templates/
│   └── chatbot.html    # Frontend
├── .env                # API key for Gemini AI
├── requirements.txt    # Python dependencies
└── README.md           # Project description

Files Overview
app.py

Main Flask application.

Serves the frontend (chatbot.html) and handles /chat POST requests.

First checks the CBIT knowledge base, then checks for restricted keywords, and finally falls back to Gemini AI.

chatbot.html

Frontend HTML page for the chatbot interface.

Features a scrollable chat box, styled messages (user vs bot), input field, and send button.

Handles Enter key to send messages.

Uses shades of purple, white, and black for a professional look.

.env

Stores your Google Gemini API key securely.

Format:

GEMINI_API_KEY=your_api_key_here

Getting Started

Clone the repository:

git clone <repository-url>
cd CBIT-Chatbot


Create a virtual environment:

python -m venv venv
# Activate it
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows


Install dependencies:

pip install -r requirements.txt


Add your Gemini API key to .env:

GEMINI_API_KEY=your_api_key_here


Run the Flask app:

python app.py


Open your browser:
Visit  to chat with your CBIT Personal & Learning Assistant.
