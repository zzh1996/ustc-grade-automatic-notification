# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
from newknn import Captcha
import random

weeks_name = dict(zip(range(1, 8), ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']))


def decode_place_time(mess):
    content = {}
    mess = mess.split(';')
    for item in mess:
        item = item.split(u'：')
        if len(item) < 2:
            return {}
        place = item[0]
        if item[1].startswith(u'单') or item[1].startswith(u'双'):
            other = item[1][0] + u'周'
            week = item[1][1]
        else:
            other = ''
            week = item[1][0]
        if item[1].find(u'晚上') != -1:
            classes = ['11']
        else:
            left = item[1].find('(')
            right = item[1].find(')')
            classes = item[1][left + 1: right].split(',')
        for i in classes:
            info = {
                'place': place,
                'week': week,
                'class_no': i,
                'other': other
                }
            content[len(content)] = info
    return content


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return d + timedelta(days_ahead)


def ical(classes, class_day_time, semester_date, semester):
    vcalendar = '''BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
X-LIC-LOCATION:Asia/Shanghai
BEGIN:STANDARD
TZOFFSETFROM:+0800
TZOFFSETTO:+0800
TZNAME:CST
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE
%s
END:VCALENDAR
'''
    event = '''BEGIN:VEVENT
DTSTART;TZID=Asia/Shanghai:%(class_firstday)sT%(class_start_time)s
DTEND;TZID=Asia/Shanghai:%(class_firstday)sT%(class_end_time)s
RRULE:FREQ=WEEKLY;UNTIL=%(semester_end_date)sT235900;BYDAY=%(class_week)s
DESCRIPTION:%(class_info)s
LOCATION:%(class_location)s
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:%(class_name)s
TRANSP:OPAQUE
END:VEVENT
'''
    events = ''
    for index, items in classes.iteritems():
        for i, item in items[u'上课时间地点'].iteritems():
            try:
                firstday = next_weekday(semester_date[semester][0],
                                    int(item['week']) - 1).strftime('%Y%m%d')
            except:
                continue
            info = {
                'class_firstday': firstday,
                'class_start_time': class_day_time[item['class_no']][0],
                'class_end_time': class_day_time[item['class_no']][1],
                'semester_end_date':
                    semester_date[semester][1].strftime('%Y%m%d'),
                'class_week': weeks_name[int(item['week'])],
                'class_info': ' '.join([items[u'教师'], item['other']]),
                'class_location': item['place'],
                'class_name': items[u'课程名称']
                }
            events += event % info
    vcalendar = vcalendar % events
    return vcalendar


class USTCMis:
    url = 'http://mis.teach.ustc.edu.cn/'
    class_day_time = {
        '1': ['075000', '083500'],
        '2': ['084000', '092500'],
        '3': ['094500', '103000'],
        '4': ['103500', '112000'],
        '5': ['112500', '121000'],
        '6': ['140000', '144500'],
        '7': ['145000', '153500'],
        '8': ['155500', '164000'],
        '9': ['164500', '173000'],
        '10': ['173500', '182000'],
        '11': ['193000', '201500'],
        '12': ['202000', '210500'],
        '13': ['211000', '215500']
        }
    semester_date = {
        '20121': [date(2012, 9, 3), date(2013, 1, 25)],
        '20122': [date(2013,2, 25), date(2013, 6, 28)],
        '20123': [date(2013, 7, 1), date(2013, 8, 9)],
        '20131': [date(2013, 9, 2), date(2014, 1, 17)],
        '20132': [date(2014, 2, 17), date(2014, 6, 20)],
        '20133': [date(2014, 6, 23), date(2014, 8, 1)],
        '20141': [date(2014, 9, 1), date(2015, 1, 30)],
        '20142': [date(2015, 3, 1), date(2015, 6, 21)]
        }

    captcha = Captcha()

    def __init__(self):
        self.s = requests.Session()
        self.login_status = False

    # Login
    def get_check_code(self):
        self.s.post(USTCMis.url + 'userinit.do', data={'userbz': 's'})
        r = self.s.get(USTCMis.url + 'randomImage.do')
        img = r.content
        return img

    def login(self, user_code, pwd):
        img = self.get_check_code()
        check_code = self.captcha.hack(img)
        login_info = {
            'userbz': 's',
            'hidjym': '',
            'userCode': user_code,
            'passWord': pwd,
            'check': check_code
            }
        self.s.post(USTCMis.url + 'login.do', data=login_info)
        self.check_login()
        if not self.login_status:
            filename = str(random.randint(1,1000)) + check_code + ".jpg"
            print filename
            with open(filename, 'w') as f:
                f.write(img)
        return self.login_status

    def check_login(self):
        r = self.s.get(USTCMis.url + 'init_xk_ts.do')
        self.login_status = (r.text.find(u'所在院系') != -1)
        return self.login_status

    # Grade
    def get_grade_semester_list(self):
        if not self.login_status or not self.check_login():
            return {'error': 'Not Login'}
        r = self.s.get(USTCMis.url + 'initquerycjxx.do')
        soup = BeautifulSoup(r.text)
        content = []
        options = soup.find_all('option')
        for i in options:
            content.append([i.attrs['value'], i.text])
        return content

    def get_grade(self, semester=''):
        if not self.login_status or not self.check_login():
            return {'error': 'Not Login'}
        query_data = {
            'xuenian': semester,
            'px': 1,
            'zd': 0
            }
        r = self.s.post(USTCMis.url + 'querycjxx.do', data=query_data)
        soup = BeautifulSoup(r.text)
        content = {}
        tables = [i.find_all('td') for i in soup.find_all('table')]
        basic = [i.string.strip() for i in tables[0]]
        content['basic'] = dict(zip(basic[::2], basic[1::2]))
        detail_key = [i.string.strip() for i in tables[1]]
        detail_item = [i.string.strip() for i in tables[2]]
        detail = {}
        for i in xrange(len(detail_item) / len(detail_key)):
            n = len(detail_key)
            item = detail_item[i * n: i * n + n]
            detail[i] = dict(zip(detail_key, item))
        content['detail'] = detail
        return content

    # Timetable
    def get_timetable_semester_list(self):
        if not self.login_status or not self.check_login():
            return {'error': 'Not Login'}
        r = self.s.get(USTCMis.url + 'initxkjgquery.do')
        soup = BeautifulSoup(r.text)
        content = []
        options = soup.find_all('option')
        for i in options:
            if len(i.attrs['value']):
                content.append([i.attrs['value'], i.text])
        return content

    def get_timetable(self, semester):
        if not self.login_status or not self.check_login():
            return {'error': 'Not Login'}
        query_data = {'selxnxq': semester}
        r = self.s.post(USTCMis.url + 'xkjgquery.do?tjfs=1', data=query_data)
        soup = BeautifulSoup(r.text)
        table = soup.find_all('table', id='jcxxtable0')[0]
        tds = [i.string.strip() for i in table.find_all('td')]
        info_key = tds[0:8]
        info_item = [tds[i:i + 8] for i in xrange(8, len(tds), 8)]
        classes = [dict(zip(info_key, item)) for item in info_item]
        content = dict(zip(range(len(info_item)), classes))
        for i in content.keys():
            mess = content[i][u'上课时间地点']
            content[i][u'上课时间地点'] = decode_place_time(mess)
        return content

    def get_ical(self, semester):
        if not self.login_status or not self.check_login():
            return 'error'
        classes = self.get_timetable(semester)
        return ical(classes, USTCMis.class_day_time, USTCMis.semester_date,
                    semester)

    # Class Operation
    def insert_class(self, param_str):
        param_key = ['tag', 'actionname', 'xnxq', 'kcid', 'kcbjbh', 'kclb',
                     'kcsx', 'sjpdm', 'kssjdm', 'cxck', 'zylx', 'gxkfl',
                     'xlh', 'qsz', 'jzz']
        param_list = param_str.split(',')
        param = dict(zip(param_key,param_list))
        data = {
            "xnxq": param.get('xnxq'),
            "kcbjbh": param.get('kcbjbh'),
            "kcid": param.get('kcid'),
            "kclb": param.get('kclb'),
            "kcsx": param.get('kcsx'),
            "cxck": param.get('cxck'),
            "zylx": param.get('zylx'),
            "gxkfl": param.get('gxkfl'),
            "xlh": param.get('xlh'),
            "sjpdm": param.get('sjpdm'),
            "kssjdm": param.get('kssjdm')
        }
        self.s.get(USTCMis.url + 'xkgcinsert.do',data=data)
