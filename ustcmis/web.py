# -*- coding: utf-8 -*-
from ustcmis import USTCMis
from flask import Flask, Blueprint, session, redirect, url_for, request, json,\
                    current_app, render_template
import random

app = Flask(__name__)
ustcmis = Blueprint('ustcmis', __name__, template_folder='templates',
                    static_folder='static', url_prefix='')
user = {}


@ustcmis.route('/')
def index():
    if 'id' in session:
        user_id = session['id']
    else:
        user_id = str(int(random.random() * 1e16))
        session['id'] = user_id
    if user_id not in user:
        user[user_id] = USTCMis()
    login = user[user_id].check_login()
    if not login:
        return render_template('index.html', login=login)
    else:
        grade_semester_list = user[user_id].get_grade_semester_list()
        timetable_semester_list = user[user_id].get_timetable_semester_list()
        return render_template('index.html', login=login, grade_semester_list=
                grade_semester_list, timetable_semester_list=timetable_semester_list)


@ustcmis.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'id' in session:
        user_id = session['id']
        if user_id not in user:
            return redirect(url_for('.login'))
        user_code = request.form['user_code']
        pwd = request.form['pwd']
        user[user_id].login(user_code, pwd)
    return redirect(url_for('.index'))


@ustcmis.route('/logout')
def logout():
    if 'id' in session:
        user_id = session['id']
        user.pop(user_id, None)
    session.clear()
    return redirect(url_for('.index'))


@ustcmis.route('/ical.ics', methods=['GET', 'POST'])
def get_ical():
    if check_login():
        try:
            semester = request.values['semester']
        except:
            semester = '20132'
        user_id = session['id']
        icalendar = user[user_id].get_ical(semester)
        if icalendar != 'error':
            return current_app.response_class(icalendar,
                                              mimetype='text/calendar')
    return json_return({'error': 'Not Login'})


# API
@ustcmis.route('/api/login', methods=['GET', 'POST'])
def api_login():
    if request.method == 'POST' and 'id' in session:
        user_id = session['id']
        if user_id not in user:
            return redirect(url_for('.login'))
        user_code = request.form['user_code']
        pwd = request.form['pwd']
        status = user[user_id].login(user_code, pwd)
        if status:
            return json_return({'user': user_code})
        else:
            return json_return({'error': 'Login Failed'})
    if 'id' in session:
        user_id = session['id']
    else:
        user_id = str(int(random.random() * 1e16))
    user[user_id] = USTCMis()
    session['id'] = user_id
    return json_return({'error': 'Not Login'})


@ustcmis.route('/api/grade', methods=['GET', 'POST'])
def api_get_grade():
    if check_login():
        try:
            semester = request.values['semester']
        except:
            semester = ''
        user_id = session['id']
        return json_return(user[user_id].get_grade(semester))
    return json_return({'error': 'Not Login'})


@ustcmis.route('/api/timetable', methods=['GET', 'POST'])
def api_get_timetable():
    if check_login():
        try:
            semester = request.values['semester']
        except:
            semester = '20132'
        user_id = session['id']
        return json_return(user[user_id].get_timetable(semester))
    return json_return({'error': 'Not Login'})


# else
def json_return(dict_variable):
    return current_app.response_class(json.dumps(dict_variable,
                    indent=2, ensure_ascii=False),
                    content_type='application/json; charset=utf-8')


def check_login():
    return 'id' in session and session['id'] in user \
        and user[session['id']].check_login()


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app.register_blueprint(ustcmis)

if __name__ == '__main__':
    app.debug = True
    app.run()
