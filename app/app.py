from collections import UserDict
import hashlib
import secrets
import datetime as dt
import os
from hashids import Hashids

from app.db_connector import *

accessType = [
    'project',
    'company',
    'user'
]
accessHashid = Hashids(os.environ['HASHID_SALT'], 10)

def login(data):
    with SessionContext() as session:
        users = session.query(Users).filter_by(user_name=data['user_name']).all()
        password = hashlib.sha256(data['user_password'].encode()).hexdigest()
        if len(users) == 1:
            user = users[0]
            if user.user_password == password:
                return {
                    'isValid': True,
                    'token': new_token(user.id),
                }
            else:
                return {
                    'isValid': False,
                    'msg': 'パスワードが間違っています'
                }
        else:
            return {
                'isValid': False,
                'msg': 'ユーザネームが違います'
            }

def signup(data):
    with SessionContext() as session:
        found = len(session.query(Users).filter_by(user_name=data['user_name']).all())
    if found:
        return {
            'isValid': False,
            'msg': '既に存在するユーザネームです'
        }
    else:
        with SessionContext() as session:
            session.add(Users(
                user_name=data['user_name'],
                user_password=hashlib.sha256(data['user_password'].encode()).hexdigest(),
                created_at=dt.datetime.now().isoformat(' ', 'seconds')
            ))
        with SessionContext() as session:
            return {
                'isValid': True,
                'msg': 'アカウント登録に成功しました',
                'token': new_token(session.query(Users).filter_by(user_name=data['user_name']).one().id)
            }

def check_login(token):
    if token == 'none':
        return False
    with SessionContext() as session:
        return session.query(TokenTable).filter_by(token=token).one_or_none() is not None

def new_token(user_id):
    with SessionContext() as session:
        token = secrets.token_hex()
        session.add(TokenTable(
            token=token,
            user_id=user_id
        ))
        return token

def verify_user(token):
    if token == 'none':
        return False
    with SessionContext() as session:
        user = session.query(TokenTable).filter_by(token=token).one_or_none()
        return int(user.user_id) if user is not None else False

def username(user_id):
    if user_id is False:
        return 'Anonymous'
    with SessionContext() as session:
        return session.query(Users).get(user_id).user_name

def generateHashID(access_type, ids):
    if not isinstance(access_type, int):
        access_type = accessType.index(access_type)
    return accessHashid.encode(ids, access_type)

def decodeHashID(hash):
    data = accessHashid.decode(hash)
    return {
        'ids': data[0],
        'access_type': accessType[data[1]]
    }

def validID_project(user_id):
    with SessionContext() as session:
        return [accessHashid.encode(int(v), 0) for v in session.query(Users).get(user_id).projects.split(',')]

def validID_company(user_id):
    with SessionContext() as session:
        return [accessHashid.encode(int(v), 1) for v in session.query(Users).get(user_id).companies.split(',')]

def validID_user(user_id):
    friends = set()
    with SessionContext() as session:
        user = session.query(Users).get(user_id)
        for company in user.companies.split(','):
            friends |= {int(member) for member in session.query(Company).get(int(company)).members.split(',')}
        for project in user.projects.split(','):
            friends |= {int(member) for member in session.query(Projects).get(int(project)).members.split(',')}
    friends.remove(user_id)
    return [accessHashid.encode(f, 2) for f in friends]

def setfeedback(user_id, msg):
    if user_id is False:
        user_id = -1
    new = FeedBacks(
        user_id=user_id,
        msg=msg,
        unread=0
    )
    with SessionContext() as session:
        session.add(new)
        session.flush()
        return new.id

def unreadmessage(user_id):
    if user_id is False:
        return []
    with SessionContext() as session:
        return [f'FEEDBACK`{feedback.msg}`ありがとうございました。以下返信です：{feedback.response}' for feedback in session.query(FeedBacks).filter_by(user_id=user_id).all() if feedback.unread]
