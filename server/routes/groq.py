from flask import Blueprint, request, jsonify
from utils.groq_service import ask_groq
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Prompt
from extension import db

groq_bp = Blueprint("groq", __name__)

# ---------------------------------------
# CREATE PROMPT
# ---------------------------------------
@groq_bp.route("/prompt", methods=["POST"])
@jwt_required()
def create_prompt():
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify(error="Missing 'prompt' field"), 400

    if not data["prompt"].strip():
        return jsonify(error="Prompt cannot be empty"), 400

    user_id = get_jwt_identity()

    response = ask_groq(data["prompt"])
    if isinstance(response, str) and response.startswith("Error"):
        return jsonify(error=response), 500

    new_prompt = Prompt(
        user_id=user_id,
        prompt=data["prompt"],
        response=response
    )

    db.session.add(new_prompt)
    db.session.commit()

    return jsonify(
        message="Prompt created successfully",
        id=new_prompt.id,
        prompt=new_prompt.prompt,
        response=new_prompt.response
    ), 201


# ---------------------------------------
# GET USER PROMPTS
# ---------------------------------------
@groq_bp.route("/prompts", methods=["GET"])
@jwt_required()
def get_prompts():
    user_id = get_jwt_identity()

    try:
        prompts = Prompt.query.filter_by(user_id=user_id).all()
    except Exception:
        return jsonify(error="Database error"), 500

    results = [
        {
            "id": p.id,
            "prompt": p.prompt,
            "response": p.response
        }
        for p in prompts
    ]

    return jsonify(count=len(results), items=results), 200


# ---------------------------------------
# UPDATE PROMPT
# ---------------------------------------
@groq_bp.route("/prompt/<int:id>", methods=["PUT"])
@jwt_required()
def update_prompt(id):
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify(error="Missing 'prompt' field"), 400

    if not data["prompt"].strip():
        return jsonify(error="Prompt cannot be empty"), 400

    prompt = Prompt.query.get_or_404(id)

    if prompt.user_id != int(get_jwt_identity()):
        return jsonify(message="Unauthorized"), 401

    response = ask_groq(data["prompt"])
    if isinstance(response, str) and response.startswith("Error"):
        return jsonify(error=response), 500

    prompt.prompt = data["prompt"]
    prompt.response = response

    db.session.commit()

    return jsonify(
        message="Prompt updated successfully",
        id=prompt.id,
        prompt=prompt.prompt,
        response=prompt.response
    ), 200


# ---------------------------------------
# DELETE PROMPT
# ---------------------------------------
@groq_bp.route("/prompt/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_prompt(id):
    prompt = Prompt.query.get_or_404(id)

    if prompt.user_id != int(get_jwt_identity()):
        return jsonify(message="Unauthorized"), 401

    db.session.delete(prompt)
    db.session.commit()

    return jsonify(message="Prompt deleted successfully"), 200
