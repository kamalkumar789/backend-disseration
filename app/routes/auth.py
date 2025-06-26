from flask import Blueprint, request, jsonify, session
from app._init_ import db
from app.models.users import Users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    consent = data.get('consent', False)
    usertype = data.get('usertype', False)

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    if Users.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = Users(username=username, consent=consent, user_type=usertype)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('username')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'This user is not registered'}), 400

    if not user.check_password(password):
        return jsonify({'error': 'Invalid password'}), 401

    session['user_id'] = user.id

    return jsonify({'message': 'User logged in successfully'})


@auth_bp.route('/whoami', methods=['POST'])
def whoami():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Session not active'}), 400

    session['user_id'] = user_id

    return jsonify({'message': 'User logged in successfully', 'user_id': user_id})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear() 
    return jsonify({'message': 'Logged out successfully'}), 200