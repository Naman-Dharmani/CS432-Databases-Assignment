from flask import request, make_response, jsonify
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from .models import User
from . import app


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        user = User(name=data['name'],
                    email=data['email'],
                    password=data['password'],
                    phone_no=data['phone_no'],
                    gender=data['gender'],
                    residence_location=data['residence_location'],
                    residence_number=data['residence_number'],
                    anonymity_level=data['anonymity_level'],
                    theme_preference=data['theme_preference'],
                    language_preference=data['language_preference'],
                    notification_preference=data['notification_preference']
                    )
        user.set_password(data['password'])
        user.save()
        return make_response(jsonify({"message": "User created successfully"}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        if user and user.check_password(data['password']):
            access_token = create_access_token(identity=data['email'])
            return make_response(jsonify({"access_token": access_token}), 200)
        else:
            return make_response(jsonify({"message": "Invalid credentials"}), 401)

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response
