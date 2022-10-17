from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    admin = db.Column(db.Boolean)
    username = db.Column(db.String(12), nullable=False, unique=True)
    password = db.Column(db.String(12), nullable=False)
    booking = db.relationship('Booking', backref='person', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.admin} - {self.username})'


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(12), nullable=False, unique=True)
    detail = db.Column(db.String(150), nullable=False,)
    booking = db.relationship('Booking', backref='digit', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.number} - {self.detail} )'


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_status = db.Column(db.String, nullable=False)
    date_in = db.Column(db.String, nullable=False)
    date_out = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id} - {self.room_status} - {self.date_in} - {self.date_out})'
