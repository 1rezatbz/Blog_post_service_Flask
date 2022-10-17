from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session
from src.models import Booking, User, Room


es = Elasticsearch(hosts="localhost", port="9200")


def elastic(db: Session):
    bookings = Booking.query.all(db)
    if bookings:
        i = 1
        for booking in bookings:
            b = {"id": f"{booking.id}", "room_status": f"{booking.room_status}", "date_in": f"{booking.date_in}",
                 "date_out": f"{booking.date_out}", "user_id": f"{booking.user_id}", "room_id": f"{booking.room_id}"}
            es.index(index='bookings', body=b, id=i)
            i += 1
    users = User.query.all(db)
    if users:
        i = 1
        for user in users:
            u = {"id": f"{user.id}", "role": f"{user.admin}", "username": f"{user.username}", "password": f"{user.password}"}
            es.index(index='users', body=u, id=i)
            i += 1
    rooms = Room.query.all(db)
    i = 1
    for room in rooms:
        u = {"id": f"{room.id}", "number": f"{room.number}", "detail": f"{room.detail}"}
        es.index(index='rooms', body=u, id=i)
        i += 1
