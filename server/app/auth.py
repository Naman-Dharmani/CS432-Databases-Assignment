# from flask import redirect, request, make_response, jsonify, url_for

# from flask_jwt_extended import create_access_token, unset_jwt_cookies
# from flask_dance.contrib.google import google

# from .models import User
# from . import app

from flask import flash
from flask_login import login_user, current_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from .models import db, User, OAuth


google_bp = make_google_blueprint(
    scope=[
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "openid",
    ],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)


# @app.route("/login", methods=["POST"])
# def login():
#     try:
#         data = request.json
#         user = User.query.filter_by(email=data["email"]).first()
#         if not user:
#             return make_response(jsonify({"message": "User not found"}), 404)

#         if user and user.check_password(data["password"]):
#             access_token = create_access_token(identity=data["email"])
#             return make_response(jsonify({"access_token": access_token}), 200)
#         else:
#             return make_response(jsonify({"message": "Invalid credentials"}), 401)

#     except Exception as e:
#         return make_response(jsonify({"error": str(e)}), 500)


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    info = resp.json()
    user_id = info["id"]

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name, provider_user_id=user_id)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(provider=blueprint.name,
                      provider_user_id=user_id, token=token)

    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in.")

    else:
        # Create a new local user account for this user
        # user = User(email=info["email"])
        user = User(
            name="Alice Smith",
            email=info["email"],
            password="password123",
            phone_no="2345678907",
            gender="Female",
            residence_location="Los Angeles",
            residence_number="456 Elm St",
        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(google_bp)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


# @app.route("/logout", methods=["POST"])
# def logout():
#     response = jsonify({"msg": "logout successful"})
#     unset_jwt_cookies(response)
#     return response
