# -*- coding:utf-8 -*-
"""
GFS下载合并后的风场 ---> 插值
"""
import os
import datetime
import time
from datetime import timedelta
import xarray as xr
import numpy as np
import pandas as pd
import argparse
from netCDF4 import Dataset
from christmas.commonCode import make_dir
from christmas import cprintf, osprint
from christmas.read_conf import read_conf


def para_iss():  # sourcery skip: merge-duplicate-blocks, remove-redundant-if
    # 获得默认参数
    nd = datetime.datetime.now()  # 按当天时间运行
    now_day = nd.strftime('%Y%m%d')
    time_now = int(nd.strftime('%H%M'))
    if time_now <= 630:     # 2:30后12不在运行
        file_List = '12'    # [12, 18, 0, 6]
    elif time_now <= 1230:  # 8:30后12,18不在运行
        file_List = '18'    # [18, 0, 6]
    elif time_now <= 1830:  # 14:30后12,18,00不在运行
        file_List = '00'    # [0, 6]
    elif time_now <= 2230:  # 20:30后12,18,00,06不在运行
        file_List = '06'    # [6]
    else:
        file_List = '06'
    # 添加外参
    parser = argparse.ArgumentParser(description="-d 日期 ;-n 风场时次文件夹")
    parser.add_argument('-d', default=now_day, help='输入时间格式为:20200101', type=str)
    parser.add_argument('-n', default=file_List, help='输入次数格式为:12', type=str)

    # 获取外参
    args = parser.parse_args()
    if len(args.d) != 8:
        osprint('输入时间格式为:20200101')
        exit()
    if len(args.n) != 2:
        osprint('输入次数格式为:12')
        exit()
    return args.d, args.n


def find_file(file_dir, prefix):
    all_file = os.listdir(file_dir)
    file_name = []
    file_path = []
    for f in all_file:
        if f.startswith(prefix):
            file_name.append(f)
            file_path.append(os.path.join(file_dir, f))
    return file_path


def seperation(_date, _conf_file='Configures/Interp_gfs_wind.conf'):
    para_conf = read_conf(_conf_file)  # 读取配置文件
    output_path = para_conf['Out_Path']
    file_name = para_conf['Region_Folder']

    needday = _date
    input_dir = os.path.join(output_path, file_name, needday)
    file_list = find_file(input_dir, 'w')
    out_dir = os.path.join(output_path, file_name,  needday, needday)
    for f in file_list:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        data = Dataset(f)
        lat = data.variables['latitude'][:]
        lon = data.variables['longitude'][:]
        timeNC=data.variables['time'][:]
        u_new=data.variables["U10"][:]
        v_new=data.variables["V10"][:]
        value_new=data.variables["v_VM"][:]
        dir_new=data.variables["dir_VM"][:]

        for i in range(24):
            outname = f'{file_name}_' + f[-11:-3] + str(i).zfill(2) + '.nc'
            out=os.path.join(out_dir, outname)
            da = Dataset(out, "w", format="NETCDF3_64BIT")

            da.createDimension("longitude", len(lat))
            da.createDimension("latitude", len(lon))
            da.createDimension("time", 1)

            da.createVariable("longitude", np.float64, "longitude")
            da.createVariable("latitude", np.float64, "latitude")
            da.createVariable("time", "f", "time")
            da.createVariable("U10", "f", ("time", "latitude", "longitude"))
            da.createVariable("V10", "f", ("time", "latitude", "longitude"))
            da.createVariable("v_VM", "f", ("time", "latitude", "longitude"))
            da.createVariable("dir_VM", "f", ("time", "latitude", "longitude"))

            da.variables["longitude"][:] = lon[:]
            da.variables["latitude"][:] = lat[:]
            da.variables["time"][:] = timeNC[i]
            da.variables["U10"][:] = u_new[i, :, :]
            da.variables["V10"][:] = v_new[i, :, :]
            da.variables["v_VM"][:] = value_new[i, :, :]
            da.variables["dir_VM"][:] = dir_new[i, :, :]

            da.close()


