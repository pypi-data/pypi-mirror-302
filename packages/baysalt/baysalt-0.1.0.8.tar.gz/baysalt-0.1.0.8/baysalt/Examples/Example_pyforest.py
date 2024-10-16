#!/Users/christmas/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#  日期 : 2024/3/21 14:56
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""
# ~/.pyforest/user_imports.py
# https://github.com/8080labs/pyforest/
"""
from pyforest import *

print(active_imports())    # 输出导入的模块
print(lazy_imports())

pd = LazyImport("import pandas as pd")
np = LazyImport("import numpy as np")
dd = LazyImport("from dask import dataframe as dd")
