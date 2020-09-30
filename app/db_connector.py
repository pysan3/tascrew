from ast import Str
from sqlalchemy import create_engine, Column, Integer, String, Boolean
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
	real_name = Column('real_name', String)
	address = Column('address', String)
	ocupation = Column('ocupation', String)
	off_days = Column('off_days', String)
	off_times = Column('off_times', String)
	companies = Column('companies', String)
	projects = Column('projects', String)

	def __repr__(self):
		return '<Users(id=%s, user_name=%s, user_password=%s, created_at=%s, google_cred=%s, email=%s, phone_number=%s, nick_name=%s, real_name=%s, address=%s, ocupation=%s, off_days=%s, off_times=%s, companies=%s, projects=%s, )>' \
			% (self.id, self.user_name, self.user_password, self.created_at, self.google_cred, self.email, self.phone_number, self.nick_name, self.real_name, self.address, self.ocupation, self.off_days, self.off_times, self.companies, self.projects, )

class Company(Base):
	__tablename__ = 'company'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	company_name = Column('company_name', String)
	department = Column('department', String)
	employee_number = Column('employee_number', String)
	address = Column('address', String)
	email = Column('email', String)
	phone_number = Column('phone_number', String)
	admin = Column('admin', String)
	sub_admin = Column('sub_admin', String)
	members = Column('members', String)

	def __repr__(self) -> str:
		return '<Company(id=%s, company_name=%s, department=%s, employee_number=%s, address=%s, email=%s, phone_number=%s, admin=%s, sub_admin=%s, members=%s, )>' \
			% (self.id, self.company_name, self.department, self.employee_number, self.address, self.email, self.phone_number, self.admin, self.sub_admin, self.members)

class UsersSchedule(Base):
	__tablename__ = 'usersschedule'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	user_id = Column('user_id', Integer)
	pre_spare_time = Column('pre_spare_time', Integer)
	post_spare_time = Column('post_spare_time', Integer)
	kind = Column('kind', String)
	event_id = Column('event_id', String)
	created = Column('created', String)
	updated = Column('updated', String)
	summary = Column('summary', String)
	description = Column('description', String)
	location = Column('location', String)
	creator = Column('creator', String)
	organizer = Column('organizer', String)
	start = Column('start', String)
	end = Column('end', String)
	icaluid = Column('icaluid', String)
	extendedproperties = Column('extendedproperties', String)

	def __repr__(self) -> str:
		return '<UsersSchedule(id=%s, user_id=%s, pre_spare_time=%s, post_spare_time=%s, kind=%s, event_id=%s, created=%s, updated=%s, summary=%s, description=%s, location=%s, creator=%s, organizer=%s, start=%s, end=%s, icaluid=%s, extendedproperties=%s, )>' \
			% (self.id, self.user_id, self.pre_spare_time, self.post_spare_time, self.kind, self.event_id, self.created, self.updated, self.summary, self.description, self.location, self.creator, self.organizer, self.start, self.end, self.icaluid, self.extendedproperties, )

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

class Tasks(Base):
	__tablename__ = 'tasks'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	task_name = Column('task_name', String)
	master_object = Column('master_object', String)
	creator = Column('creator', String)
	organizer = Column('organizer', String)
	start_time_strict = Column('start_time_strict', String)
	end_time_strict = Column('end_time_strict', String)
	start_time = Column('start_time', String)
	end_time = Column('end_time', String)
	priority = Column('priority', String)
	files = Column('files', String)
	description = Column('description', String)
	need_check = Column('need_check', Boolean)
	check_status = Column('check_status', Integer)
	feedback = Column('feedback', String)

	def __repr__(self) -> str:
		return '<Tasks(id=%s, task_name=%s, master_object=%s, creator=%s, organizer=%s, start_time_strict=%s, end_time_strict=%s, start_time=%s, end_time=%s, priority=%s, files=%s, description=%s, need_check=%s, check_status=%s, feedback=%s, )>' \
			% (self.id, self.task_name, self.master_object, self.creator, self.organizer, self.start_time_strict, self.end_time_strict, self.start_time, self.end_time, self.priority, self.files, self.description, self.need_check, self.check_status, self.feedback, )

class TaskLog(Base):
	__tablename__ = 'tasklog'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	user_id = Column('user_id', Integer)
	task_id = Column('task_id', Integer)
	start_time = Column('start_time', String)
	end_time = Column('end_time', String)

	def __repr__(self) -> str:
		return '<TaskLog(id=%s, user_id=%s, task_id=%s, start_time=%s, end_time=%s, )>' \
			% (self.id, self.user_id, self.task_id, self.start_time, self.end_time, )

class Notifications(Base):
	__tablename__ = 'notifications'
	id = Column('id', Integer, primary_key=True, autoincrement=True)

	def __repr__(self) -> str:
		return '<Notifications(id=%s, )>' \
			% (self.id)

class Projects(Base):
	__tablename__ = 'projects'
	id = Column('id', Integer, primary_key=True, autoincrement=True)
	project_name = Column('project_name', String)
	company_id = Column('company_id', Integer)
	members = Column('members', String)
	schedule_privacy_level = Column('schedule_privacy_level', Integer)
	chart_color = Column('chart_color', String)
	status = Column('status', Integer)
	current_type = Column('current_type', Integer)
	tree = Column('tree', String)

	def __repr__(self) -> str:
		return '<Projects(id=%s, project_name=%s, company_id=%s, members=%s, schedule_privacy_level=%s, chart_color=%s, status=%s, current_type=%s, tree=%s, )>' \
			% (self.id, self.project_name, self.company_id, self.members, self.schedule_privacy_level, self.chart_color, self.status, self.current_type, self.tree, )

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
