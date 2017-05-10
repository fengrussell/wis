# -*- coding: utf-8 -*-

"""
    Copyright (c) 2008-2015 wing

    FileName: file_util.py

    ProjectName: wis 

    Description: 文件操作工具类

    History:
    v1.0.0, hlj, 2016-04-28 18:28, Created:

"""

import os

# 获取待处理文件列表
def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if special_file.startswith(prefix) and special_file.endswith(postfix):
                files_list.append(os.path.join(root, special_file))
    if len(files_list):
        print('%d files(prefix=%s,postfix=%s) matched in %s!' % (len(files_list), prefix, postfix, directory))
    else:
        print('%d files(prefix=%s,postfix=%s) matched in %s!' % (len(files_list), prefix, postfix, directory))
        exit()
    return files_list

# 获取待处理文件列表
def scan_files(directory, prefix, postfixs):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if special_file.startswith(prefix) and special_file.endswith(postfixs):
                files_list.append(os.path.join(root, special_file))
    if len(files_list):
        print('%d files(prefix=%s,postfix=%s) matched in %s!' % (len(files_list), prefix, postfixs, directory))
    else:
        print('%d files(prefix=%s,postfix=%s) matched in %s!' % (len(files_list), prefix, postfixs, directory))
        exit()
    return files_list

