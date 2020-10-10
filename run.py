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
    @api.background.task
    def sendVerificationEmail(user_id):
        # ユーザのメアドに確認のメールを送る
        # これが完了するまではユーザはtmpに登録しておく
        pass
    if resp.media['isValid']:
        sendVerificationEmail(backapp.verify_user(resp.media['token']))

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

@api.route('/api/validhashid/{hash_types}')
async def validhashid(req, resp, *, hash_types):
    user_id = backapp.verify_user((await req.media())['token'])
    if hash_types == 'all':
        hash_types = '-'.join(backapp.accessType)
    resp.media = [{
        'type': t,
        'data': getattr(backapp, f'validID_{t}')(user_id)
    } for t in hash_types.split('-')]

@api.route('/api/fetchaccessinfo')
async def fetchaccessinfo(req, resp):
    data = await req.media()
    hashdata = backapp.decodeHashID(data['accesshash'])
    if data['accesshash'] in getattr(backapp, f'validID_{hashdata["access_type"]}')(backapp.verify_user(data['token'])):
        accessinfo = getattr(backapp, f'get_{hashdata["access_type"]}')(hashdata['ids'], 0)
        resp.media = {
            'icon': accessinfo['icon'],
            'name': accessinfo[f'{hashdata["access_type"]}_name'],
        }
        if hashdata["access_type"] == 'user':
            resp.media['name'] = accessinfo['nick_name']
            resp.media['description'] = f'@{accessinfo["user_name"]}'
            for k in ['user_name', 'real_name', 'email', 'phone_number', 'zipcode', 'address']:
                resp.media[k] = accessinfo[k]
        elif hashdata["access_type"] == 'project':
            company = backapp.decodeHashID(accessinfo['company_id'])
            if company['access_type'] == 'user':
                resp.media['description'] = 'Private'
            else:
                resp.media['description'] = backapp.get_company(company['ids'], 100)['company_name']
            resp.media['tree'] = accessinfo['tree']

@api.route('/api/createcompany')
async def createcompany(req, resp):
    data = await req.media()
    data['admin'] = backapp.verify_user(data.pop('token'))
    data['sub_admin'] = [backapp.decodeHashID(e)['ids'] for e in data['sub_admin']]
    data['members'] = [backapp.decodeHashID(e)['ids'] for e in data['members']]
    data.setdefault('icon', '/static/usericons/default.png')
    resp.media = {
        'isValid': True,
        'accesshash': backapp.add_company(data)
    }

@api.route('/api/createproject')
async def createproject(req, resp):
    data = await req.media()
    data['admin'] = backapp.verify_user(data.pop('token'))
    data['sub_admin'] = []
    data['members'] = [backapp.decodeHashID(e)['ids'] for e in data['members']]
    data.setdefault('icon', '/static/usericons/default.png')
    data['company_id'] = data['tree'].split('/')[0]
    if data['company_id'] == 'private':
        data['company_id'] = backapp.generateHashID(data['admin'], 'user')
    resp.media = {
        'isValid': True,
        'accesshash': backapp.add_project(data)
    }

@api.route('/api/assign')
async def assign(req, resp):
    data = await req.media()
    hashdata = backapp.decodeHashID(data['accesshash'])
    resp.media = {
        'isValid': getattr(backapp, f'add_member2{hashdata["access_type"]}')(hashdata['ids'], backapp.verify_user(data['token']))
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
