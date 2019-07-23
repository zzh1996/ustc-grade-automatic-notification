# ustc-grade-automatic-notification

USTC 成绩自动通知脚本

# 由于教务系统已经更换成新系统，此项目不再适用并停止维护，大家有兴趣可以针对新系统开发功能类似的脚本

### 简介

这是一个针对中国科学技术大学本科生教务系统（[mis.teach.ustc.edu.cn](http://mis.teach.ustc.edu.cn/)）的成绩查询脚本，可以自动登录教务系统（验证码使用图像识别技术自动输入，基于 zhsj 的 [项目](https://github.com/zhsj/ustcmis)）并定时查询成绩，若新出成绩则以邮件形式发送给用户。

邮件的标题和内容均为[学科名称]+[成绩]。

使用用户名密码登录，而不是用 cookie，是因为教务系统服务器经常出问题，宕机十多分钟就会导致 cookie 失效。

本程序未经严格测试，不保证提供服务的稳定性。

### 使用方法（以 Ubuntu 16.04.3 LTS 为例）

1、安装 git 并下载代码

```shell
sudo apt update
sudo apt install git -y
git clone https://github.com/zzh1996/ustc-grade-automatic-notification.git
```

2、安装必要的库

```shell
sudo apt install python python-bs4 python-numpy python-opencv python-html5lib vim -y
```

3、修改配置文件

```shell
cd ustc-grade-automatic-notification
cp config_example.py config.py
vim config.py
```

配置文件中各个参数的含义请参考每行后面的注释

4、运行

```
./grade.py
```

运行后会询问用户是否要发送一封测试邮件，输入 y 并回车可以发送测试邮件。

如果在服务器上运行，为了保证 ssh 断开后脚本仍在运行，请使用 tmux 或 screen。

### 使用 Docker 部署

假设已经安装了 Docker

1、在一个空目录中，放入本项目的 `Dockerfile`。

2、将本项目的 `config_example.py` 按照需求修改好，命名为 `config.py`，并且和 `Dockerfile` 放在同一个目录下。

3、在这个目录下，运行 `docker build -t grade .`。

4、运行 `docker run -it grade` 启动脚本。

### 已知问题

1、暂时没加识别学号或密码错误的部分，如果发现程序反复尝试登录而且一直失败，请检查学号和密码是否错误。

2、若使用 163、QQ 等邮箱的 smtp 发信，请在邮箱的设置页面开启 smtp 服务。

3、如果邮件被当作垃圾邮件，请自行加白名单。

4、某些网络环境禁止了 smtp 协议的端口，可以尝试开启 SSL。

### 反馈 bug

开 issue 或发邮件至 `zzh1996@科大学生邮箱`
