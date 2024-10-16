# -*- coding: utf-8 -*-
# @File    : lalala.py
# @Date    : 2023-04-11
# @Author  : Dovelet
import xarray as xarray
from metpy.interpolate import inverse_distance_to_grid
import numpy as np
import matplotlib.pyplot as plt
import time as T
from pykrige.ok import OrdinaryKriging
# 读取数据
plt.rcParams["font.family"] = ["sans-serif"]
plt.rcParams["font.sans-serif"] = ['SimHei']


# metpy cressman插值
def example1(radius=500/111000, neighbors=3):
    # metpy cressman插值
    # 通过改变r和min_neighbors可以改变插值的效果
    # r是欧氏距离，建议根据散点实际分辨率设置
    # min_neighbors是最小邻居数，如果找不到这么多邻居，就不插值
    f = xarray.open_dataset(r'ww3.20230417.nc')
    s_lon = f['longitude'].data
    s_lat = f['latitude'].data
    hs = f['hs'].data[0, :]

    lonmin = 120.15
    lonmax = 120.3
    latmin = 35.95
    latmax = 36.1
    re_ra = 400
    ##
    num_grid = int(round(latmax - latmin, 2) * re_ra)
    lon_new = np.linspace(lonmin, lonmax, num_grid)  # 创建插值格点
    lat_new = np.linspace(latmin, latmax, num_grid)

    lon_gridmesh, lat_gridmesh = np.meshgrid(lon_new, lat_new)

    start= T.time()
    tm_grid = inverse_distance_to_grid(s_lon, s_lat, hs, lon_gridmesh, lat_gridmesh, r=radius, min_neighbors=neighbors)
    end= T.time()
    print(f'metpy cressman插值耗时：{end-start}')
    plt.figure(1)
    plt.contourf(tm_grid)
    plt.colorbar()
    plt.title(f'metpy cressman插值 r={np.round(radius,2)},min_neighbors={neighbors}')
    plt.show()


# 克里金插值
def example2(model='linear'):
    # 一种对已知样本加权平均以估计平面上的未知点，并使得估计值与真实值的数学期望相同且方差最小的地统计学过程
    # 通过改变variogram_model可以改变插值的效果
    # pykrige提供 linear, power, gaussian, spherical, exponential, hole-effect几种variogram_model可供选择，默认的为linear模型
    f = xarray.open_dataset(r'ww3.20230417.nc')
    s_lon = f['longitude'].data
    s_lat = f['latitude'].data
    hs = f['hs'].data[0, :]

    lonmin = 120.15
    lonmax = 120.3
    latmin = 35.95
    latmax = 36.1
    re_ra = 400
    ##
    num_grid = int(round(latmax - latmin, 2) * re_ra)
    lon_new = np.linspace(lonmin, lonmax, num_grid)  # 创建插值格点
    lat_new = np.linspace(latmin, latmax, num_grid)

    # 需要对数据进行区域限定
    flag1=np.where((s_lon>=lonmin) & (s_lon<=lonmax))
    s_lon=s_lon[flag1]
    s_lat=s_lat[flag1]
    hs=hs[flag1]
    flag2=np.where((s_lat>=latmin) & (s_lat<=latmax))
    s_lon=s_lon[flag2]
    s_lat=s_lat[flag2]
    hs=hs[flag2]

    start = T.time()
    krige= OrdinaryKriging(s_lon, s_lat, hs, variogram_model=model, verbose=False, enable_plotting=False)
    tm_grid, ss = krige.execute('grid', lon_new, lat_new)
    end = T.time()
    print(f'克里金插值耗时：{end - start}')
    plt.figure(2)
    plt.contourf(tm_grid)
    plt.colorbar()
    plt.title(f'克里金线性插值，model：{model}')
    # 保存图片
    plt.show()
    plt.savefig(r'lalala2.png')


if __name__ == '__main__':
    example1()
    example2()
