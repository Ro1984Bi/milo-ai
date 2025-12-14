from flask import Blueprint, request, jsonify
from extension import db
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"]).first()
    if user and user.check_password(data["password"]):
        access_token = create_access_token(identity=str(user.id))
        return (
            jsonify(
                {"message": "User logged in successfully", "access_token": access_token}
            ),
            200,
        )
    else:
        return jsonify({"message": "Invalid email or password"}), 401
    

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "User logged out successfully"}), 200