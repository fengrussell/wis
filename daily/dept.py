# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing

    FileName:   dept.py

    ProjectName: wis

    Description: 部门

    History:
    v1.0.0, russell, 2016-07-23 19:25, Modify:

"""

import re

class Department:
    name = '' # 部门名称
    prj_name = '' # gitlab项目的名称
    git_root_path = '' # git根路径
    out_root_path = '' # 输出的根路径

    def __init__(self, name, prj_name, git_root_path, out_root_path):
        self.name = name
        self.prj_name = prj_name
        self.git_root_path = git_root_path
        self.out_root_path = out_root_path

    def get_name(self):
        return self.name

    def get_prj_name(self):
        return self.prj_name

    def get_gitlab_wiki_name(self):
        return self.prj_name + ".wiki"

    def get_git_path(self):
        """
        返回部门对应的工作日志目录，带了末尾的路径分隔符
        :return:
        """
        return self.git_root_path + "/" + self.get_gitlab_wiki_name() + "/"

    def get_out_path(self):
        """
        返回日志输出目录
        :return:
        """
        return self.out_root_path + "/" + self.name + "/"

    def get_staff_list_file(self):
        # return self.get_out_path() + "work_record.md"
        return self.get_git_path() + "work_record.md"

