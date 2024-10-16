#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  日期 : 2023/4/11 20:22
#  作者 : Dovelet, Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""
根据散点分辨率，最近插值最为接近实际情况
从散点数据提取单点数据， 并将单点数据转换为json｜txt文件
Have done!!!
"""
import argparse
import netCDF4
import numpy as np
import datetime
import os
import math
import scipy.integrate
import scipy.interpolate
import json
from christmas import makedirs
from christmas.cprintf import cprintf
import baysalt.strDateTime as strDateTime
from baysalt.Interp.Interp_g2s import print_args


class Sca2Sca:
    def __init__(self, s_lon, s_lat, _input, _output, _name, value_list, title_list, m_hours=216, time_zone=8, _location=None, _separate_tj=False):
        self.s_lon = s_lon  # 单点经度
        self.s_lat = s_lat  # 单点纬度
        self._input = _input  # 输入数据文件夹， 如：'/home/ocean/ForecastSystem/WW3_6.07/Output/ww3_dql/', 内存有'yyyymmdd/ww3.yyyymmdd.nc'文件
        self._output = _output  # 输出数据文件夹， 如：'/home/ocean/PostProcess/160/Data/single_json/'
        self._name = _name  # 输出文件名称， 如：'dql01_'
        self.value_list = value_list  # 需要提取的变量列表
        self.title_list = title_list  # 需要提取的变量名称列表
        self.m_hours = list(range(m_hours))  # 预报时效
        self.time_zone = time_zone  # 时间区间， 如：8
        self._location = _location  # json文件的location信息
        self._separate_tj = _separate_tj  # 是否区分txt和json文件夹
    
    def getsp(self, _date):
        # sourcery skip: inline-immediately-returned-variable
        """
        索引ww3点位,找到最近的ww3散点
        :param _date: 任务日期
        :return: 点位No
        """
        _date = str(_date)
        filename = os.path.join(self._input, f'{_date}/ww3.{_date}.nc')

        w = netCDF4.Dataset(filename)

        lon = w.variables['longitude'][:]
        lat = w.variables['latitude'][:]
        D = np.zeros((lon.size, 1))
        for i in range(lon.size):
            D[i] = (self.s_lon - lon[i]) ** 2 + (self.s_lat - lat[i]) ** 2  # 读取ww3_rizhao的nc文件，传入w中
        p = np.argwhere(D == min(D))

        return p
    
    def getData(self, _date, _idx, p):
        # 时间处理，将UTC转为CST
        date1 = datetime.datetime.strptime(f'{_date}00', '%Y%m%d%H')
        t_idx = _idx - self.time_zone  # 向前time_zone个钟头，找到对应时区当天的0点, 如CST应为 - 8
        date2 = date1 + datetime.timedelta(hours=t_idx)
        idx = t_idx % 24
        filename = os.path.join(self._input, date2.strftime('%Y%m%d') + '/ww3.' + date2.strftime('%Y%m%d') + '.nc')  # ww3 nc文件名
        w = netCDF4.Dataset(filename)
        wind_swell = ["shww", "mpww", "hmaxw", "shts", "mpts", "hmaxs"]
        rely_on_hs = ["hmaxe", "h4", "h10"]
        current = ["currentspeeds", "currentspeedm", "currentspeedb", "currentdirs", "currentdirm", "currentdirb"]
        interp_value = []
        interp_num = []
        for ele in self.value_list:
            
            if ele in rely_on_hs:
                element = w.variables['hs'][idx, :][p[0][0]]
                temp = self.rely_on_hs(element, ele)
            elif ele in wind_swell:
                temp = self.wind_swell_cal(date2, idx, p, ele)
            elif ele in current:
                temp = self.gettpxo(_date, _idx, ele)
            elif ele in ["mdww", "mdts"]:
                temp = w.variables['dir'][idx, :][p[0][0]]
            elif ele == "pp1d":
                temp = 1 / w.variables['fp'][idx, :][p[0][0]]
                if np.isnan(temp):  # 谱峰周期为空时，采用2.99代替,过于不科学了嗷兄弟们
                    temp = 2.99
            else:
                temp = w.variables[ele][idx, :][p[0][0]]
            
            interp_value, interp_num = self.return_str_value(interp_value, interp_num, temp)
        return interp_value, interp_num
    
    @staticmethod
    def getTime(_date, _hour):
        """
        获取预报的日期/小时
        :param _date: 任务日期
        :param _hour: 小时
        :return: 日期/小时(10位长度的字符串)
        """
        date = strDateTime.convertToTime(_date)
        date_t = date + datetime.timedelta(hours=int(_hour))
        
        return date_t.strftime('%Y%m%d%H')
    
    @staticmethod
    def return_str_value(interp_value, interp_num, _value, retract=14):
        if str(_value).strip() == "--":
            _value = np.nan
        _value = np.round(_value, 2)
        interp_value.append(str(_value).format('.2f').rjust(retract, " "))
        interp_num.append(_value)
        return interp_value, interp_num
    
    @staticmethod
    def rely_on_hs(value, ele):
        if ele == "hmaxe":
            return np.round(1.46 * value, 2)
        elif ele == "h4":
            # 平均波高Hp
            Hp = (0.747 * value) / 1.129
            return np.round(2.024 * Hp, 2)
        elif ele == "h10":
            # 平均波高Hp
            Hp = (0.747 * value) / 1.129
            return np.round(1.712 * Hp, 2)
    
    def wind_swell_cal(self, _date, idx, p, ele):
        # sourcery skip: extract-duplicate-method
        """
        专门做风浪涌浪数据处理
        :param _date: _date是经过时区处理的
        :param idx: 时间点
        :param p: 点位索引
        :param ele: ele要素名
        :return: 要什么给什么
        """
        # 读取一位谱数据用于下面计算风浪和涌浪
        ef_filename = os.path.join(self._input, _date.strftime('%Y%m%d') + '/ww3.' + _date.strftime(
            '%Y%m%d') + '_ef.nc')
        ww3_ef = netCDF4.Dataset(ef_filename)
        ef = ww3_ef.variables['ef'][:, :, p[0][0]]
        f = ww3_ef.variables['f'][:]
        # 风浪要素计算准备
        sf2 = ef[idx, 18:30]
        fs2 = f[18:30]
        # 涌浪要素计算准备
        sf1 = ef[idx, 0:18]
        fs1 = f[:18]
        if ele == "shww":
            wndhs = 4 * math.sqrt(scipy.integrate.trapz(sf2, fs2))  # 计算风浪有效波高
            return np.round(wndhs, 2)
        # 新的风浪替代公式
        elif ele == "mpww":
            wndtm = math.sqrt(
                scipy.integrate.trapz(sf2, fs2) / scipy.integrate.trapz(np.multiply(fs2 ** 2, sf2), fs2))  # 计算风浪有效周期
            return np.round(wndtm, 2)
        elif ele == "hmaxw":
            wndhs = 4 * math.sqrt(scipy.integrate.trapz(sf2, fs2))
            wndmaxhs = 1.46 * wndhs
            return np.round(wndmaxhs, 2)  # 风浪最大波高
        elif ele == "shts":
            shs = 4 * math.sqrt(scipy.integrate.trapz(sf1, fs1))  # 计算涌浪有效波高
            return np.round(shs, 2)
        elif ele == "mpts":
            swelltm = math.sqrt(
                scipy.integrate.trapz(sf1, fs1) / scipy.integrate.trapz(np.multiply(fs1 ** 2, sf1), fs1))  # 计算涌浪有效周期
            return np.round(swelltm, 2)
        elif ele == "hmaxs":
            shs = 4 * math.sqrt(scipy.integrate.trapz(sf1, fs1))
            maxshs = 1.46 * shs
            return np.round(maxshs, 2)  # 涌浪最大波高
        else:
            # 这句话是多余的，懒得改
            cprintf('ERROR', f"要素名有误：{ele},请检查风涌浪要素名称是否正确.")
    
    def gettpxo(self, _date, _idx, ele):
        # 时间处理，不需要转cst
        date1 = datetime.datetime.strptime(f'{_date}00', '%Y%m%d%H')
        date2 = date1 + datetime.timedelta(hours=_idx)
        filename = f'/data/Postprocess/160/Data/input/tpxo/{_date[:4]}_singlepoint_tpxo.nc'
        w = netCDF4.Dataset(filename, 'r', format='NETCDF4')
        lons = w.variables['longitude'][:]
        times = w.variables['TIME_CST'][:]
        
        row = next(
            (
                i
                for i in range(len(times))
                if ("".join(times[i].astype(str).tolist())) == date2.strftime('%Y%m%d%H')
            ),
            0,
        )
        col = np.argmin(np.abs(lons - self.s_lon))
        
        # print(row,col)
        u_m = w.variables['u'][row, col]  # 中层流速u
        v_m = w.variables['v'][row, col]  # 中层流速v
        # 计算流速和流向
        _dir = math.atan2(u_m, v_m)
        _dir = int(_dir * 180 / math.pi)
        if _dir < 0:
            _dir += 360
        speed = (u_m ** 2 + v_m ** 2) ** 0.5
        if ele[7:10] == "dir":
            return np.round(float(_dir), 2)
        elif ele == "currentspeeds":
            return np.round(float(1.2 * speed), 2)
        elif ele == "currentspeedm":
            return np.round(float(1.0 * speed), 2)
        else:
            return np.round(float(0.5 * speed), 2)
    
    def makefore(self, _date, _txt=True, _json=True):
        # sourcery skip: extract-duplicate-method, low-code-quality
        """
        txt 预报单的生成
        :param _date: 任务日期
        :param _txt: 是否生成txt文件
        :param _json: 是否生成json文件
        :return: none
        """
        if type(_date) == int:
            _date = str(_date)

        if self._separate_tj:
            file_path_txt = os.path.join(self._output, 'single_txt')
            file_path_json = os.path.join(self._output, 'single_json')
        else:
            file_path_txt = self._output
            file_path_json = self._output
        
        makedirs(file_path_txt, file_path_json)
        p = self.getsp(_date)  # 获取最近索引
        # 写入文件内容----------------------------------begin
        
        if _txt and not _json:  # 只生成txt文件
            cprintf('INFO', '生成txt文件中')
            
            tmp = self.m_hours
            
            file_name = self._name + _date + ".txt"
            
            file = os.path.join(file_path_txt, file_name)
            
            with open(file, "w") as fl:
                # 写入文件头----------------------------------begin
                fl.writelines("UTC{0:+03d}".format(self.time_zone).rjust(10, " "))
                for ele in self.title_list:
                    fl.writelines(ele.rjust(14, " "))
                fl.writelines('\n')
                # 写入文件头----------------------------------end
                
                for i in range(max(tmp) + 1):
                    fc_time = self.getTime(_date, i)  # 获取时间
                    txt_ele, json_ele = self.getData(_date, i, p)
                    del json_ele
                    if i in self.m_hours:
                        fl.writelines(fc_time)
                        fl.writelines(txt_ele)
                        fl.writelines('\n')
                        cprintf('SUCCESS', f"hour in={str(i)}")

        elif _txt:
            cprintf('INFO', '开始生成txt和json文件')

            tmp = self.m_hours
            json_data_list = []
            txt_data_list = []
            for i in range(max(tmp) + 1):
                # 创建json数据----------------------------------begin
                fc_time = self.getTime(_date, i)  # 第一列日期留空白
                
                txt_ele, json_ele = self.getData(_date, i, p)  # 获取数据
                del txt_ele
                for j in range(len(json_ele)):
                    if str(json_ele[j]).strip() == "--":
                        json_ele[j] = np.nan
                
                JsonData, TxtData = self.getTxtJsonData(fc_time, json_ele)  # dict()
                ## json
                json_data_list.append(JsonData)
                ## txt
                txt_data_list.append(TxtData)
                
                # 创建json数据----------------------------------end
                if i in self.m_hours:
                    cprintf('SUCCESS', f"hour in={str(i)}")
            # 创建json文件----------------------------------begin
            file_name_json = self._name + _date + ".json"
            file_json = os.path.join(file_path_json, file_name_json)
            if self._location is None:
                new_dict = {"location": {"lon": self.s_lon, "lat": self.s_lat}, "data": json_data_list}
            else:
                new_dict = {"location": self._location, "data": json_data_list}
            
            with open(file_json, "w") as f:
                json.dump(new_dict, f, ensure_ascii=False, indent=10)
            # 写入json文件内容----------------------------------end
            
            # 创建txt文件----------------------------------begin
            file_name_txt = self._name + _date + ".txt"
            file_txt = os.path.join(file_path_txt, file_name_txt)
            # 写入txt文件内容----------------------------------begin
            with open(file_txt, "w") as fl:
                fl.writelines("UTC{0:+03d}".format(self.time_zone).rjust(10, " "))
                for ele in self.title_list:
                    fl.writelines(ele.rjust(14, " "))
                fl.writelines('\n')
                for row in txt_data_list:
                    fl.writelines(row)
                    fl.writelines('\n')
            # 写入txt文件内容----------------------------------end
        elif _json:
            cprintf('INFO', '开始生成json文件')
            
            tmp = self.m_hours
            json_data_list = []
            for i in range(max(tmp) + 1):
                # 创建json数据----------------------------------begin
                fc_time = self.getTime(_date, i)  # 第一列日期留空白
                
                txt_ele, json_ele = self.getData(_date, i, p)  # 获取
                del txt_ele
                for j in range(len(json_ele)):
                    if str(json_ele[j]).strip() == "--":
                        json_ele[j] = np.nan
                
                JsonData = self.getJsonData(fc_time, json_ele)  # dict()
                ## json
                json_data_list.append(JsonData)
                
                # 创建json数据----------------------------------end
                if i in self.m_hours:
                    cprintf('SUCCESS', f"hour in={str(i)}")
            # 创建json文件----------------------------------begin
            file_name = self._name + _date + ".json"
            file = os.path.join(file_path_json, file_name)
            if self._location is None:
                new_dict = {"location": {"lon": self.s_lon, "lat": self.s_lat}, "data": json_data_list}
            else:
                new_dict = {"location": self._location, "data": json_data_list}

            with open(file, "w") as f:
                json.dump(new_dict, f, ensure_ascii=False, indent=10)
            # 写入json文件内容----------------------------------end
    
    def getJsonData(self, fc_time, json_ele):
        postData = {'date': fc_time}
        for i in range(len(self.value_list)):
            postData[self.title_list[i]] = np.round(np.float64(json_ele[i]), 2)
        
        return postData
    
    def getTxtJsonData(self, fc_time, json_ele):
        postJsonData = {'date': fc_time}
        PostTxtData = [fc_time]
        for i in range(len(self.value_list)):
            postJsonData[self.title_list[i]] = np.round(np.float64(json_ele[i]), 2)
            PostTxtData.append(str(json_ele[i]).format('.2f').rjust(14, " "))
        
        return postJsonData, PostTxtData


def get_parser():
    # Grid2scatter.conf文件路径
    baysalt_path = os.path.dirname(os.path.abspath(__file__))
    Conf_Grid2scatter_file = os.path.join(baysalt_path, 'Configures', 'Grid2scatter.conf')
    # 区分参数大小写
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog="End help",
        add_help=False,
        prog=f'./{os.path.basename(__file__)}',
        conflict_handler='error',
        formatter_class=argparse.RawTextHelpFormatter,
        allow_abbrev=True,
        prefix_chars='-+',
        # description='Usages',
    )
    parser.add_argument_group(
        'Usages Help', '%(prog)s \n'
                       '                -m liner \n'
                       '                -t 8 \n'
                       '                -p 4 \n'
                       '                -lon 114 \n'
                       '                -lat 35 \n'
                       '                -iv hs lm \n'
                       '                -ov swh mwl \n'
                       '                -i  /data/ForecastSystem/WW3_6.07/Output/ww3_WPacific/ \n'
                       '                -o  ./ \n'
                       '                -n try \n'
                       '                -d 20230301 \n'
                       '%(prog)s \n'
                       '                -conf 1 \n'
    )
    parser.usage = '%(prog)s [options] parameter'
    parser.add_argument('-h', '--help', action='help', help='show this help message and exit')
    parser.add_argument('-t', required=False, type=int, metavar='', default=8, help='set time zone')
    parser.add_argument('-lon', required=False, type=float, metavar='', default=0, help='set longitude')
    parser.add_argument('-lat', required=False, type=float, metavar='', default=0, help='set latitude')
    parser.add_argument('-iv', required=False, type=str, metavar='', default=['hs', 't02', 'dir', 'fp', 'lm', 'hmaxe'],
                        help='set input variable name', choices=['hs', 't02', 'dir', 'fp', 'lm', 'hmaxe'], nargs='+')
    parser.add_argument('-ov', required=False, type=str, metavar='',
                        default=['swh', 'mwp', 'mwd', 'pp1d', 'mwl', 'hmax'], help='set output variable name',
                        nargs='+')
    parser.add_argument('-i', required=False, type=str, metavar='',
                        default='/data/Output_160/ww3_djk/', help='set input path')
    parser.add_argument('-o', required=False, type=str, metavar='', default='./', help='set output path')
    parser.add_argument('-n', required=False, type=str, metavar='', default='s2s_', help='set output file name')
    parser.add_argument('-d', required=False, type=str, metavar='', default=strDateTime.getToday(), help='set date')
    parser.add_argument('-conf', required=False, type=str, metavar='', default=Conf_Grid2scatter_file, help='set conf')
    
    return parser.parse_args(), Conf_Grid2scatter_file


def example():

    args, _ = get_parser()
    print_args(args)

    X = Sca2Sca(119.78182518, 35.57300175, _input=args.i, _output=args.o, _name=args.n, value_list=args.iv, title_list=args.ov)
    X.makefore(_date=args.d, _json=True, _txt=True)


if __name__ == '__main__':
    example()
