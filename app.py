from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re

app = Flask(__name__)

# Load .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model_name = "gemini-2.5-flash-lite"
gemini_model = genai.GenerativeModel(model_name)
print(f"Using Gemini model: {model_name}")

# Knowledge base
knowledge_base = {
    "college_name": "Chaitanya Bharathi Institute of Technology (CBIT)",
    "about": "Chaitanya Bharathi Institute Of Technology was established at Proddatur in YSR Kadapa District, Andhra Pradesh. It aims to provide quality education and research.",
    "vision": "To contribute through brilliance in education and research, producing competent and ethically strong professionals.",
    "mission": "• Imparting quality education\n• Fostering an empowered workforce\n• Promoting entrepreneurial skills",
    "founder": "Sri. V. Jayachandra Reddy",
    "chairman": "V. Jaya Chandra Reddy",
    "principal": "Dr. S. SRUTHI, M.E, Ph.D",
    "ceo": "V. Lohit Reddy",
    "directors": {
        "academics": "Prof. G.K.D. Prasanna Venkatesan",
        "admin": "Dr. G. Sreenivasulu Reddy"
    },
    "affiliations": "Approved by AICTE, Affiliated to JNTUA, Recognized by UGC, Accredited by NBA & NAAC (Grade A)",
    "courses": {
        "ug": [
            "CSE (360)", "CSE (AI) (180)", "CSE (AI & ML) (60)",
            "ECE (180)", "EEE (60)", "MECH (30)", "CIVIL (30)", "CSE (DS)"
        ],
        "pg": ["MBA (60)"],
        "diploma": ["DCME (120)", "DECE (120)", "DEEE (60)", "DCE (60)"]
    },
    "contact": "Chaitanya Bharathi Institute Of Technology, Vidya Nagar, Proddatur, YSR Kadapa (Dist.), AP 516360. Mail: info@cbit.edu.in | Phone: +91-9640808099"
}

# Restricted keywords (handled instantly)
restricted_keywords = ["fee", "fees", "placement", "placements", "faculty", "facilities", "hostel", "bus", "transport"]

# Aliases
aliases = {
    "cbit": "chaitanya bharathi institute of technology",
    "chaitanya bharathi": "chaitanya bharathi institute of technology"
}

# Knowledge keywords mapping → KB key
kb_keywords = {
    "about": "about",
    "information": "about",
    "cbit": "about",
    "where": "about",
    "vision": "vision",
    "mission": "mission",
    "founder": "founder",
    "chairman": "chairman",
    "principal": "principal",
    "ceo": "ceo",
    "director": "directors",
    "courses": "courses",
    "programs": "courses",
    "contact": "contact",
    "address": "contact",
    "website": "contact"
}

def preprocess_query(query):
    query_lower = query.lower()
    for alias, full_form in aliases.items():
        if alias in query_lower:
            query_lower = query_lower.replace(alias, full_form)
    return query_lower

def get_gemini_response(message: str) -> str:
    """Fallback to Gemini if KB and restricted keywords do not match."""
    try:
        response = gemini_model.generate_content(message)
        if hasattr(response, "text"):
            return response.text.strip()
        elif isinstance(response, str):
            return response.strip()
        else:
            return "Sorry, I couldn’t generate a proper response."
    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return "⚠️ Error processing your request. Please try again later."

@app.route("/")
def home():
    return render_template("chatbot.html")  # serve frontend

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    processed_input = preprocess_query(user_input)

    # 1️⃣ Check knowledge base keywords first
    for key, kb_field in kb_keywords.items():
        if key in processed_input:
            kb_response = knowledge_base[kb_field]
            # If value is a dict (like directors), convert to string
            if isinstance(kb_response, dict):
                kb_response = "\n".join([f"{k.title()}: {v}" for k, v in kb_response.items()])
            # If value is a list (like courses), join them
            if isinstance(kb_response, list):
                kb_response = ", ".join(kb_response)
            return jsonify({"response": kb_response})

    # 2️⃣ Check restricted keywords
    if any(re.search(rf"\b{word}\b", processed_input) for word in restricted_keywords):
        return jsonify({
            "response": "I currently don’t have that data. Please check the official website: https://cbit.edu.in or contact: +91-9640808099"
        })

    # 3️⃣ Fallback → Gemini
    return jsonify({"response": get_gemini_response(user_input)})

if __name__ == "__main__":
    app.run(debug=True)
