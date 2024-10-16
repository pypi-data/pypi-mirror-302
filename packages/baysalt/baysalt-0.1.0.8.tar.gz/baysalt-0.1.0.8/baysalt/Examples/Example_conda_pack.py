#!/Users/christmas/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
#  日期 : 2024/3/21 14:28
#  作者 : Christmas
#  邮箱 : 273519355@qq.com
#  项目 : Project
#  版本 : python 3
#  摘要 :
"""

"""
import conda_pack

# Pack environment my_env into my_env.tar.gz
conda_pack.pack(name="my_env")

# Pack environment my_env into out_name.tar.gz
conda_pack.pack(name="my_env", output="out_name.tar.gz")

# Pack environment located at an explicit path into my_env.tar.gz
conda_pack.pack(prefix="/explicit/path/to/my_env")
