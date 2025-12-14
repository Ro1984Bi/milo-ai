from flask import Blueprint, request, jsonify
from utils.mistrlai_service import ask_mistral
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Prompt
from extension import db

prompt_bp = Blueprint("prompt", __name__)

# create user prompt
@prompt_bp.route("/prompt", methods=["POST"])
@jwt_required()
def create_prompt():
    data = request.get_json()
    user_id = get_jwt_identity()
    response = ask_mistral(data["prompt"])
    new_prompt = Prompt(user_id=user_id, prompt=data["prompt"], response=response)
    db.session.add(new_prompt)
    db.session.commit()
    return (
        jsonify(
            message="Prompt created successfully",
            id=new_prompt.id,
            response=new_prompt.response,
            prompt=new_prompt.prompt,
        ),
        201,
    )

# get all prompts
@prompt_bp.route("/prompts", methods=["GET"])
@jwt_required()
def get_prompts():
    user_id = get_jwt_identity()
    prompts = Prompt.query.filter_by(user_id=user_id).all()
    return (
        jsonify(
            [
                {"id": prompt.id, "prompt": prompt.prompt, "response": prompt.response}
                for prompt in prompts
            ]
        ),
        200,
    )

# update user prompt
@prompt_bp.route("/prompt/<int:id>", methods=["PUT"])
@jwt_required()
def update_prompt(id):
    data = request.get_json()
    prompt = Prompt.query.get_or_404(id)
    if prompt.user_id != int(get_jwt_identity()):
        return jsonify(message="Unauthorized"), 401
    prompt.prompt = data["prompt"]
    prompt.response = ask_mistral(data["prompt"])
    db.session.commit()
    return (
        jsonify(
            message="Prompt updated successfully",
            id=prompt.id,
            response=prompt.response,
            prompt=prompt.prompt,
        ),
        200,
    )

# delete user prompt
@prompt_bp.route("/prompt/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_prompt(id):
    prompt = Prompt.query.get_or_404(id)
    if prompt.user_id != int(get_jwt_identity()):
        return jsonify(message="Unauthorized"), 401
    db.session.delete(prompt)
    db.session.commit()
    return jsonify(message="Prompt deleted successfully"), 200