def run_interp2d(_date, _num, _conf_file='Configures/Interp_gfs_wind.conf'):
    # py_file_path = os.path.dirname(os.path.abspath(__file__))  # 当前python文件所在位置

    para_conf = read_conf(_conf_file)  # 读取配置文件
    lonmin = para_conf['Lon_min']  # 经度最小值
    lonmax = para_conf['Lon_max']  # 经度最大值
    latmin = para_conf['Lat_min']  # 纬度最小值
    latmax = para_conf['Lat_max']  # 纬度最大值
    Res_point = para_conf['Res_point']  # 格点数量

    num_grid = int(round(latmax - latmin, 2) * Res_point)   # 创建插值格点
    lon_new = np.linspace(lonmin, lonmax, num_grid)
    lat_new = np.linspace(latmin, latmax, num_grid)

    gfs_path = para_conf['Gfs_Path']                          # gfs文件夹路径
    Out_Path = para_conf['Out_Path']                          # 输出文件夹路径
    Region_Folder = para_conf['Region_Folder']                # 小区域文件夹路径
    output_path = os.path.join(Out_Path, Region_Folder, _date)
    # 输出文件夹路径
    make_dir(output_path)

    # 检测wind_3.nc文件（00:00检测文件夹12 00:06检测18）
    while True:
        if os.path.exists(f'{gfs_path}/{_date}/{_num}/wind_3.nc'):
            cprintf('INFO', f'{_date}的{_num}的wind_3文件存在')
            time.sleep(1)
            break
        else:
            cprintf('ERROR', f'未检测到{_date}的{_num}的wind_3文件,等待10分钟')
            time.sleep(10*60)

    # 合并前一天和当天的wind_3.nc文件
    nd = datetime.datetime.strptime(_date, '%Y%m%d')
    ago_date = (nd + timedelta(days=-1)).strftime('%Y%m%d')
    nc_data1 = xr.open_dataset(f'{gfs_path}/{ago_date}/{_num}/wind_3.nc')
    nc_data2 = xr.open_dataset(f'{gfs_path}/{_date}/{_num}/wind_3.nc')
    nc_data = xr.concat([nc_data2, nc_data1], dim='time')
    nc_data1.close()
    nc_data2.close()
    # 去重
    _, index = np.unique(nc_data['time'], return_index=True)
    nc_data = nc_data.isel(time=index)

    # 时区转换
    nc_data['time'] = nc_data['time'] + pd.Timedelta('8 hours')
    # 更改变量名字
    nc_data = nc_data.rename({'UGRD_10maboveground': 'U10', 'VGRD_10maboveground': 'V10'})
    # 插值到小区域并按时间截取
    for i in range(9):  # 天数(9天)
        cprintf('SUCCESS', f'正在处理{(nd + timedelta(days=i)).strftime("%Y%m%d")}')
        date_range = pd.date_range(start=nd+timedelta(days=i), end=nd+timedelta(days=i)+timedelta(hours=23), freq='H')
        nc_tem = nc_data.interp(longitude=lon_new, latitude=lat_new, time=date_range, method='linear')  # 时间空间插值
        # 添加新变量
        value = np.sqrt(nc_tem['U10'] ** 2 + nc_tem['V10'] ** 2)
        wind_dir = (np.arctan2(nc_tem['U10'], nc_tem['V10']) / np.pi) * 180 + 180
        nc_tem = nc_tem.update({'v_VM': value, 'dir_VM': wind_dir})
        # 压缩等级
        nc_tem.encoding['format'] = 'NETCDF4'
        nc_tem.encoding['engine'] = 'h5netcdf'
        nc_tem.encoding['dtype'] = 'float32'
        nc_tem['U10'].encoding['zlib'] = True
        nc_tem['U10'].encoding['complevel'] = 4
        nc_tem['V10'].encoding['zlib'] = True
        nc_tem['V10'].encoding['complevel'] = 4
        nc_tem['v_VM'].encoding['zlib'] = True
        nc_tem['v_VM'].encoding['complevel'] = 4
        nc_tem['dir_VM'].encoding['zlib'] = True
        nc_tem['dir_VM'].encoding['complevel'] = 4
        # 保存文件
        fout = f'{output_path}/{Region_Folder}_{(nd + timedelta(days=i)).strftime("%Y%m%d")}.nc'
        nc_tem.to_netcdf(fout)
    nc_data.close()

    seperation(_date, _conf_file)


if __name__ == '__main__':
    date, num = para_iss()
    run_interp2d(date, num)
