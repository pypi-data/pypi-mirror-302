#!/Users/christmas/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#  日期 : 2023/3/27 10:56
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""

"""

from christmas.read_conf import read_conf
from christmas import Blog
from christmas.commonCode import get_date, make_dir, osprint, split_path, osprints
import datetime
import itertools
from datetime import timedelta
import os


def select_file(_date, menu_path=r'Select_zip.conf', _logger=Blog().logger):
    menu = read_conf(menu_path)
    file_path = split_path(menu['SelectfromDir'])  # 原始文件的位置
    zip_path = split_path(menu['SelectputDir'])   # 压缩文件的位置
    dir_suffix = menu['DirSuffix']                                      # 压缩文件后缀名
    file_suffix = menu['FileSuffix']                                # 文件后缀名
    format_select = menu['Format_select']                         # 日期格式
    Format_date_py = menu['Format_date_py']                         # 日期格式
    Save_path = os.path.join(zip_path, f'{_date}{dir_suffix}')  # 保存路径
    # Zip_path = f'{Save_path}.zip'
    # path_to_del =[Save_path, Zip_path]
    # # 删除旧文件-------start
    # for i in path_to_del:
    #     if os.path.exists(i):
    #         os.system(f"rm -r {i}")
    #         osprint(f'已删除旧文件{i}！')
    make_dir(f'{Save_path}')
    # 删除旧文件并创建新文件夹-------end

    # 挑选和cp文件-------start
    folder_list = menu['Folder_list']
    filepre_list = menu['Filepre_list']
    time_list = menu['Switch_Select']

    for i, j in itertools.product(range(len(folder_list)), time_list):
        for day in range(int(menu['Select_duration'])):
            try:
                nd = datetime.datetime.strptime(_date, Format_date_py) + timedelta(day)
                input_path = f"{file_path}/{folder_list[i]}/{j}/{datetime.datetime.strftime(nd, '%Y%m%d')}"  # 插值文件输入位置
                output_path = f"{Save_path}/{folder_list[i]}/{j}/{datetime.datetime.strftime(nd, '%Y%m%d')}"
                make_dir(output_path)
                os.system(f"cp {input_path}/{filepre_list[i]}{file_suffix}{format_select} {output_path}")
            except Exception as e:
                continue
            if day == int(menu['Select_duration']) - 1:
                if j =='.':
                    _logger.info(f'{folder_list[i]} ---> {datetime.datetime.strftime(nd, "%Y%m%d")}')
                else:
                    _logger.info(f'{folder_list[i]}--{j} ---> {datetime.datetime.strftime(nd, "%Y%m%d")}')
    # 挑选和cp文件-------end


def zip_file(_date, menu_path=r'Select_zip.conf', _type='r', _logger=Blog().logger):
    menu = read_conf(menu_path)
    zip_path = split_path(menu['SelectputDir'])   # 压缩文件的位置
    dir_suffix = menu['DirSuffix']                                      # 压缩文件后缀名
    # 压缩
    pwd = os.getcwd()
    os.chdir(zip_path)
    if _type == 'r':  # 递归
        command = f"zip -qr {_date}{dir_suffix}.zip {_date}{dir_suffix}"
    elif _type == 'j':  # 不存储目录
        command = f"zip -qj {_date}{dir_suffix}.zip {_date}{dir_suffix}/*"
    else:
        raise ValueError('zip type error!')
    os.system(command)

    if not os.path.exists(f'{_date}{dir_suffix}.zip'):
        _logger.error(f'cd {zip_path} && {command} && cd {pwd}')
    else:
        _logger.info(f'已压缩{_date}{dir_suffix}.zip！')

    os.chdir(pwd)


def tgz_file(_date, menu_path=r'Select_zip.conf', _logger=Blog().logger):
    menu = read_conf(menu_path)
    zip_path = split_path(menu['SelectputDir'])   # 压缩文件的位置
    dir_suffix = menu['DirSuffix']                                      # 压缩文件后缀名
    # 压缩
    if os.path.exists(f'{_date}{dir_suffix}.tgz'):
        os.system(f"rm -r {_date}{dir_suffix}.tgz")
    pwd = os.getcwd()
    os.chdir(zip_path)
    os.system(f"tar czf {_date}{dir_suffix}.tgz {_date}{dir_suffix}")

    if not os.path.exists(f'{_date}{dir_suffix}.tgz'):
        _logger.error(f'tar czf {_date}{dir_suffix}.tgz {_date}{dir_suffix}')
    os.chdir(pwd)


def select_zip(_date, menu_path=r'Select_zip.conf'):
    select_file(_date, menu_path=menu_path)
    zip_file(_date, menu_path=menu_path)


if __name__ == '__main__':
    _date = get_date()
    select_zip(_date, menu_path='Select_zip.conf')
