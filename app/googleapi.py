import datetime as dt
import json
from google.auth.credentials import Credentials
import google.auth.transport.requests
from google_auth_oauthlib.flow import Flow
from requests_oauthlib import oauth2_session
from googleapiclient.discovery import build

from app.db_connector import *

def hasCredentials(user_id: int) -> bool:
    with SessionContext() as session:
        return session.query(Users).get(user_id).google_cred is not None

def googleCalendarAPI_creds(authCode: str, redirect_uri: str) -> Credentials:
    flow = Flow.from_client_secrets_file(
        'app/client_secret_77701347155-oc5bqd2mfkof8oiukmg2hu6rkd4hqedt.apps.googleusercontent.com.json',
        scopes=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/userinfo.email',
            'openid',
            'https://www.googleapis.com/auth/userinfo.profile'
        ],
        redirect_uri=redirect_uri
    )
    flow.fetch_token(code=authCode, access_type='offline')
    return flow.credentials

def updateUserCredentials(user_id:int, credentials: Credentials):
    if user_id is False:
        return
    with SessionContext() as session:
        session.query(Users).get(user_id).google_cred = json.dumps({
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'id_token':credentials.id_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
            'expiry':dt.datetime.strftime(credentials.expiry,'%Y-%m-%d %H:%M:%S')
        })

def loadUserCredentials(user_id: int):
    with SessionContext() as session:
        cred_json = session.query(Users).get(user_id).google_cred
        if cred_json is None:
            return None
        credentials = Credentials(
            cred_json['token'],
            refresh_token=cred_json['refresh_token'],
            id_token=cred_json['id_token'],
            token_uri=cred_json['token_uri'],
            client_id=cred_json['client_id'],
            client_secret=cred_json['client_secret'],
            scopes=cred_json['scopes'],
        )
        credentials.expiry = dt.datetime.strptime(cred_json['expiry'], '%Y-%m-%d %H:%M:%S')
    if credentials.expired:
        credentials.refresh(google.auth.transport.requests.Request())
        updateUserCredentials(user_id, credentials)
    return credentials

def print_calendar_info(credentials):
    service = build('calendar', 'v3', credentials=credentials)
    print(type(service))
    print(service.events().list(calendarId='primary', singleEvents=True, orderBy='startTime').execute().get('items', []))
    events_list = []
    for item in service.calendarList().list().execute().get('items', []):
        events_list.extend(service.events().list(calendarId=item.get('id'), singleEvents=True, orderBy='startTime').execute().get('items', []))
    print(events_list)

def connect2Service(credentials: Credentials):
    return build('calendar', 'v3', credentials=credentials)

def save_calendar_id(user_id: int, credentials: Credentials):
    service = connect2Service(credentials)
    with SessionContext() as session:
        print(type(service))
        for item in service.calendarList().list().execute().get('items', []):
            session.add(UsersGoogleCalendar(
                user_id=user_id,
                calendar_id=item.get('id'),
                summary=item.get('summary'),
                description=item.get('description'),
                privacy_level=0
            ))

def change_calendar_privacy_level(user_id: int, c_id: int, privacy_level: int) -> bool:
    with SessionContext() as session:
        data = session.query(UsersGoogleCalendar).get(c_id)
        if data.user_id != user_id:
            return False
        data.privacy_level = privacy_level
    return True

def get_all_calendars(user_id: int):
    with SessionContext() as session:
        data = session.query(UsersGoogleCalendar).filter_by(user_id=user_id).all()
        # print([DBtoDict(d, ['user_id']) for d in data])
        data = [DBtoDict(d, ['user_id']) for d in data]
        return data
