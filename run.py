import responder

import app.app as backapp
import app.googleapi as googleapi

api = responder.API(templates_dir='static')
api.add_route('/', static=True)

@api.route('/api/login')
async def login(req, resp):
    resp.media = backapp.login(await req.media())

@api.route('/api/signup')
async def signup(req, resp):
    resp.media = backapp.signup(await req.media())

@api.route('/api/loggedin')
async def logged_in(req, resp):
    resp.media = {
        'isValid': backapp.check_login((await req.media())['token'])
    }

@api.route('/api/username')
async def username(req, resp):
    resp.media = {
        'user_name': backapp.username(backapp.verify_user((await req.media())['token']))
    }

@api.route('/api/feedback')
async def feedback(req, resp):
    data = await req.media()
    user_id = backapp.verify_user(data['token'])
    feedback_id = backapp.setfeedback(user_id, data['feedback'])
    # twi.update_status(f'FEEDBACK({feedback_id}): user_id: {user_id if user_id is not False else -1}, comment: {data["feedback"]}')

@api.route('/api/message')
async def message(req, resp):
    resp.media = {
        'msg': backapp.unreadmessage(backapp.verify_user((await req.media())['token']))
    }

@api.route('/api/validhashid/{hash_type}')
async def validhashid(req, resp, *, hash_type):
    resp.media = {
        'type': hash_type,
        'data': getattr(backapp, f'validID_{hash_type}')(backapp.verify_user((await req.media())['token']))
    }

@api.route('/auth/hasgoogle')
async def hasgoogle(req, resp):
    user_id = backapp.verify_user((await req.media())['token'])
    resp.media = {
        'isValid': user_id is not False and googleapi.hasCredentials(user_id)
    }

@api.route('/auth/googlecalendar')
async def googlecalendar(req, resp):
    data = await req.media()
    credentials = googleapi.googleCalendarAPI_creds(data['code'], data['redirect_uri'])
    @api.background.task
    def cred2db(user_id, credentials: googleapi.Credentials):
        googleapi.updateUserCredentials(user_id, credentials)
        googleapi.save_calendar_id(user_id, credentials)
        googleapi.print_calendar_info(credentials)
    cred2db(backapp.verify_user(data['token']), credentials)
    resp.media = {
        'success': True
    }

@api.route('/google/getmycalendars')
async def getmycalendars(req, resp):
    resp.media = {
        'calendarList': googleapi.get_all_calendars(backapp.verify_user((await req.media())['token']))
    }

@api.route('/setting/calendarprivacylevel')
async def calendarprivacylevel(req, resp):
    data = await req.media()
    resp.media = {
        'isValid': googleapi.change_calendar_privacy_level(
            backapp.verify_user(data['token']),
            data['c_id'],
            data['new_level']
        )
    }

if __name__ == "__main__":
    api.run(port=8080)
