import hashlib
import secrets
import datetime as dt
import json
import os
from hashids import Hashids

from app.db_connector import *

accessType = [
    'company',
    'project',
    'user',
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
            'msg': '既に存在するユーザネームです',
            'already_taken': True
        }
    else:
        project_dict = json.dumps({'admin':[],'sub_admin':[],'members':[]})
        with SessionContext() as session:
            session.add(Users(
                user_name=data['user_name'],
                user_password=hashlib.sha256(data['user_password'].encode()).hexdigest(),
                created_at=dt.datetime.now().isoformat(' ', 'seconds'),
                icon='/static/usericons/default.png',
                email=data['email'],
                phone_number=data['phone_number'],
                nick_name=data['nick_name'],
                real_name=data['real_name'],
                zipcode='-'.join(data['zipcode']),
                address='/'.join(data['address']),
                ocupation=json.dumps(data['ocupation']),
                companies=project_dict,
                projects=project_dict,
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

def generateHashID(ids, access_type):
    if not isinstance(access_type, int):
        access_type = accessType.index(access_type)
    return accessHashid.encode(ids, access_type)

def decodeHashID(hash):
    data = accessHashid.decode(hash)
    return {
        'ids': data[0],
        'access_type': accessType[data[1]]
    }

def validID_company(user_id):
    with SessionContext() as session:
        return [generateHashID(v, 'company') for v in sum(json.loads(session.query(Users).get(user_id).companies).values(), [])]

def validID_project(user_id):
    with SessionContext() as session:
        return [generateHashID(v, 'project') for v in sum(json.loads(session.query(Users).get(user_id).projects).values(), [])]

def validID_user(user_id):
    friends = {user_id}
    with SessionContext() as session:
        user = session.query(Users).get(user_id)
        user_projects = json.loads(user.projects)
        user_companies = json.loads(user.companies)
        friends |= {session.query(Projects).get(i).admin for i in user_projects['admin']}
        friends |= {session.query(Company).get(i).admin for i in user_companies['admin']}
        auth_types = ['admin', 'sub_admin', 'members']
        for i in range(1, len(auth_types)):
            user_projects[auth_types[i]].extend(user_projects[auth_types[i - 1]])
            user_companies[auth_types[i]].extend(user_companies[auth_types[i - 1]])
            for project in user_projects[auth_types[i]]:
                friends |= {member for member in json.loads(getattr(session.query(Projects).get(project), auth_types[i]))}
            for company in user_companies[auth_types[i]]:
                friends |= {member for member in json.loads(getattr(session.query(Company).get(company), auth_types[i]))}
    friends.remove(user_id)
    return [generateHashID(f, 'user') for f in friends]

def get_company(data_id, privacy_level):
    with SessionContext() as session:
        data = DBtoDict(session.query(Company).get(data_id), ['id'])
        return {k: v for k, v in data.items() if Company.privacy_settings[k] <= privacy_level}

def get_project(data_id, privacy_level):
    with SessionContext() as session:
        data = DBtoDict(session.query(Projects).get(data_id), ['id'])
        return {k: v for k, v in data.items() if Projects.privacy_settings[k] <= privacy_level}

def get_user(data_id, privacy_level):
    with SessionContext() as session:
        data = DBtoDict(session.query(Users).get(data_id), ['id'])
        return {k: v for k, v in data.items() if Users.privacy_settings[k] <= privacy_level}

def add_company(data):
    new = Company(
        company_name=data['company_name'],
        icon=data['icon'],
        department=data['department'],
        employee_number=int(data['employee_number']),
        zipcode=data['zipcode'],
        address=data['address'],
        email=data['email'],
        phone_number=data['phone_number'],
        admin=int(data['admin']),
        sub_admin=json.dumps(data['sub_admin']),
        members=json.dumps(data['members']),
    )
    with SessionContext() as session:
        session.add(new)
        session.flush()
        user = session.query(Users).get(data['admin'])
        user.companies = add_admin(user.companies, 'admin', new.id)
        return generateHashID(new.id, 'company')

def add_project(data):
    new = Projects(
        project_name=data['project_name'],
        icon=data['icon'],
        company_id=data['company_id'],
        admin=int(data['admin']),
        sub_admin=json.dumps(data['sub_admin']),
        members=json.dumps(data['members']),
        schedule_privacy_level=data['schedule_privacy_level'],
        chart_color=data['chart_color'],
        status=0,
        current_type=0,
        tree=data['tree'],
    )
    with SessionContext() as session:
        session.add(new)
        session.flush()
        user = session.query(Users).get(data['admin'])
        user.projects = add_admin(user.projects, 'admin', new.id)
        return generateHashID(new.id, 'project')

def add_member2company(company_id, user_id):
    with SessionContext() as session:
        company = session.query(Company).get(company_id)
        company.members = add_member2list(company.members, user_id)
        user = session.query(Users).get(user_id)
        user.companies = add_admin(user.companies, 'members', company_id)

def add_member2project(project_id, user_id):
    with SessionContext() as session:
        project = session.query(Projects).get(project_id)
        project.members = add_member2list(project.members, user_id)
        user = session.query(Users).get(user_id)
        user.projects = add_admin(user.projects, 'members', project_id)

def add_admin(data, auth_type, ids):
    tmp = json.loads(data)
    tmp[auth_type].append(int(ids))
    return json.dumps(tmp)

def add_member2list(data, ids):
    tmp = json.loads(data)
    tmp.append(ids)
    return json.dumps(tmp)

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
