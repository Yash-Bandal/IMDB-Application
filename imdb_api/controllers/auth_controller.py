from flask import Blueprint, jsonify

from imdb_api.services.auth_service import login
from imdb_api.utils.validation import body_json, required_text


auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.post("/api/auth/login")
def login_route():
    data = body_json()
    email = required_text(data.get("emailid"), "Email Id")
    password = required_text(data.get("password"), "Password")
    token = login(email, password)
    return jsonify(data={"accessToken": token})
