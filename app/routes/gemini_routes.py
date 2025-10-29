from flask import Blueprint, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv 
import os

load_dotenv()

gemini_bp = Blueprint('gemini', __name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("AIzaSyCYJzQ5FiV9qRffwOoTTkHVm0tCEnDWsNM"))

@gemini_bp.route('/ask', methods=['POST'])
def ask_gemini():

    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Use Gemini model
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return jsonify({
        "response": response.text
    }), 200
