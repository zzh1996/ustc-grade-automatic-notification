# ustc-grade-automatic-notification

USTC成绩自动通知脚本

### 简介

这是一个针对中国科学技术大学本科生教务系统（[mis.teach.ustc.edu.cn](http://mis.teach.ustc.edu.cn/)）的成绩查询脚本，可以自动登录教务系统（验证码使用图像识别技术自动输入，基于zhsj的[项目](https://github.com/zhsj/ustcmis)）并定时查询成绩，若新出成绩则以邮件形式发送给用户。

邮件的标题和内容均为[学科名称]+[成绩]。

使用用户名密码登录，而不是用cookie，是因为教务系统服务器经常出问题，宕机十多分钟就会导致cookie失效。

本程序未经严格测试，不保证提供服务的稳定性。

### 使用方法（以Ubuntu为例）

1、安装git并下载代码

```shell
sudo apt update
sudo apt install git -y
git clone https://github.com/zzh1996/ustc-grade-automatic-notification.git
```

2、安装必要的库

```shell
sudo apt install python python-bs4 python-numpy python-opencv -y
```

3、修改配置文件

```shell
cd ustc-grade-automatic-notification
cp config.py.example config.py
vim config.py
```

配置文件内容：

```
enable_mail = True #此行表示是否发送邮件提醒，设置为True发邮件
smtp_server = 'smtp.163.com' #此行表示smtp服务器地址
smtp_username = 'xxx@163.com' #此行表示发件人邮箱地址
smtp_password = 'xxx' #此行表示发件人邮箱密码
smtp_to = 'xxx@163.com' #此行表示收件人邮箱地址

student_no = 'PBxxxxxxxx' #此行表示登录教务系统所用学号
ustcmis_password = 'xxx' #此行表示教务系统密码
semester = '20152' #此行表示学期，例如20152表示2016春季学期（即2015~2016学年第二学期），如需查询所有学期成绩，请改为空字符串
```

4、运行

```
./grade.py
```

如果在服务器上运行，为了保证ssh断开后脚本仍在运行，请使用tmux或screen。

### 已知问题

1、暂时没加识别学号或密码错误的部分，如果发现程序反复尝试登录而且一直失败，请检查学号和密码是否错误。

2、未将查询间隔加入配置文件，如需修改两次查询的间隔，请修改`grade.py`最后一行，将其中的`5`改为其他数值（单位：秒）。

3、若使用163、QQ等邮箱的smtp发信，请在邮箱的设置页面开启smtp服务。

4、查成绩前请先进行教学评估。

5、如果邮件被当作垃圾邮件，请自行加白名单。

### 反馈bug

请发邮件至`zzh1996@科大学生邮箱`

