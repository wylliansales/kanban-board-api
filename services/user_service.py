import jwt
import datetime
from repository import user_repository
from werkzeug.security import check_password_hash

def create_user(name, email, password):
    if user_repository.get_user_by_email(email):
        return None
    return user_repository.create_user(name, email, password)

def get_user_by_email(email):
    return user_repository.get_user_by_email(email)

def authenticate_user(email, password):
    user = user_repository.get_user_by_email(email)
    if user and check_password_hash(user.password, password):
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, 'your-secret-key', algorithm='HS256')
        return token
    return None

def update_user(user_id, name, email, password):
    user_repository.update_user(user_id, name, email, password)

def delete_user(user_id):
    user_repository.delete_user(user_id)
