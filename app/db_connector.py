from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

__version__ = "0.1.0"

engine = create_engine(os.environ['DATABASE_URL'], echo=False)
Session: sessionmaker = sessionmaker(bind=engine)
Base = declarative_base()

class Users(Base):
	__tablename__ = 'users'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	user_name = Column('user_name', String)
	user_password = Column('user_password', String)
	created_at = Column('created_at', String)
	google_cred = Column('google_cred', String)
	email = Column('email', String)
	phone_number = Column('phone_number', String)
	nick_name = Column('nick_name', String)
	address = Column('address', String)
	ocupation = Column('ocupation', String)

	def __repr__(self):
		return '<Users(id=%s, user_name=%s, user_password=%s, created_at=%s, google_cred=%s, email=%s, phone_number=%s, nick_name=%s, address=%s, ocupation)>' \
			% (self.id, self.user_name, self.user_password, self.created_at, self.google_cred, self.email, self.phone_number, self.nick_name, self.address, self.ocupation)

class UsersGoogleCalendar(Base):
	__tablename__ = 'usersgooglecalendar'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	user_id = Column('user_id', Integer)
	calendar_id = Column('calendar_id', String)
	summary = Column('summary', String)
	description = Column('description', String)
	privacy_level = Column('privacy_level', Integer)

	def __repr__(self) -> str:
		return '<UsersGoogleCalendar(id=%s, user_id=%s, calendar_id=%s, summary=%s, description=%s, privacy_level=%s, )>' \
			% (self.id, self.user_id, self.calendar_id, self.summary, self.description, self.privacy_level)

class TokenTable(Base):
	__tablename__ = 'tokentable'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	token = Column('token', String)
	user_id = Column('user_id', Integer)

	def __repr__(self):
		return '<TokenTable(id=%s, token=%s, user_id=%s)>' \
			% (self.id, self.token, self.user_id)

class SessionContext(object):
    def __init__(self):
        self.session: Session = Session()

    def __enter__(self) -> Session:
        return self.session

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.flush()
        self.session.commit()
        self.session.close()

class FeedBacks(Base):
	__tablename__ = 'feedbacks'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	user_id = Column('user_id', Integer)
	msg = Column('msg', String)
	response = Column('response', String)
	unread = Column('unread', Integer)

	def __repr__(self):
		return '<FeedBacks(id=%s, user_id=%s, msg=%s, response=%s, unread=%s)' \
			% (self.id, self.user_id, self.msg, self.response, self.unread)

def DBtoDict(obj, delete=[]):
	tmp = obj.__dict__
	tmp.pop('_sa_instance_state', None)
	for d in delete:
		tmp.pop(d, None)
	return tmp
