# -*- coding: utf-8 -*-

# @File    : newnew_cangnan.py
# @Date    : 2023-07-26
# @Author  : Dovelet
# -*- coding: utf-8 -*-

"""
1.增加流速提取的部分
2.将WW3里识别为陆地的地方采取idw插值的方式进行填充
"""

import netCDF4
import numpy as np
import os
import datetime
import baysalt.strDateTime as strDateTime
from scipy.interpolate import interp2d
from scipy.interpolate import interpn
import scipy.integrate
import json
import math
import scipy.spatial as spt
import itertools

m_hours = list(range(120))
fvcom_dir='/data/Output_147/FVCOM_ECS_storm/Run/'
tpxo_dir='/home/ocean/Project/Cangnan_hedian/Data/input/tpxo/'

class Cangnan_Single:
    def __init__(self, _lon, _lat, _input, _output_txt, _output_json, _name, **_new_dict):
        self._lon = _lon
        self._lat = _lat
        self._input = _input
        self._output_txt = _output_txt
        self._output_json = _output_json
        self._name = _name
        self._new_dict = _new_dict
        self.p=None

    def getnum(self, _date, _idx,para1,para2):
        """
        获取ww3_djk数据
        :param _date: 任务日期
        :param _idx: 小时
        :return: 有效波高，平均周期，谱峰周期，平均波向
        """
        # 时间处理，将UTC转为CST
        date1 = datetime.datetime.strptime(f'{_date}00', '%Y%m%d%H')
        _idx = _idx - 8  # 向前8个钟头，找到CST当天的0点
        date2 = date1 + datetime.timedelta(hours=_idx)
        idx = _idx % 24
        filename = self._input + date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime(
            '%Y%m%d') + '.nc'  # ww3 nc文件名

        w = netCDF4.Dataset(filename)  # 读取ww3_Wp的nc文件，传入w中
        lons = w.variables['longitude'][:]
        lats = w.variables['latitude'][:]
        ww3hs = w.variables['hs'][idx, :, :]  # 有效波高
        ww3t02 = w.variables['t02'][idx, :, :]  # 平均周期
        ww3fp = w.variables['fp'][idx, :, :]  # 谱峰频率
        ww3dir = w.variables['dir'][idx, :, :]  # 波向
        ww3swellhs = w.variables['phs1'][idx, :, :]  # 涌浪有效波高
        ww3swelltm = w.variables['ptp1'][idx, :, :]  # 涌浪谱峰周期
        ww3lm = w.variables['lm'][idx, :, :]  # 波长

        fhs = interp2d(lons, lats, ww3hs, kind='linear')
        hs = fhs(self._lon, self._lat)
        if hs[0] < 1e+10:
            ft02 = interp2d(lons, lats, ww3t02, kind='linear')
            ffp = interp2d(lons, lats, ww3fp, kind='linear')
            fdir = interp2d(lons, lats, ww3dir, kind='linear')
            fswellhs = interp2d(lons, lats, ww3swellhs, kind='linear')
            fswelltm = interp2d(lons, lats, ww3swelltm, kind='linear')
            flm = interp2d(lons, lats, ww3lm, kind='linear')
            # H4
            t02 = ft02(self._lon, self._lat)
            # H10
            mwd = fdir(self._lon, self._lat)
            # pp
            PP = 1 / ffp(self._lon, self._lat)
            # phs1
            phs1 = fswellhs(self._lon, self._lat)
            # ptp1
            ptp1 = fswelltm(self._lon, self._lat)
            # LM
            lm = flm(self._lon, self._lat)
            if phs1[0] >= 1e+10 or ptp1[0] >= 1e+10:  # 涌浪波高或谱峰周期为空时用一维谱计算
                ef_filename = self._input + date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime(
                    '%Y%m%d') + '_ef.nc'  # ww3_ef nc文件名
                ww3_ef = netCDF4.Dataset(ef_filename)
                ww3ef = ww3_ef.variables['ef'][idx, :, :, :]
                f = ww3_ef.variables['f'][:]

                Z, Y, X = np.meshgrid(f, self._lat, self._lon, indexing='ij')
                ef = interpn((f, lats, lons), ww3ef, (Z, Y, X), method='linear')  # 维度和值的维度是正的

                # 涌浪要素
                # 新的涌浪计算公式
                sf1 = ef[:18, 0, 0]
                fs1 = f[:18]
                phs1[0] = 4 * math.sqrt(scipy.integrate.trapz(sf1, fs1))  # 计算涌浪有效波高
                ptp1[0] = math.sqrt(
                    scipy.integrate.trapz(sf1, fs1) / scipy.integrate.trapz(np.multiply(fs1 ** 2, sf1),fs1))  # 计算涌浪有效周期
            # hs_rtn = np.round(hs[0], 2)
            # t02_rtn = np.round(t02[0], 2)
            # dir_rtn = np.round(mwd[0], 2)
            # PP_rtn = np.round(PP[0], 2)
            # phs1_rtn = np.round(phs1[0], 2)
            # ptp1_rtn = np.round(ptp1[0], 2)
            # lm_rtn = np.round(lm[0], 2)
        else:
            hs =self.gts_idw(ww3hs, para1, para2)
            t02 = self.gts_idw(ww3t02, para1, para2)
            mwd = self.gts_idw(ww3dir, para1, para2)
            PP = 1 / self.gts_idw(ww3fp, para1, para2)
            phs1 = self.gts_idw(ww3swellhs, para1, para2)
            ptp1 = self.gts_idw(ww3swelltm, para1, para2)
            lm = self.gts_idw(ww3lm, para1, para2)
            
            if str(phs1) =='--' or str(ptp1)=='--':  # 涌浪波高或谱峰周期为空时用一维谱计算
                ef_filename = self._input + date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime(
                    '%Y%m%d') + '_ef.nc'  # ww3_ef nc文件名
                ww3_ef = netCDF4.Dataset(ef_filename)
                ww3ef = ww3_ef.variables['ef'][idx, :, :, :]
                f = ww3_ef.variables['f'][:]

                Z, Y, X = np.meshgrid(f, self._lat, self._lon, indexing='ij')
                ef = interpn((f, lats, lons), ww3ef, (Z, Y, X), method='linear')  # 维度和值的维度是正的

                # 涌浪要素
                # 新的涌浪计算公式
                sf1 = ef[:18, 0, 0]
                fs1 = f[:18]
                phs1 = 4 * math.sqrt(scipy.integrate.trapz(sf1, fs1))  # 计算涌浪有效波高
                ptp1 = math.sqrt(
                    scipy.integrate.trapz(sf1, fs1) / scipy.integrate.trapz(np.multiply(fs1 ** 2, sf1),fs1))  # 计算涌浪有效周期

            if phs1 >= 1e+10 or ptp1 >= 1e+10:
               phs1=self.judge_swell(ww3swellhs,para1)
               ptp1=self.judge_swell(ww3swelltm,para1)

            if not phs1 or not ptp1:
                phs1=np.nan
                ptp1=np.nan

        hs_rtn = np.round(np.float64(hs), 2)
        t02_rtn = np.round(np.float64(t02), 2)
        dir_rtn = np.round(np.float64(mwd), 2)
        PP_rtn = np.round(np.float64(PP), 2)
        phs1_rtn = np.round(np.float64(phs1), 2)
        ptp1_rtn = np.round(np.float64(ptp1), 2)
        lm_rtn = np.round(np.float64(lm), 2)

        return hs_rtn, t02_rtn, dir_rtn, PP_rtn, phs1_rtn, ptp1_rtn, lm_rtn


    def judge_swell(self, value,para1):
        for i in range(len(para1)):
            if str(value[para1[i]])=='--':
                continue
            else:
                return value[para1[i]]




    def getfore(self, _date, _idx,para1,para2):
        """
        获取ww3_djk数据,流场数据
        :param _date: 任务日期
        :param _idx: 小时
        :return: 有效波高，平均周期，谱峰周期，平均波向
        """
        hs_rtn, t02_rtn, dir_rtn, PP_rtn, phs1_rtn, ptp1_rtn, lm_rtn = self.getnum(_date, _idx,para1,para2)
        
        uvh_avg = self.getcurrent(_date, _idx,self.p)
        fc_cmu = uvh_avg['ua']
        fc_cmv = uvh_avg['va']
        fc_h = uvh_avg['zeta']

        return str(format(hs_rtn, '.2f')).rjust(12, " "), \
               str(format(t02_rtn, '.2f')).rjust(12, " "), \
               str(format(dir_rtn, '.2f')).rjust(12, " "), \
               str(format(PP_rtn, '.2f')).rjust(12, " "), \
               str(format(phs1_rtn, '.2f')).rjust(12, " "), \
               str(format(ptp1_rtn, '.2f')).rjust(12, " "), \
               str(format(lm_rtn, '.2f')).rjust(12, " "), \
                str(format(fc_cmu, '.2f')).rjust(12, " "), \
                str(format(fc_cmv, '.2f')).rjust(12, " "), \
                str(format(fc_h, '.2f')).rjust(12, " ")




    def getcurrent(self,_date,_idx,p):
        """
        获取fvcom数据
        :param _date: 日期
        :param _idx: 预报小时（需要做时间处理）
        :param p: fvcom网格点的索引
        :return: 流uv，深度
        """
        # 时间处理，将UTC转为CST

        if _idx>=120:
            uvh_avg = {'ua': np.nan, 'va': np.nan, 'zeta': np.nan}
            return uvh_avg
        _idx_tpxo = _idx
        _date_tpxo = _date
        date1 = datetime.datetime.strptime(f'{_date}00', '%Y%m%d%H') # 预报起始时间
        date3 = date1 + datetime.timedelta(days=-1)  # 预报起始前一天
        _idx = _idx - 8  # 向前8个钟头，找到CST当天的0点
        date2 = date1 + datetime.timedelta(hours=_idx) # 预报时刻
        idx = _idx % 24

        if _idx<0:
            filename=os.path.join(fvcom_dir,date2.strftime('%Y%m%d')+'/output'+'/forecast_0001.nc')

        else:

            # 一个小天才的写法，哈哈哈哈
            filename=os.path.join(fvcom_dir,date2.strftime('%Y%m%d')+'/output'+'/forecast_0001.nc')

            if os.path.exists(filename)==False:

                filename=os.path.join(fvcom_dir,date1.strftime('%Y%m%d')+'/output'+'/forecast_'+str(int(_idx/24)+1).zfill(4)+'.nc')

            if os.path.exists(filename)==False:

                filename=os.path.join(fvcom_dir,date3.strftime('%Y%m%d')+'/output'+'/forecast_'+str(int(_idx/24)+2).zfill(4)+'.nc')

        f_c = netCDF4.Dataset(filename) #fvcom nc
        ua = f_c.variables['ua'][:]
        va = f_c.variables['va'][:]
        # 环流的u,v
        ua_model = ua[idx,  p[0]]
        va_model = va[idx,  p[0]]
        # u_s= u[idx,0, p[0]]
        # v_s= v[idx,0, p[0]]
        # u_m= u[idx,1, p[0]]
        # v_m= v[idx,1, p[0]]
        # u_b= u[idx,2, p[0]]
        # v_b= v[idx,2, p[0]]
        # 水位
        h_zeta = f_c.variables['zeta'][:]
        zeta=h_zeta[idx,p[1]]

        # 潮流的u,v
        uvh_tpxo_dict = self.get_tpxo(_date_tpxo, _idx_tpxo)
        # tpxo_us = uv_tpxo_dict['u_s']
        # tpxo_vs = uv_tpxo_dict['v_s']
        # tpxo_um = uv_tpxo_dict['u_m']
        # tpxo_vm = uv_tpxo_dict['v_m']
        # tpxo_ub = uv_tpxo_dict['u_b']
        # tpxo_vb = uv_tpxo_dict['v_b']
        tpxo_u_mean = uvh_tpxo_dict['u_mean']
        tpxo_v_mean = uvh_tpxo_dict['v_mean']
        tpxo_h_mean = uvh_tpxo_dict['h']

        # 合并环流和潮流的UVh
        ua = ua_model + tpxo_u_mean
        va = va_model + tpxo_v_mean
        zeta = zeta + tpxo_h_mean
        
        # u_s = u_s + tpxo_us
        # v_s = v_s + tpxo_vs
        # u_m = u_m + tpxo_um
        # v_m = v_m + tpxo_vm
        # u_b = u_b + tpxo_ub
        # v_b = v_b + tpxo_vb
        # 保留两位小数
        ua = np.round(np.float64(ua), 2)
        va = np.round(np.float64(va), 2)
        # u_s = np.round(np.float64(u_s), 2)
        # v_s = np.round(np.float64(v_s), 2)
        # u_m = np.round(np.float64(u_m), 2)
        # v_m = np.round(np.float64(v_m), 2)
        # u_b = np.round(np.float64(u_b), 2)
        # v_b = np.round(np.float64(v_b), 2)

        zeta=np.round(np.float64(zeta),2)
        
        uvh_avg = {'ua': ua, 'va': va, 'zeta': zeta}

        return uvh_avg


    def get_current_sp(self,_date):
        """
        找到最近的fvcom数据点的索引
        :param _date: 日期。
        :return: 点位索引
        """
        _date = str(_date)
        date1 = datetime.datetime.strptime(f'{_date}00', '%Y%m%d%H')  # 预报起始时间
        date3 = date1 + datetime.timedelta(days=-1)  # 预报起始前一天
        date3= date3.strftime('%Y%m%d')
        filename = os.path.join(fvcom_dir, date3 + '/output' + '/forecast_0001.nc')
        f_c = netCDF4.Dataset(filename)  # fvcom nc
        lonc= f_c.variables['lonc'][:]
        latc= f_c.variables['latc'][:]
        D=np.sqrt((lonc-self._lon)**2+(latc-self._lat)**2)
        idx_uv=np.argmin(D)

        lon=f_c.variables['lon'][:]
        lat=f_c.variables['lat'][:]
        D=np.sqrt((lon-self._lon)**2+(lat-self._lat)**2)
        idx_h=np.argmin(D)

        return [idx_uv,idx_h]


    def get_tpxo(self,_date,_idx):
        date1 = datetime.datetime.strptime(_date + '00', '%Y%m%d%H')
        date2 = date1 + datetime.timedelta(hours=_idx)
        date2 = date2.strftime('%Y%m%d%H')
        filename= os.path.join(tpxo_dir, date2[0:4]+'_singlepoint_tpxo.nc')
        f_t = netCDF4.Dataset(filename)  # tpxo nc
        lons = f_t.variables['longitude'][:]

        col = np.argmin(np.abs(lons - self._lon))
        row = self.hourInyear(date2)
        # 潮流的u,v
        u_m = f_t.variables['u'][row, col]  # 中层流速u
        v_m = f_t.variables['v'][row, col]  # 中层流速v
        h = f_t.variables['h'][row, col]  # 潮位
        # 计算表层流速和底层
        u_s = u_m*np.sqrt(1.2)
        v_s = v_m*np.sqrt(1.2)
        u_b = u_m*np.sqrt(0.5)
        v_b = v_m*np.sqrt(0.5)
        
        u_mean = u_m
        v_mean = v_m
        
        uvh = {'u_s': u_s, 'v_s': v_s, 'u_m': u_m, 'v_m': v_m, 'u_b': u_b, 'v_b': v_b, 'u_mean': u_mean, 'v_mean': v_mean,'h':h}

        return uvh


    def hourInyear(self,given_time):
        given_time = datetime.datetime.strptime(given_time, "%Y%m%d%H")
        day_of_year = given_time.timetuple().tm_yday  # 获取该时刻是一年中的第几天
        hour_of_day = given_time.hour  # 获取该时刻是当天的第几个小时
        return (day_of_year - 1) * 24 + hour_of_day

    @staticmethod
    def getTime(_date, _hour):
        """
        获取预报的日期/小时
        :param _date: 任务日期
        :param _hour: 小时
        :return: 日期/小时(10位长度的字符串)
        """
        if _hour == 215:
            _hour = 215

        date = strDateTime.convertToTime(_date)
        date_t = date + datetime.timedelta(hours=int(_hour))

        return date_t.strftime('%Y%m%d%H')

    @staticmethod
    def nan2str(_data):
        # 将nan转换为字符串
        if np.isnan(_data):
            return 'NaN'
        else:
            return _data

    @staticmethod
    def getJsonData(date, fc_hs, fc_dir, fc_t01, fc_lm, fc_PP, fc_phs1, fc_ptp1, fc_cmu, fc_cmv, fc_h):
        # sourcery skip: dict-literal, inline-immediately-returned-variable, merge-dict-assign
        postData = dict()
        postData['date'] = date
        postData['swh'] = fc_hs
        postData['mwd'] = fc_dir
        postData['mwp'] = fc_t01
        postData['pp1d'] = Cangnan_Single.nan2str(fc_PP)
        postData['shts'] = Cangnan_Single.nan2str(fc_phs1)
        postData['mpts'] = Cangnan_Single.nan2str(fc_ptp1)
        postData['mwl'] = Cangnan_Single.nan2str(fc_lm)
        postData['u_average'] = Cangnan_Single.nan2str(fc_cmu)
        postData['v_average'] = Cangnan_Single.nan2str(fc_cmv)
        # postData['u_surface'] = Cangnan_Single.nan2str(fc_csu)
        # postData['v_surface'] = Cangnan_Single.nan2str(fc_csv)
        # postData['u_middle'] = Cangnan_Single.nan2str(fc_cmu)
        # postData['v_middle'] = Cangnan_Single.nan2str(fc_cmv)
        # postData['u_bottom'] = Cangnan_Single.nan2str(fc_cbu)
        # postData['v_bottom'] = Cangnan_Single.nan2str(fc_cbv)
        postData['h'] = Cangnan_Single.nan2str(fc_h)
        return postData

    def grttxt(self, _date):
        """
        构建预报单信息
        :param _date: 预报单日期
        :return: 0-生成预报数据成功  大于等于1-生成预报数据失败
        """

        today = strDateTime.getToday()
        file_path = self._output_txt
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        # 写入文件内容----------------------------------begin
        _date0 = _date
        list_hours = [m_hours]
        # 写入文件头----------------------------------begin
        fh_time = "time".rjust(12, " ")  # 第一列日期留空白
        fh_hs = "swh".rjust(12, " ")  # 有效波高
        fh_dir = "mwd".rjust(12, " ")  # 波向
        fh_t01 = "mwp".rjust(12, " ")  # 平均周期
        fh_lm = 'mwl'.rjust(12, " ")  # 波长
        fh_PP = "pp1d".rjust(12, " ")  # 谱峰周期
        fh_phs1 = 'shts'.rjust(12, " ")  # 涌浪有效波高
        fh_ptp1 = 'mpts'.rjust(12, " ")  # 涌浪谱峰周期
        # 流场数据开头
        fh_cmu='u_average'.rjust(12, " ")
        fh_cmv='v_average'.rjust(12, " ")
        # fh_css='u_surface'.rjust(12, " ")
        # fh_csm='v_surface'.rjust(12, " ")
        # fh_csb='u_middle'.rjust(12, " ")
        # fh_cds='v_middle'.rjust(12, " ")
        # fh_cdm='u_bottom'.rjust(12, " ")
        # fh_cdb='v_bottom'.rjust(12, " ")
        fh_h='h'.rjust(12, " ")

        self.p = self.get_current_sp(_date)
        para1, para2 = self.judge_method(_date)  # 反距离加权插值的参数


        for k in range(1):
            tmp = list_hours[k]
            file_name = self._name + strDateTime.addDays(_date, k) + ".txt"
            file = os.path.join(file_path, file_name)

            with open(file, "w") as fl:
                fl.writelines([fh_time, fh_hs, fh_dir, fh_t01, fh_lm, fh_PP, fh_phs1, fh_ptp1,fh_cmu,fh_cmv,fh_h,"\n"])
                # 写入文件头----------------------------------end

                for i in range(max(tmp) + 1):  # +72

                    fc_time = self.getTime(_date0, i)  # 第一列日期留空白

                    fc_hs, fc_t01, fc_dir, fc_PP, fc_phs1, fc_ptp1, fc_lm, fc_cmu, fc_cmv, fc_h = self.getfore(_date0, i,para1,para2)  # 获得数据

                    # if fc_PP.strip() == "nan":  # 谱峰周期为空时，采用2.99代替
                    #     fc_PP = str(2.99).rjust(12, " ")
                    if i in m_hours:

                        fl.writelines([fc_time, fc_hs, fc_dir, fc_t01, fc_lm, fc_PP, fc_phs1, fc_ptp1, fc_cmu, fc_cmv, fc_h,"\n"])
                        print(f"hour in={str(i)}")
                    else:
                        print(f"hour={str(i)}")

    def grtjson(self, _date):

        file_path = self._output_json
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        _date0 = _date
        list_hours = [m_hours]
        self.p = self.get_current_sp(_date)
        para1, para2 = self.judge_method(_date)  # 反距离加权插值的参数
        # 创建json数据----------------------------------begin
        for k in range(1):
            tmp = list_hours[k]
            list = []
            for i in range(max(tmp) + 1):

                fc_time = self.getTime(_date0, i)  # 第一列日期留空白

                fc_hs, fc_t01, fc_dir, fc_PP, fc_phs1, fc_ptp1, fc_lm = self.getnum(_date0, i,para1, para2)  # 获取数据
                uvh_avg = self.getcurrent(_date0, i,self.p)
                fc_cmu = uvh_avg['ua']
                fc_cmv = uvh_avg['va']
                fc_h = uvh_avg['zeta']

                # if np.isnan(fc_PP):  # 谱峰周期为空时，采用2.99代替
                #     fc_PP = 2.99

                JsonData = self.getJsonData(fc_time, fc_hs, fc_dir, fc_t01, fc_lm, fc_PP, fc_phs1, fc_ptp1, fc_cmu, fc_cmv, fc_h)  # dict()
                list.append(JsonData)
                # 创建json数据----------------------------------end
                # 创建json文件----------------------------------begin
                file_name = self._name + strDateTime.addDays(_date, k) + ".json"
                file = os.path.join(file_path, file_name)
                # new_dict = {"location": {"No": "rzlssh01", "name": "日照岚山港区原油码头", "lon": lon_g, "lat": lat_g}, "data": list}
                new_dict = {"location": self._new_dict, "data": list}
                with open(file, "w") as f:
                    json.dump(new_dict, f, ensure_ascii=False, indent=10)
                # 写入文件内容----------------------------------end

    def judge_method(self, _date):

        _date1 = datetime.datetime.strptime(f'{_date}', '%Y%m%d')
        filename = self._input + _date1.strftime('%Y%m%d') + '/ww3.' + _date1.strftime(
            '%Y%m%d') + '.nc'  # ww3 nc文件名

        w = netCDF4.Dataset(filename)  # 读取ww3_Wp的nc文件，传入w中
        lons = w.variables['longitude'][:]
        lats = w.variables['latitude'][:]
        value = w.variables['hs'][0, :, :]  # 有效波高
        method = 'idw'
        cal_id, cal_pa = self.idw_para(lons, lats, value, self._lon, self._lat,12)

        return cal_id, cal_pa

    @staticmethod
    def gts_idw(value, cal_id, cal_pa):
        result = 0
        for i in range(len(cal_id)):
            result = result + cal_pa[i] * value[cal_id[i]]
        return result

    def idw_para(self, g_lon, g_lat, value, s_lon, s_lat,search_point):
        lat_number = len(g_lat)
        lon_number = len(g_lon)
        # 生成格点坐标，放进一个二维平面
        grid = []
        for i, j in itertools.product(range(lon_number), range(lat_number)):
            x = [g_lon[i], g_lat[j]]
            grid.append(x)
        point = np.array(grid)

        # 用于快速查找的KDTree类
        kt = spt.KDTree(data=point, leafsize=10)
        ckt = spt.cKDTree(point)  # 用C写的查找类，执行速度更快
        find_point = np.array([s_lon, s_lat])  # 原点
        distance, sequence = kt.query(find_point, search_point)  # 返回最近邻点的距离d和在数组中的顺序sequence
        fp = []  # 存格点
        if search_point == 1:
            fp.extend(point[i] for i in range(len(point)) if i == sequence)
        else:
            fp.extend(point[p] for p in sequence)
        index = []  # 存索引
        for f in fp:
            id = self.find_index(g_lon, g_lat, f[0], f[1])
            index.append(id)

        cal_id = []  # 存可以进入计算的点的索引
        cal_d = []
        for i in range(len(index)):
            if self.detect_nan(value[index[i]]):
                cal_id.append(index[i])
                cal_d.append(distance[i])
        # 反距离加权参数的计算
        cal_pa = []
        total = 0
        for item in cal_d:
            total = total + 1 / item
        cal_pa.extend((1 / dis) / total for dis in cal_d)
        return cal_id, cal_pa


    @staticmethod
    def detect_nan(value):
        """
        判断格点数据是否满足双线性插值条件
        :param value: 取出的格点数据
        :return: 满足则返回1，不满足则返回0
        """
        try:
            if value.mask:
                return 0
        except Exception:
            return 1

    @staticmethod
    def find_index(g_lon, g_lat, s_lon, s_lat):
        """
        获取经纬度索引
        :param g_lon: 一维格点经度
        :param g_lat: 一维格点纬度
        :param s_lon: 散点经度
        :param s_lat: 散点纬度
        :return: 纬度索引 经度索引
        """
        latli = np.argmin(np.abs(g_lat - s_lat))
        lonli = np.argmin(np.abs(g_lon - s_lon))
        return latli, lonli


if __name__ == '__main__':
    input_path = '/data/ForecastSystem/WW3_6.07/Output/ww3_WPacific/'
    py_file_path = os.path.dirname(os.path.abspath(__file__))
    output_path_txt = os.path.join(py_file_path, './Data/single_txt/')
    output_path_json = os.path.join(py_file_path, './Data/single_json/')
    if not os.path.exists(output_path_txt):
        os.makedirs(output_path_txt)
    if not os.path.exists(output_path_json):
        os.makedirs(output_path_json)
    location_xdhy1 = {"No": "bdhy1", "name": "浅滩北堤海域1", "lon": 121.071017,
                      "lat": 27.926412}
    name_xdhy1 = "bdhy1_121.071E_27.926N_"
    c=Cangnan_Single( 121.071017, 27.926412, input_path, output_path_txt, output_path_json, name_xdhy1,**location_xdhy1)

    #c.grttxt('20230728')
    print('json')
    c.grtjson('20230728')
    print('end')
