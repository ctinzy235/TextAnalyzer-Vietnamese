from flask import Blueprint, request, jsonify
from modules.pos_ner.pos_ner import pos_tagging as tag_text
from modules.pos_ner.pos_ner import ner_tagging as ner_text
from modules.preprocessing import preprocess_text
pos_bp = Blueprint('pos', __name__)

@pos_bp.route('/tag', methods=['POST'])
def tag():
    data = request.get_json()
    text = data.get('text', '')
    model = data.get('model', 'underthesea')
    if not text:
        return jsonify({"error": "No text provided"}), 400
    text = preprocess_text(text, remove_icon=True)
    if not text:
        return jsonify({"error": "No text provided"}), 400
    print(f"Received text for POS tagging: {text[:50]}...")  # Log first 50 characters for debugging
    if model == "underthesea":
        result = tag_text(text, model = "underthesea")
    elif model == "vncorenlp":
        result = tag_text(text, model = "vncorenlp")
    else:
        return jsonify({"error": "Invalid model specified"}), 400
    return jsonify({"result": result})

    data = request.get_json()
    text = data.get('text', '')
    model = data.get('model', 'vncorenlp')
    if not text:
        return jsonify({"error": "No text provided"}), 400

    if model == "underthesea":
        result = ner_text(text, model = "underthesea")
    elif model == "vncorenlp":
        result = ner_text(text, model = "vncorenlp")
    else:
        return jsonify({"error": "Invalid model specified"}), 400

    return jsonify({"result": result})