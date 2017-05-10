# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing

    FileName: conf.py

    ProjectName: wis 

    Description: 配置信息

    History:
    v1.0.0, russell, 2016-05-28 17:29, Created:

"""
import os
import  configparser
import re
from daily.project import Project

from daily.staff import Staff

class Config:
    # 配置文件
    config_file = 'wis.conf'
    # 日报输入路径
    daily_input_path = ''
    # 日志路径
    log_path = ''
    # 文件名前缀
    file_prefix = ''
    # 文件名后缀
    file_postfix = ''
    # 数据输出路径
    data_output_path = ''
    # 日期格式yyyymmdd
    #date_format = datetime.datetime.now().strftime('%Y%m%d')
    # 项目列表文件
    project_list_file = ''
    # 人员列表文件
    staff_list_file = ''

    # 项目列表（字典）
    project_list = {}
    # 人员列表（字典）
    staff_list = {}

    def __init__(self, config_file=None):
        if config_file is not None:
            self.config_file = config_file

    """
    加载配置wis.conf文件
    """
    def load_config(self):
        # 清空一下数据
        project_list = {}
        staff_list = {}

        config = configparser.ConfigParser()
        print(os.getcwd())
        print("self.config_file: " + self.config_file)
        config.read(self.config_file)
        # self.daily_input_path = config.get('global', 'daily_input_path') # 改成其他参数赋值
        self.file_prefix = config.get('global', 'file_prefix')
        self.file_postfix = config.get('global', 'file_postfix')

        #self.data_output_path = config.get('global', 'data_output_path')
        self.log_path = config.get('global', 'log_path')
        self.project_list_file = config.get('global', 'project_list_file')
        # self.staff_list_file = config.get('global', 'staff_list_file') # 改成其他参数赋值

    def load_project_list(self):
        """
        加载项目列表
        """
        with open(self.project_list_file, 'rb') as project_file:
            project_start_flag = False
            for line in project_file.readlines():
                line_array = line.strip().decode().split('|')
                # 读取project的wiki页面，标识为5个|，如|RD999003|支撑工作（固网）|||，split后为6
                # 2016.07.09 标识改为6个|，如|RD999003|支撑工作（固网）|||RD999003|，split后为7
                if (len(line_array) != 7):
                    continue
                elif project_start_flag:
                    # 在wiki页面里的项目名称定义方式有多种，需要处理一下
                    #
                    prj_name = Project.strip_spec_char( line_array[2])
                    self.project_list[prj_name] = line_array[5] # line_array[5]是项目对应的编号
                    print('项目名称：' + prj_name + ' 项目编号：' + line_array[5])
                elif line_array[1].count('-') > 3: # markdown的表格的表头和内容通过 | ---- | ---- | ... 分开的
                    project_start_flag = True
                    continue

    def load_staff_list(self):
        """
        加载员工列表
        """
        with open(self.staff_list_file, 'rb') as staff_file:
            for line in staff_file.readlines():
                line_array = line.strip().decode().split('|')
                # 判断是否员工的方法，| 分隔格式是否正确，第一个元素的是否为6位数字工号
                if (len(line_array) != 7):
                    continue
                else:
                    job_num = Staff.strip_spec_char(line_array[1])
                    if Staff.is_job_num(job_num):
                        staff =  Staff(job_num, Staff.strip_spec_char(line_array[2]), Staff.strip_spec_char(line_array[3]), Staff.is_on_job(line_array[1]))
                        self.staff_list[line_array[3].strip()] = staff
                        staff.to_staff_info()

    def to_log(self):
        """
        日志信息
        """
        print('daily_input_path = %s' % self.daily_input_path)
        print('data_output_path = %s' % self.data_output_path)
        print('file_prefix = %s' % self.file_prefix)
        print('file_postfix = %s' % self.file_postfix)
        print('project_list_file = %s' % self.project_list_file)
        print('staff_list_file = %s' % self.staff_list_file)

    def staff_data_to_file(self, data_file, err_data_file, job_status=None):
        """

        :param data_file:
        :param err_data_file:
        :param job_status:
        :return:
        """

        no_data_name_list = [] # 没有数据的名称列表

        # TODO 没有数据staff也要输出来
        for (key,staff) in self.staff_list.items():
            if staff.job_state == False:
                continue
            else:
                if len(staff.project_list) == 0:
                    no_data_name_list.append(staff.name)
                staff.data_to_file(data_file)
                staff.err_data_to_file(err_data_file)
        self.list_to_file(no_data_name_list, err_data_file)

    def list_to_file(self, list, output_file):
        with open(output_file, 'a', encoding='utf-8') as out_file:
            out_file.write("没有统计项目数据的人员列表：\n")
            for str in list:
                # print("%s %s %s %s" % (self.name, t[0], t[1].get_name(), t[1].get_time()))
                out_file.write("%s \n" % str)

    def clear_staff_project_data(self):
        """
        清理staff的项目数据
        :return:
        """
        for (key,staff) in self.staff_list.items():
            staff.clear_project_data()

# 程序入口
if __name__ == '__main__':
    c = Config()
    c.load_config()
    c.to_log()
    c.load_project_list()
    print("")
    c.load_staff_list()
    print("")
    # print(c.project_list.get("UBAS系统1"))

    # print(c._is_job_num("000121"))
