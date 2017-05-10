# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing

    FileName: time_util.py

    ProjectName: wis 

    Description: 时间工具类

    History:
    v1.0.0, russell, 2016-05-28 18:38, Created:

"""

import os
import datetime
import time
import calendar
import math


def format_date(date, format=None):
    """
    格式化为指定格式的日期
    日期必须为datetime类型，不输入format参数，默认格式为YYYYMMDD
    """
    if format is None:
        format = '%Y%m%d'
    return date.strftime(format)

def fromat_date(str_date, src_format, dst_format):
    return datetime.datetime.strptime(str_date, src_format).strftime(dst_format)

def today_date(format=None):
    """
    当天的日期
    """
    if format is not None:
        return datetime.datetime.now().strftime(format)
    else:
        return datetime.datetime.now().strftime('%Y%m%d')

def current_time(format=None):
    """
    返回当前时间
    :param format:
    :return:
    """
    if format is not None:
        return datetime.datetime.now().strftime(format)
    else:
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

def add_days_from_date(days, str_date=None, format=None):
    """
    从一个日期增加天数（可以是负数）得到一个新的日期（字符串）
    :param days: 天数
    :param str_date: 字符串的日期
    :param format: 日期格式
    :return:
    """
    if format is None:
        format = "%Y%m%d"
    if str_date is None:
        str_date = today_date()

    temp_date = datetime.datetime.strptime(str_date, format) + datetime.timedelta(days)
    return temp_date.strftime(format)

def monday_sunday(date=None):
    """
    指定日期所在周的周一和周日的日期，没有指定date就是当前日期
    """
    if date is None:
        date = today_date()
    # 当前日期
    tdate = datetime.datetime.strptime(date, "%Y%m%d")
    # 当前日期和周一的天数，0是周一，6是周日
    monday = tdate - datetime.timedelta(tdate.weekday())
    sunday = tdate + datetime.timedelta(6 - tdate.weekday())
    return format_date(monday), format_date(sunday)


def lastweek_monday_sunday(date=None):
    """
    指定日期上周的周一和周日的日期，没有指定date就是当前日期
    """
    if date is None:
        date = today_date()
    # 减去7天到上周的日期
    ldate = datetime.datetime.strptime(date, "%Y%m%d") - datetime.timedelta(7)
    # ldate是datetime类型，需要转成字符串
    return monday_sunday(format_date(ldate))


def month_1thday_lasday(date=None):
    """
    返回指定日期所在月的第一天和最后一天的日期
    date没有输入则是当前月，date格式为yyyymmddd，其他格式目前不支持
    """
    if date is None:
        date = today_date()
    tdate = datetime.datetime.strptime(date, "%Y%m%d")
    # day_now = time.localtime()
    day_begin = '%d%02d01' % (tdate.year, tdate.month)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(tdate.year, tdate.month)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d%02d%02d' % (tdate.year, tdate.month, monthRange)
    return day_begin, day_end
    # print('月初日期为：',day_begin, '月末日期为：',day_end)

def _add_month_interval (dt, inter):
    m=dt.month+inter-1
    print("--------------\n")
    print(m)
    print("--------------\n")
    y=dt.year+math.floor(m/12)
    m=m % 12 +1
    return (y,m)

def add_month_interval (date, inter):
    """
    按照指定日期，增加/减去月份的结果
    :param date: 日期  datetime类型
    :param inter: 间隔，支持负值
    :return:
    """
    y,m =_add_month_interval(date, inter)
    y2, m2 = _add_month_interval(date, inter+1)
    maxD = ( datetime.date(y2, m2, 1)-datetime.timedelta(days=1) ).day
    d = date.day <= maxD and date.day or maxD
    return datetime.date(y, m, d)

def add_year_interval (date, inter):
    """
    按照指定日期，增加/减去年份的结果
    :param date: 日期  datetime类型
    :param inter: 间隔，支持负值
    :return:
    """
    return add_month_interval(date, inter*12)

def lastmonth_1thday_lasday(date=None):
    if date is None:
        date = today_date()
    last_month_date = add_month_interval(datetime.datetime.strptime(date, "%Y%m%d"), -1).strftime('%Y%m%d')
    return month_1thday_lasday(last_month_date)

def get_month_list_by_date(begin_date, end_date):
    """
    通过起止日期返回月份列表
    """
    month_list = []
    tbegin_date = datetime.datetime.strptime(begin_date, "%Y%m%d")
    tend_date = datetime.datetime.strptime(end_date, "%Y%m%d")
    while (tbegin_date.year < tend_date.year) or (tbegin_date.year == tend_date.year and tbegin_date.month <= tend_date.month):
        month_list.append("%d%02d" % (tbegin_date.year, tbegin_date.month))
        tbegin_date = add_month_interval(tbegin_date, 1)
    return  month_list

def get_year_month(date):
    temp_date = datetime.datetime.strptime(date, "%Y%m%d")
    return "%d%02d" % (temp_date.year, temp_date.month)


# 程序入口
if __name__ == '__main__':
    print()
    # print(today_date())
    # i = datetime.datetime.now()
    # print ("本周第 %u " % i.weekday() + "天")
    # print(monday_sunday())
    # print(lastweek_monday_sunday())
    # print(month_1thday_lasday("20160201"))

    # mlist = get_month_list_by_date("20160501", "20160531")
    # for m in mlist:
    #     print(m)

    # print(lastmonth_1thday_lasday("20160201"))

    # print(current_time())
    #
    # print(get_year_month("20150611"))
    #
    # print(fromat_date('20150611', '%Y%m%d', '%Y.%m.%d'))

    # print(add_days_from_date(1, '2015.06.06', "%Y.%m.%d"))


