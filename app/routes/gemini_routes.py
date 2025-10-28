from flask import Blueprint, request, jsonify
import google.generativeai as genai
import os

gemini_bp = Blueprint('gemini', __name__)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@gemini_bp.route('/ask', methods=['POST'])
def ask_gemini():
    """
    Route for AI responses. 
    Example request body:
    { "prompt": "Give me modern farming tips" }
    """
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Use Gemini model
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    return jsonify({
        "response": response.text
    }), 200
