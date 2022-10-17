from flask import request, jsonify
from src import app, rdis
from src.models import User
import jwt
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*ards, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['id']).first()

        except:
            return jsonify({'message': 'Token is invalid'}), 401
        if rdis.get_token(str(current_user.id)):
            return f(current_user, *ards, **kwargs)
        else:
            return False

    return decorated






