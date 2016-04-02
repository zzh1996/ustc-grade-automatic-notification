from bs4 import BeautifulSoup
from newknn import Captcha
import urllib,urllib2,cookielib,os,zlib,time,getpass,sys
import mail

sourcemail='fydpfg1996@163.com'
sourcemailpassword=''
destmail='903806024@qq.com'

try:
    xuenian=sys.argv[1]
except:
    xuenian=20151
#userCode=raw_input("student no: ")
userCode='PB14011086'
passWord=getpass.getpass()

captcha = Captcha()
login=False

while not login:
 
    cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
    }
    req = urllib2.Request(
        url = 'http://mis.teach.ustc.edu.cn/',
        headers = headers
    )
    content = urllib2.urlopen(req).read()
    req = urllib2.Request(
        url = 'http://mis.teach.ustc.edu.cn/randomImage.do',
        headers = headers
    )
    content = urllib2.urlopen(req).read()

    check=captcha.hack(content)
    #print check

    postdata=urllib.urlencode({
        'userbz':'s',
        'hidjym':'',
        'userCode':userCode,
        'passWord':passWord,
        'check':check
    })

    req = urllib2.Request(
        url = 'http://mis.teach.ustc.edu.cn/login.do',
        data = postdata,
        headers = headers
    )
    result = urllib2.urlopen(req).read()

    error="<head><meta http-equiv='refresh' content='0; url=/userinit.do'></head>"

    if error in result:
        #print 'wrong code!'
        pass
    else:
        login=True 

postdata=urllib.urlencode({
    'xuenian': xuenian,
    'px': 1,
    'zd': 0
})

req = urllib2.Request(
    url = 'http://mis.teach.ustc.edu.cn/querycjxx.do',
    data = postdata,
    headers = headers
)

oldresult=""

while True:
    try:
        result = urllib2.urlopen(req).read()
        if result!=oldresult:
            #print result
            soup = BeautifulSoup(result, "html5lib")
            #for i,line in enumerate(soup.find_all('tr')):
            #    for j,elem in enumerate(line.find_all('td')):
            #        print 'line=',i,' row=',j,' ',elem.get_text().encode('utf-8')
            graderows=soup.find_all('tr')
            gpa=graderows[0].find_all('td')[9].get_text().strip().encode('utf-8')
            graderows=graderows[2:-1]
            count=len(graderows)
            print 'count =',count
            data=[]
            for row in graderows:
                elems=row.find_all('td')
                elems=[elems[x].get_text().encode('GBK') for x in [2,6,4]]
                data.append(elems)
            maxlen=max([len(x[0]) for x in data])
            msg=''
            for elems in data:
                msg+= (elems[0].ljust(maxlen)+'\t'+elems[1]+'\t'+elems[2]).decode('GBK').encode('utf-8')
                msg+='\n'
            mail.send_email(sourcemail,sourcemailpassword,destmail,(data[-1][0]+' '+data[-1][2]).decode('GBK').encode('utf-8'),msg)
        else:
            print "not changed , count =",count,", GPA =",gpa," ",time.strftime('%Y-%m-%d %X',time.localtime(time.time()))
        oldresult=result
        time.sleep(5)
    except:
        pass

