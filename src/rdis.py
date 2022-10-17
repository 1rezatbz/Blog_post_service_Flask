# import redis
#
# redis_db = redis.Redis(host='localhost', port=6379, db=0)
#
#
# def get_token(id: str):
#     return redis_db.get(id)
#
#
# def set_token(id: int, token: str):
#     return redis_db.set(str(id), token)
#
#
# def delete_token(id: int):
#     return redis_db.delete(str(id))