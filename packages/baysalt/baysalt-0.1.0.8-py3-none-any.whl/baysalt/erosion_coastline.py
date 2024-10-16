# -*- coding: utf-8 -*-

# @File    : erosion_coastline.py
# @Date    : 2023-03-25
# @Author  : Dovelet

import itertools
import numpy as np
from netCDF4 import Dataset
import scipy.spatial as spt
from scipy.io import loadmat
import matplotlib.pyplot as plt
import json
import xarray as xr
from collections import deque


def find_index(g_lon, g_lat, _s_lon, _s_lat):
    """
    获取经纬度索引
    :param g_lon: 一维格点经度
    :param g_lat: 一维格点纬度
    :param _s_lon: 散点经度
    :param _s_lat: 散点纬度
    :return: 纬度索引 经度索引
    """
    _s_lon = np.array(_s_lon)
    _s_lat = np.array(_s_lat)

    _latli = np.where(g_lat == _s_lat[:, None])[-1]
    _lonli = np.where(g_lon == _s_lon[:, None])[-1]

    return _latli.tolist(), _lonli.tolist()


def erosion_cal_id(g_lon, g_lat, value, k, judge_num, _print=False, methond='npnan'):
    # sourcery skip: inline-immediately-returned-variable, low-code-quality
    """
    找到离指定散点最近的K个格点
    :param g_lon: 一维格点经度
    :param g_lat: 一维格点纬度
    :param value: 二维格点值
    :param k: 寻找近邻点的个数
    :param judge_num: 周边水点数 > judge_num的点，改为水点
    :param _print: 是否打印输出
    :param methond: 判断是否为nan的方法
    :return: 格点索引id
    """
    lat_number = len(g_lat)
    lon_number = len(g_lon)
    # 生成格点坐标，放进一个二维平面
    if _print:
        print('开始建立Kdtree')
    grid = []
    grid=deque(grid)
    for i, j in itertools.product(range(lon_number), range(lat_number)):
        x = [g_lon[i], g_lat[j]]
        grid.append(x)
    point = np.array(grid)
    fp_lon = []
    fp_lon = deque(fp_lon)
    fp_lat = []
    fp_lat = deque(fp_lat)

    # 用于快速查找的KDTree类

    ckt = spt.cKDTree(point)  # 用C写的查找类，执行速度更快
    # 开始把所有格点进行一个循环
    if _print:
        print(f'Kdtree建立完毕，开始查找{k}个近邻点')

    for ig in point:
        x, y = [], []
        x.append(ig[0])
        y.append(ig[1])
        id1, id2 = find_index(g_lon, g_lat, x, y)
        del x, y
        if methond=='np.nan':
            # print(id1, id2, value[id1, id2])
            if not np.isnan(value[id1, id2]):
                continue
            # find_point = np.array(ig)
        elif methond=='nc.mask':
            if not value.mask[id1, id2]:
                continue
            # find_point = np.array(ig)
        elif methond=='txt.mask':
            if value[id1, id2] != 0:
                continue
            # find_point = np.array(ig)
        distance, sequence = ckt.query(ig, k)  # 返回最近k个邻点的距离d和在数组中的顺序sequence
        for item in sequence:
            fp_lon.append(grid[item][0])
            fp_lat.append(grid[item][1])
    if _print:
        print('查找完毕，开始获取行列索引')

    lat_id, lon_id = find_index(g_lon, g_lat, fp_lon, fp_lat)

    if _print:
        print('行列索引已全部获取，开始判断nan值个数')
    
    lonli_arr = np.array([0])
    latli_arr = np.array([0])
    if methond=='np.nan':
        latli_arr, lonli_arr=judge_nan_npnan(lat_id, lon_id, value, k, judge_num)
    elif methond=='nc.mask':
        latli_arr, lonli_arr=judge_nan_ncmask(lat_id, lon_id, value, k, judge_num)
    elif methond == 'txt.mask':
        latli_arr, lonli_arr = judge_nan_txtmask(lat_id, lon_id, value, k, judge_num)
    if _print:
        print(f'判断完毕，水点数不少于{judge_num}的点才参与运算')

    # 每行第一列就是要改的值
    _change_lat= latli_arr[:, 0].tolist()
    _change_lon= lonli_arr[:, 0].tolist()
    # 每行剩下的就是用来赋值的
    _value_lat = latli_arr[:, 1:].tolist()
    _value_lon = lonli_arr[:, 1:].tolist()

    _weight = {
        'change_lat': _change_lat,
        'change_lon': _change_lon,
        'value_lat': _value_lat,
        'value_lon': _value_lon,
    }
    return _weight


