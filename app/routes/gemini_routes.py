from flask import Blueprint, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os
import base64

load_dotenv()

gemini_bp = Blueprint('gemini', __name__)

# ✅ Correctly load API key from .env
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@gemini_bp.route('/ask', methods=['POST'])
def ask_gemini():
    data = request.get_json()

    query = data.get("query")
    image_data = data.get("image")

    if not query and not image_data:
        return jsonify({"error": "Either 'query' or 'image' is required."}), 400

    # ✅ Create the model
    model = genai.GenerativeModel("gemini-2.0-flash")

    # ✅ Prepare input for multimodal requests
    if image_data:
        image_base64 = image_data.get("base64")
        mime_type = image_data.get("mimeType", "image/png")

        try:
            image_bytes = base64.b64decode(image_base64)
            response = model.generate_content([
                {"mime_type": mime_type, "data": image_bytes},
                {"text": query or "Analyze this image for plant disease or issues."}
            ])
        except Exception as e:
            return jsonify({"error": f"Error processing image: {str(e)}"}), 500
    else:
        response = model.generate_content(query)

    return jsonify({"response": response.text}), 200
