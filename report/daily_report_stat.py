# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing

    FileName: daily_report_stat.py

    ProjectName: wis 

    Description: 日报统计

    History:
    v1.0.0, russell, 2016-05-28 17:14, Created:

"""

import datetime
import os
import sys
print(sys.path)
sys.path.append('/data1/workgit/wis/')
print(sys.path)

from util.file_util import *
from conf.conf import Config
from util.time_util import get_month_list_by_date
from util.time_util import current_time
from util.time_util import get_year_month
from util.time_util import month_1thday_lasday
from util.time_util import fromat_date
from util.time_util import add_days_from_date
from util.time_util import lastweek_monday_sunday
from util.time_util import add_month_interval

from daily.dairy_parser import parse_dairy
from daily.dept import Department

from git.git_handler import git_pull

REPORT_PREFIX = "daily_report"

def dotted_quad_date(date):
    """
    转化为点分制的日期格式
    :param date:
    :return:
    """
    return fromat_date(date, '%Y%m%d', '%Y.%m.%d')

def month_report(config, date, dept):
    """
    月报
    :param date:
    :param dept:
    :return:
    """
    print("1111111111111\n")
    print(date)
    curr_time = current_time()
    data_file = config.data_output_path + "/" + dept.get_name() + "_m_" + get_year_month(date) +  "." +  curr_time # 生成月报的文件名
    err_data_file = config.data_output_path + "/" + dept.get_name() + "_err_m_" + get_year_month(date) +  "." +  curr_time # 生成月报的文件名

    begin_date, end_date = month_1thday_lasday(date)

    daily_file_list = []
    month_list = get_month_list_by_date(begin_date, end_date)

    for month in month_list:
        daily_file_list.extend(scan_files(config.daily_input_path, config.file_prefix, '_' + month + config.file_postfix))

    for file in daily_file_list:
        parse_dairy(file, config, dotted_quad_date(begin_date), dotted_quad_date(end_date))

    config.staff_data_to_file(data_file, err_data_file)

def week_report(config, begin_date, end_date, dept):
    """
    周报
    :param config:
    :param begin_date:
    :param end_date:
    :param dept:
    :return:
    """
    curr_time = current_time()
    data_file = config.data_output_path + "/" + dept.get_name() + "_w_" + begin_date + "_" + end_date + "." +  curr_time # 生成月报的文件名
    err_data_file = config.data_output_path + "/" + dept.get_name() + "_err_w_" + begin_date + "_" + end_date + "." +  curr_time # 生成月报的文件名

    daily_file_list = []
    month_list = get_month_list_by_date(begin_date, end_date)

    for month in month_list:
        daily_file_list.extend(scan_files(config.daily_input_path, config.file_prefix, '_' + month + config.file_postfix))

    for file in daily_file_list:
        parse_dairy(file, config, dotted_quad_date(begin_date), dotted_quad_date(end_date))

    config.staff_data_to_file(data_file, err_data_file)

def day_report(config, date, dept):
    """
    日报
    :param config:
    :param date:
    :param dept: 部门
    :return:
    """
    curr_time = current_time()
    data_file = config.data_output_path + "/" + dept.get_name() + "_d_" + date + "." +  curr_time # 生成月报的文件名
    err_data_file = config.data_output_path + "/" + dept.get_name() + "_err_d_" + date + "." +  curr_time # 生成月报的文件名

    daily_file_list = []
    month_list = get_month_list_by_date(date, date)

    for month in month_list:
        daily_file_list.extend(scan_files(config.daily_input_path, config.file_prefix, '_' + month + config.file_postfix))

    for file in daily_file_list:
        parse_dairy(file, config, dotted_quad_date(date), dotted_quad_date(date))

    config.staff_data_to_file(data_file, err_data_file)


def gen_daily_report(dept):

    # git更新
    cwd_path = os.getcwd()
    git_pull(dept.get_git_path())

    # git_pull 改变了工作路径，切换回来，否则读不到配置文件
    os.chdir(cwd_path)

    config = Config("../conf/wis.conf")
    config.load_config()

    # 根据部门参数对config的参数赋值
    config.daily_input_path = dept.get_git_path()
    config.data_output_path = dept.get_out_path()
    config.staff_list_file = dept.get_staff_list_file()

    # 加载数据
    config.load_staff_list()
    config.load_project_list()

   
    now = datetime.datetime.now()
    now_day = now.day
    now_weekday = now.weekday()
   
    #day_report(config, "20160722", dept)
    
    #month_report(config, "20161231",dept)

    # 触发统计报表数据
    # 日报，今天生成前天的数据，本来考虑到周一要特殊处理，要生成周五的数据。目前的逻辑是不处理，日报就是处理昨天的数据。
    #print("生成日报")
    #config.clear_staff_project_data()
    #day_report(config, add_days_from_date(-1),dept)
    
    # 周报，周一生成上周周报
    #if now_weekday == 0:
    #    print("生成周报")
    #    config.clear_staff_project_data()
    #    begin_date, end_date = lastweek_monday_sunday()
    #    week_report(config, begin_date, end_date, dept)
    
    # 月报，每月1号开始统计    
    if now_day == 4:
        print("生成月报")
        config.clear_staff_project_data()
        month_report(config, add_month_interval(now, -1).strftime('%Y%m%d'), dept)


# 程序入口
if __name__ == '__main__':
    git_root_path = '/data1/workgit' 
    out_root_path = '/data1/repo/daily'
    dept_list = [Department('软件部','Software', git_root_path, out_root_path)]

    for dept in dept_list:
        print(dept.get_name(), dept.get_git_path())
        gen_daily_report(dept)
