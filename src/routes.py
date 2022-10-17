from flask import request, jsonify, make_response
from src import app, db, rdis
from src.models import User, Room, Booking
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from src.crude import token_required
from src.rdis import *
import datetime


@app.route('/', methods=['GET'])
def home():
    return jsonify({'Message': 'Welcome to hotel red'})


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="login required"'})
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="login required"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},
            app.config['SECRET_KEY'], algorithm="HS256")
        rdis.set_token(user.id, token)
        return jsonify({'token': token})
        # return jsonify({'token': token.decode('UTF-8')})
    return make_response('could not verify', 401, {'WWW-Authenticate': 'Basic realm="login required"'})


@app.route('/logout')
@token_required
def logout(current_user):
    delete_token(current_user.id)
    return jsonify({'message': 'You logout successfully'})


@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user is created!'})


@app.route('/user/<id>', methods=['PUT'])
@token_required
def promote_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No User found!'})
    user.admin = True
    db.session.commit()
    return jsonify({'message': 'the user has been promoted'})


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    users = User.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['admin'] = user.admin
        user_data['username'] = user.username
        user_data['password'] = user.password
        output.append(user_data)
    return jsonify({'Users': output})


@app.route('/user/<id>', methods=['DELETE'])
@token_required
def delete_user(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No User found!'})
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user has been Deleted'})


@app.route('/rooms', methods=['POST'])
@token_required
def add_room(current_user):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    data = request.get_json()
    new_room = Room(number=data['number'], detail=data['detail'])
    db.session.add(new_room)
    db.session.commit()
    return jsonify({'message': 'new room is created!'})


@app.route('/rooms', methods=['GET'])
@token_required
def get_all_room(current_user):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    users = Room.query.all()
    output = []
    for user in users:
        room_data = {}
        room_data['id'] = user.id
        room_data['number'] = user.number
        room_data['detail'] = user.detail
        output.append(room_data)
    return jsonify({'Room': output})


@app.route('/rooms/<id>', methods=['GET'])
@token_required
def get_one_room(current_user, id):
    room = Room.query.filter_by(id=id).first()
    if not room:
        return jsonify({'message': 'No User found!'})
    room_data = {}
    room_data['id'] = room.id
    room_data['number'] = room.number
    room_data['detail'] = room.detail
    return jsonify({'room': room_data})


@app.route('/rooms/<room_id>/booking', methods=['POST'])
@token_required
def booking(current_user, room_id):
    room = Room.query.filter_by(id=room_id).first()
    data = request.get_json()
    fdin = datetime.strptime(data["date_in"], '%Y-%m-%d').date()
    fdout = datetime.strptime(data["date_out"], '%Y-%m-%d').date()
    delta = fdout - fdin
    b1 = Booking.query.filter_by(room_id=room_id).all()
    if delta.days >= 1:
        for b in b1:
            bdin = datetime.strptime(b.date_in, '%Y-%m-%d').date()
            bdout = datetime.strptime(b.date_out, '%Y-%m-%d').date()
            if bdin < fdin and bdout < fdout:
                boo = Booking(room_status='1', date_in=data["date_in"], date_out=data["date_out"], user_id=current_user.id, room_id=room_id)
                db.session.add(boo)
                db.session.commit()
                return jsonify({'message': 'Your chosen room  is booked for you!'})
            else:
                return jsonify({'message': 'This room is occupied'})
    else:
        return jsonify({'message': 'Your entered date is wrong'})


@app.route('/booking/<id>', methods=['DELETE'])
@token_required
def delete_booking(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    book = Booking.query.filter_by(id=id).first()
    if not book:
        return jsonify({'message': 'No User found!'})
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'book has been Deleted'})


@app.route('/test', methods=['POST'])
@token_required
def test(current_user):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    data = request.get_json()
    new_booking = Booking(room_status='2', date_in=data["date_in"], date_out=data["date_out"], user_id=current_user.id, room_id=2)
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'message': 'Your trial book is done!'})


# @app.route('/voucher/<id>', methods=['GET'])
# @token_required
# def voucher():
#     booking_data = Booking.query.filter_by(id=id).first()
#     if not booking_data:
#         return jsonify({'message': 'No User found!'})
#     booking_data = {}
#     booking_data['id'] = booking_data.id
#     booking_data['date_in'] = booking_data.date_in
#     booking_data['date_out'] = booking_data.date_out
#     booking_data['room_id'] = booking_data.room_id
#     return jsonify({'Booking_data': booking_data})


@app.route('/bookingup', methods=['PUT'])
@token_required
def update_expire_room(current_user):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    expire_booking = Booking.query.filter(Booking.room_status.endswith('2')).all()
    for eb in expire_booking:
        dout = datetime.strptime(eb.date_out, '%Y-%m-%d')
        if datetime.now() > dout:
            eb.room_status = '0'
            db.session.commit()
        return jsonify({'Booking_data': 'room status is updated'})


@app.route('/booking/<id>', methods=['PUT'])
@token_required
def Settlement(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    settel_booking = Booking.query.filter_by(id=id).all()
    if settel_booking.room_status == '1':
        settel_booking.room_status = '2'
        db.session.commit()
        return jsonify({'Booking_data': 'The traveller has got his room'})


@app.route('/booking/<id>/ex', methods=['PUT'])
@token_required
def update_failed_booked(current_user, id):
    if not current_user.admin:
        return jsonify({'message': 'cannot perform that function'})
    failed_booking = Booking.query.filter_by(id=id).all()
    if failed_booking.room_status == '1':
        failed_booking.room_status = '0'
        db.session.commit()
        return jsonify({'Booking_data': 'Reservation is expired'})

