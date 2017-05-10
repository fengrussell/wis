# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing

    FileName:   project.py

    ProjectName: wis

    Description: 项目，从原object.py文件把staff独立出来

    History:
    v1.0.0, russell, 2016-04-29 23:09, Modify:
    v1.0.1, hlj, 2016-05-13 09:09, Modify: 按PEP8修改编码风格

"""

class Project:
    name = ''  # 项目名称
    time = 0.0  # 工时
    number = ''

    def __init__(self, name, time):
        self.name = name
        self.time = time

    def get_name(self):
        return self.name

    def get_time(self):
        return self.time

    def add_time(self, time):
        self.time = self.time + time

    def set_number(self, number):
        self.number = number

    def get_number(self):
        return self.number

    @staticmethod
    def strip_spec_char(str):
        # 在wiki页面里的项目名称定义方式有多种，需要处理一下
        tstr = str.strip().replace('*', '').replace('`', '')
        if (tstr.startswith('[')):
            idx = tstr.find(']')
            if idx != -1:
                return tstr[1:idx]
        return tstr