def judge_nan_ncmask(latli, lonli, value, k, judge_num):

    # 将获得的索引分开，保证K个索引是同一个点的最近临点索引
    latli_1 = np.array(latli)
    lonli_1 = np.array(lonli)
    latli_2 = np.reshape(latli_1, [-1, k])
    lonli_2 = np.reshape(lonli_1, [-1, k])
    mask_arr=value.mask
    test_arr=mask_arr[latli_2.tolist(), lonli_2.tolist()]  # 判断找出来的点里有哪些需要处理

    sum_arr=np.sum(test_arr, axis=1)  #

    select_id=np.where(sum_arr <= k-judge_num)[0].tolist()

    latli_r=latli_2[select_id[:]]
    lonli_r=lonli_2[select_id[:]]

    return latli_r, lonli_r


def judge_nan_npnan(latli, lonli, value, k, judge_num):
    # 将获得的索引分开，保证K个索引是同一个点的最近临点索引
    latli_1 = np.array(latli)
    lonli_1 = np.array(lonli)
    latli_2 = np.reshape(latli_1, [-1, k])
    lonli_2 = np.reshape(lonli_1, [-1, k])
    mask_arr=np.isnan(value)

    test_arr=mask_arr[latli_2.tolist(), lonli_2.tolist()]  # 判断找出来的点里有哪些需要处理
    print(test_arr)
    sum_arr=np.sum(test_arr, axis=1)  #

    select_id=np.where(sum_arr <= k-judge_num)[0].tolist()

    latli_r=latli_2[select_id[:]]
    lonli_r=lonli_2[select_id[:]]

    return latli_r, lonli_r


def judge_nan_txtmask(latli, lonli, value, k, judge_num):
    latli_1 = np.array(latli)
    lonli_1 = np.array(lonli)
    latli_2 = np.reshape(latli_1, [-1, k])
    lonli_2 = np.reshape(lonli_1, [-1, k])

    test_arr = value[latli_2.tolist(), lonli_2.tolist()]  # 判断找出来的点里有哪些需要处理

    sum_arr = np.sum(test_arr, axis=1)  #

    select_id = np.where(sum_arr >= judge_num)[0].tolist()

    latli_r = latli_2[select_id[:]]
    lonli_r = lonli_2[select_id[:]]

    return latli_r, lonli_r


def erosion_via_id(_weight, value):
    """
    通过索引id进行腐蚀
    :param _weight: weight字典
    :param value: 二维格点值
    """

    _change_lat = _weight['change_lat']
    _change_lon = _weight['change_lon']
    _value_lat = _weight['value_lat']
    _value_lon = _weight['value_lon']

    new = value.copy()
    if value.ndim == 3:
        for i in range(value.shape[0]):
            replace=value[i, _value_lat, _value_lon]
            replace=np.nanmean(replace, axis=1)
            new[i, _change_lat, _change_lon]=replace[:]

    elif value.ndim == 2:
        replace=value[_value_lat, _value_lon]
        replace=np.nanmean(replace, axis=1)
        new[_change_lat, _change_lon]=replace[:]

    return new


def example_cal_weight():  # sourcery skip: extract-duplicate-method

    methoood = 1
    weight = {}
    viss = []
    if methoood == 1:
        mask_wrf = loadmat('baysalt/Forage/erosion_data/mask_wrf.mat')['mask_wrf'][300:500, 900:1200]
        xr_nc = xr.open_dataset('baysalt/Forage/erosion_data/erosion_ww3.nc')  # ww3直接输出的nc，由于海浪可能算出来nan，所以用地形文件判断nan
        lons = xr_nc['longitude'][900:1200].data
        lats = xr_nc['latitude'][300:500].data
        viss = xr_nc['hs'][:, 300:500, 900:1200].data
        xr_nc.close()
        weight = erosion_cal_id(lons, lats, mask_wrf, 16, 3, methond='txt.mask', _print=True)
        mask_2 = erosion_via_id(weight, mask_wrf)

    elif methoood == 2:
        f = Dataset('baysalt/Forage/erosion_data/erosion_xujie.nc')  # 杰哥写的nc，用mask的属性判断nan，data里是--，mask里是True
        lons = f.variables['lon'][:]
        lats = f.variables['lat'][:]
        viss = f.variables['hs'][:]
        f.close()
        weight = erosion_cal_id(lons, lats, viss, 16, 3, methond='nc.mask', _print=True)

    elif methoood == 3:
        f = Dataset('baysalt/Forage/erosion_data/erosion_Post_ww3.nc')  # Postprocess_WW3产生的nc，mask为False，data里是nan
        lons = f.variables['longitude'][900:1200].data
        lats = f.variables['latitude'][300:500].data
        viss = f.variables['swh'][:, 300:500, 900:1200].data
        f.close()
        weight = erosion_cal_id(lons, lats, viss[0, :, :], 16, 3, methond='np.nan', _print=True)

    with open('weight.json', 'w') as f:
        json.dump(weight, f)
    with open('weight.json', 'r') as f:
        weight=json.load(f)

    new_hs=erosion_via_id(weight, viss)

    plt.contourf(viss[0, :, :], cmap='jet')
    plt.colorbar()
    plt.show()
    plt.contourf(new_hs[0, :, :], cmap='jet')
    plt.colorbar()
    plt.show()


