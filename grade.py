#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from newknn import Captcha
import urllib, urllib2, cookielib, os, zlib, time, getpass, sys
from mail import send_email
from config import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
}
cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)


def login():
    captcha = Captcha()
    has_login = False
    while not has_login:
        print 'Trying to login...'
        req = urllib2.Request(
            url='http://mis.teach.ustc.edu.cn/',
            headers=headers
        )
        urllib2.urlopen(req, timeout=req_timeout).read()
        req = urllib2.Request(
            url='http://mis.teach.ustc.edu.cn/randomImage.do',
            headers=headers
        )
        content = urllib2.urlopen(req, timeout=req_timeout).read()
        code = captcha.hack(content)
        print 'Recognized captcha code:', code
        postdata = urllib.urlencode({
            'userbz': 's',
            'hidjym': '',
            'userCode': student_no,
            'passWord': ustcmis_password,
            'check': code
        })
        req = urllib2.Request(
            url='http://mis.teach.ustc.edu.cn/login.do',
            data=postdata,
            headers=headers
        )
        result = urllib2.urlopen(req, timeout=req_timeout).read()
        # print result
        if "alert" in result:
            print 'Login incorrect!'
        else:
            has_login = True
            print 'Login OK!'


def get_grade():
    req = urllib2.Request(
        url='http://mis.teach.ustc.edu.cn/initfqcjxx.do?tjfs=1',
        headers=headers
    )
    return urllib2.urlopen(req, timeout=req_timeout).read()


def parse_grade(grade):
    soup = BeautifulSoup(grade, "html5lib")
    # for i,line in enumerate(soup.find_all('tr')):
    #    for j,elem in enumerate(line.find_all('td')):
    #        print 'line=',i,' row=',j,' ',elem.get_text().encode('utf-8')
    flag = 0
    rows = soup.find_all('tr')
    data = []
    for row in rows:
        elems = row.find_all('td')
        if len(elems) == 7:
            if flag:
                data.append([td.get_text() for td in elems])
            flag = 1
    return data


olddata = []
first_run = True
while True:
    print 'Query...'
    try:
        grade = get_grade()
        if "userinit" in grade:
            print 'Not login.'
            login()
            continue
        data = parse_grade(grade)
        print time.strftime('%Y-%m-%d %X', time.localtime(time.time())), 'Count :', len(data)
        test_mail = False
        if first_run:
            ans = raw_input('Send test email? (y/n)')
            if ans.lower() in ['', 'y', 'yes']:
                test_mail = True
        if len(data) != len(olddata) and not first_run or test_mail:
            text = ' , '.join(row[2] + ' ' + row[3] for row in data if row not in olddata)
            if test_mail:
                text = 'Test email. ' + text
            print 'Sending mail...'
            print 'Text:', text.encode('utf8')
            if enable_mail:
                send_email(text, text.encode('utf-8'))
            print 'Mail sent.'
        olddata = data
        first_run = False
    except Exception as e:
        if not isinstance(e, KeyboardInterrupt):
            print time.strftime('%Y-%m-%d %X', time.localtime(time.time())), 'Error:', str(e)
        else:
            break
    time.sleep(interval)
