# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing.

    FileName:   dairy_parser.py

    ProjectName: AttendanceCheckingSystem

    Description: 日报解析器

    History:
    v1.0.0, russell, 2016-04-29 23:09, Modify:
    v1.0.1, hlj, 2016-05-13 09:09, Modify: 按PEP8修改编码风格
"""

import os
import datetime

from conf.conf import Config
from daily.project import Project

def parse_dairy(dairy_file, config_info, begin_date=None, end_date=None):
    """
    解析日报，生成一定格式的数据文件，不符合格式的记录同时记录到一个文件里
    格式为：
    :dairy_file:
    :config_info:
    :return:
    """
    # 通过dairy_file获取员工的帐号
    username = parse_user_name(dairy_file, config_info.file_postfix)
    staff = config_info.staff_list.get(username)
    if staff is None:
        print("GitLab帐号 %s 不存在" % username)
        return

    with open(dairy_file, 'rb') as daily_record_file:
        daily_date = ''
        count = 0
        is_rational_date = False # 是否是合理的日期
        for line in daily_record_file.readlines():
            # 解析日期
            is_date, temp_dairy_date = parse_dairy_date(line)
            if is_date: # 是日期
                if is_in_date_range(temp_dairy_date, begin_date, end_date):  # 如果是日期，且在有效的范围日期内
                    is_rational_date = True
                    daily_date = temp_dairy_date
                else:
                    is_rational_date = False
                    daily_date = temp_dairy_date

            # 解析项目
            is_project, temp_project = parse_project(line)
            if is_rational_date and is_project: # 合理的日期，且是项目
                number = config_info.project_list.get(temp_project.name)
                if number is not None:
                    temp_project.set_number(number)
                    staff.add_project_data(daily_date, temp_project)
                else:
                    # print("err project name: %s " % temp_project.name)
                    staff.add_error_project_data(daily_date, temp_project)

             # staff.to_log(output_file)
#            tempLine = line.strip().decode()
#            print(tempLine)


def parse_user_name(dairy_file, postfix):
    """
    从文件名中获取员工的user_name
    :param dairy_file:
    :param postfix:
    :return:
    """
    filename = os.path.basename(dairy_file)
    staff_name = filename.replace(postfix, '').split('_')[2]
    if staff_name.__sizeof__():
        return staff_name
    else:
        print('failed to get user_name in %s!' % dairy_file)

def parse_dairy_date(line):
    """
    解析日报中的日期
    :param line:
    :return:
    """
    temp_line = line.strip().decode()
    if temp_line.startswith("##"):
        temp_line = temp_line[2:].strip()
        if temp_line.startswith("**") and temp_line.endswith("**"):
            temp_line = temp_line[2:-2]
            date = is_valid_date(temp_line)
            if date[0]:
                return True, date[1]
        else:
            return False, ''
    return False, ''


def parse_project(line):
    """
    解析项目名称
    """
    temp_line = line.strip().decode()
    if (temp_line.startswith("*") or temp_line.startswith("+") or temp_line.startswith("-")) and temp_line.endswith("**"):
        temp_line = temp_line[1:-2].strip()

        if temp_line.startswith("**") and temp_line.lower().endswith("h]"):
            temp_line = temp_line[2:-2]
            idx = temp_line.rfind("[")
#            print(tempLine[:idx].strip())
#            print(tempLine[(idx+1):])
            return True, Project(temp_line[:idx].strip(), temp_line[(idx+1):])
        else:
            return False, ''
    else:
        return False, ''

def is_in_date_range(date, begin_date, end_date):
    """
    是否在有效的日期范围内
    """
    if begin_date is not None and end_date is not None:
        if (datetime.datetime.strptime(date, "%Y.%m.%d") >= datetime.datetime.strptime(begin_date, "%Y.%m.%d")) and (datetime.datetime.strptime(date, "%Y.%m.%d") <= datetime.datetime.strptime(end_date, "%Y.%m.%d")):
            return True
        else:
            return False
    elif begin_date is not None:
        if (datetime.datetime.strptime(date, "%Y.%m.%d") < datetime.datetime.strptime(begin_date, "%Y.%m.%d")):
            return False
        else:
            return True
    elif end_date is not None:
        if (datetime.datetime.strptime(date, "%Y.%m.%d") > datetime.datetime.strptime(end_date, "%Y.%m.%d")):
            return False
        else:
            return True
    else:
        return True


def is_valid_date(str):
    """
    判断是否是一个有效的日期字符串，格式为yyyy.mm.dd
    """
    try:
        date = datetime.datetime.strptime(str, "%Y.%m.%d")
#        print(date.strftime("%Y.%m.%d"))
        return True, date.strftime("%Y.%m.%d")
    except:
        return False,

# 程序入口
if __name__ == '__main__':
    print(is_in_date_range('2015.01.03', None, '2015.01.03'))
