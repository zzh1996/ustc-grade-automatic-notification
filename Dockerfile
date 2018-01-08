FROM ubuntu
RUN sudo sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt update && apt install python python-bs4 python-numpy python-opencv python-html5lib vim git -y && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/zzh1996/ustc-grade-automatic-notification.git
WORKDIR ustc-grade-automatic-notification
ADD config.py config.py
ENTRYPOINT ./grade.py
