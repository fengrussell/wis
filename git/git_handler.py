# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing

    FileName: git_handler.py

    ProjectName: AttendanceCheckingSystem 

    Description:

    History:
    v1.0.0, hlj, 2016-05-16 11:38, Modify:

"""

#from pip.vcs import git

import os
import configparser
import datetime

# 从gitlab上pull(默认程序运行所在计算机与gitlab以配置好ssh)
def git_pull(repo_path):
    os.chdir(repo_path)
    os.system("git pull")

# 程序入口
if __name__ == '__main__':
    git_pull('C:/E/gitlab/Software.wiki')

