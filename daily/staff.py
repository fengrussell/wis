# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing

    FileName:   staff.py

    ProjectName: wis

    Description: 员工，从原object.py文件把staff独立出来

    History:
    v1.0.0, russell, 2016-04-29 23:09, Modify:
    v1.0.1, hlj, 2016-05-13 09:09, Modify: 按PEP8修改编码风格

"""

import re

CHAR_STAR = '*'
CHAE_TILDE = '~'

class Staff:
    job_number = '' # 工号
    name = ''  # 姓名
    user_name = '' # gitlab上的帐号
    job_state = True # 是否在职

    project_list = []  # 项目列表(数组)
    project_dict = {}  # 项目字典

    err_project_list = [] # 不在项目列表中的项目名称

    def __init__(self, job_number, name, user_name, job_state=None):
        self.job_number = job_number
        self.name = name
        self.user_name = user_name

        if job_state is not None:
            self.job_state = job_state

        # 项目列表初始化为空
        self.project_list = []
        self.project_dict = {}
        self.err_project_list = []
    #        print("prjLen: " + str(len(self.prjList)))

    def update_project_data(self, prj):
        self.project_dict[prj.get_name()]

    def add_project_data(self, date, prj):
        self.project_list.append((date, prj))

    def add_error_project_data(self, date, prj):
        self.err_project_list.append((date, prj))

    def clear_project_data(self):
        self.project_list = []
        self.project_dict = {}
        self.err_project_list = []

    def to_log1(self):
        for t in self.project_list:
            print("%s %s %s %s" % (self.name, t[0], t[1].get_name(), t[1].get_time()))

    def to_error_log(self):
        for t in self.err_project_list:
            print("%s %s %s %s" % (self.name, t[0], t[1].get_name(), t[1].get_time()))

    def to_log(self, output_file):
        with open(output_file, 'a', encoding='utf-8') as out_file:
            for t in self.project_list:
                print("%s %s %s %s" % (self.name, t[0], t[1].get_name(), t[1].get_time()))
                out_file.write("%s %s %s %s\n" % (self.name, t[0], t[1].get_name(), t[1].get_time()))

    def data_to_file(self, output_file):
        with open(output_file, 'a', encoding='utf-8') as out_file:
            for t in self.project_list:
                # print("%s %s %s %s" % (self.name, t[0], t[1].get_name(), t[1].get_time()))
                out_file.write("%s %s %s %s %s\n" % (self.name, t[0], t[1].get_name(), t[1].get_time(), t[1].get_number()))

    def err_data_to_file(self, output_file):
        with open(output_file, 'a', encoding='utf-8') as out_file:
            for t in self.err_project_list:
                # print("%s %s %s %s" % (self.name, t[0], t[1].get_name(), t[1].get_time()))
                out_file.write("%s %s %s %s %s\n" % (self.name, t[0], t[1].get_name(), t[1].get_time(), t[1].get_number()))

    def get_records(self, begin_time, end_time):
        records = ''
        for entry in self.project_list:
            daily_date = entry.get_time()
        return records

    def to_staff_info(self):
        print('工号: %s , 姓名: %s , GitLab: %s , 是否在职: %s ' % (self.job_number, self.name, self.user_name, "是" if self.job_state else "否"))

    @staticmethod
    def is_job_num(num):
        """
        是否为工号
        :param num:
        :return:
        """
        an = re.match('^\d{6}$', num)
        if an:
            return True
        else: # 返回 None
            return False

    @staticmethod
    def strip_spec_char(str):
        """
        去掉特殊字符
        :param str:
        :return:
        """
        return str.strip().replace(CHAR_STAR, '').replace(CHAE_TILDE, '')

    @staticmethod
    def is_on_job(str):
        """
        是否在职
        :param str:
        :return:
        """
        if str.count(CHAR_STAR) > 0 or str.count(CHAE_TILDE) > 0:
            return False
        else:
            return True
