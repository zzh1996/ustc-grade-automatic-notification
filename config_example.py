#!/usr/bin/env python
# -*- coding: utf-8 -*-

enable_mail = True  # 此行表示是否发送邮件提醒，设置为 True 发邮件
smtp_server = 'smtp.163.com'  # 此行表示 smtp 服务器地址
smtp_username = 'xxx@163.com'  # 此行表示发件人邮箱地址
smtp_password = 'xxx'  # 此行表示发件人邮箱密码
smtp_to = 'xxx@163.com'  # 此行表示收件人邮箱地址
smtp_ssl = False  # 此行表示连接邮箱是否使用 SSL

student_no = 'PBxxxxxxxx'  # 此行表示登录教务系统所用学号
ustcmis_password = 'xxx'  # 此行表示教务系统密码（不是统一身份验证密码）

req_timeout = 10  # 此行表示向教务系统发查询请求的超时时间（单位：秒）
interval = 60  # 此行表示两次查询的间隔时间（单位：秒）