def test():
    mask_wrf = loadmat('mask_wrf.mat')['mask_wrf']
    xr_nc = xr.open_dataset('/home/ocean/ForecastSystem/Output/WW3_output/20230407/ww3.20230407.nc')
    lons = xr_nc['longitude'][:].data
    lats = xr_nc['latitude'][:].data
    xr_nc.close()

    weight_1 = erosion_cal_id(lons, lats, mask_wrf, 16, 3, methond='txt.mask', _print=True)
    mask_wrf_1 = erosion_via_id(weight_1, mask_wrf)

    weight_2 = erosion_cal_id(lons, lats, mask_wrf_1, 16, 3, methond='txt.mask', _print=True)

    with open('weight_1.json', 'w') as f:
        json.dump(weight_1, f)
    with open('weight_2.json', 'w') as f:
        json.dump(weight_2, f)

    check_draw()


def check_draw():  # sourcery skip: extract-duplicate-method
    # 验证
    xr_nc = xr.open_dataset('baysalt/Forage/erosion_data/erosion_ww3.nc')
    viss = xr_nc['hs'][:].data
    xr_nc.close()

    with open('/Users/christmas/Desktop/weight_1.json', 'r') as f:
        weight_1 = json.load(f)
    with open('/Users/christmas/Desktop/weight_2.json', 'r') as f:
        weight_2 = json.load(f)
    new_hs = erosion_via_id(weight_1, viss)
    new_hs_2 = erosion_via_id(weight_2, new_hs)

    plt.contourf(viss[0, 500:800, 1200:1700], cmap='jet')
    plt.colorbar()
    plt.show()
    plt.contourf(new_hs[0, 500:800, 1200:1700], cmap='jet')
    plt.colorbar()
    plt.show()
    plt.contourf(new_hs_2[0, 500:800, 1200:1700], cmap='jet')
    plt.colorbar()
    plt.show()


def example_cal_weight_xu(method):  # sourcery skip: extract-duplicate-method

    methoood = method
    weight = {}
    viss = []
    if methoood == 1:
        mask_wrf = loadmat('mask_wrf.mat')['mask_wrf'][300:500, 900:1200]
        xr_nc = xr.open_dataset('erosion_ww3.nc')  # ww3直接输出的nc，由于海浪可能算出来nan，所以用地形文件判断nan
        lons = xr_nc['longitude'][900:1200].data
        lats = xr_nc['latitude'][300:500].data
        viss = xr_nc['hs'][:, 300:500, 900:1200].data
        xr_nc.close()
        weight = erosion_cal_id(lons, lats, mask_wrf, 16, 3, methond='txt.mask', _print=True)
        mask_2 = erosion_via_id(weight, mask_wrf)

    elif methoood == 2:
        f = Dataset('erosion_xujie.nc')  # 杰哥写的nc，用mask的属性判断nan，data里是--，mask里是True
        lons = f.variables['lon'][:]
        lats = f.variables['lat'][:]
        viss = f.variables['hs'][:]
        f.close()
        weight = erosion_cal_id(lons, lats, viss, 16, 3, methond='nc.mask', _print=True)

    elif methoood == 3:
        f = Dataset('erosion_Post_ww3.nc')  # Postprocess_WW3产生的nc，mask为False，data里是nan
        lons = f.variables['longitude'][900:1200].data
        lats = f.variables['latitude'][300:500].data
        viss = f.variables['swh'][:, 300:500, 900:1200].data
        f.close()
        weight = erosion_cal_id(lons, lats, viss[0, :, :], 16, 3, methond='np.nan', _print=True)

    with open('weight.json', 'w') as f:
        json.dump(weight, f)
    with open('weight.json', 'r') as f:
        weight=json.load(f)

    new_hs=erosion_via_id(weight, viss)
    if method !=2:
        plt.contourf(viss[0, :, :], cmap='jet')
        # plt.colorbar()
        # plt.show()
        plt.savefig('viss.png')
        plt.contourf(new_hs[0, :, :], cmap='jet')
    else:
        plt.contourf(viss[:], cmap='jet')
        # plt.colorbar()
        # plt.show()
        plt.savefig('viss.png')
        plt.contourf(new_hs[:], cmap='jet')

    # plt.colorbar()
    # plt.show()
    plt.savefig('new_hs.png')


if __name__ == '__main__':
    import time as T

    start = T.time()
    example_cal_weight_xu(3)
    end = T.time()
    print(end - start)
    # test()
