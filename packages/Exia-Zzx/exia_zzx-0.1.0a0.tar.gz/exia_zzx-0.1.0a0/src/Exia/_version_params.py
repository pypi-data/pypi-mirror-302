#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/14 上午11:12
# @Author  : @Zhenxi Zhang
# @File    : _version_params.py
# @Software: PyCharm

_DATAFRAME_FORMAT_ERROR_MSG = (
    "将df传入数据库，df的格式规范应该为:\n"
    "---------------------------------------------------------\n"
    "---index       id_code        field_name(e.g daily_Ret)\n"
    "2024-01-02     000001.SZ        0.025\n"
    "2024-01-02     000002.SZ        0.032\n"
    "2024-01-03     000001.SZ        0.025\n"
    "2024-01-03     000002.SZ        0.032\n"
    ".....\n"
    "---------------------------------------------------------\n"
)

_AVAILABLE_DATA_SOURCE = ["Wind"]
_DATA_SOURCE_FUNC = {"Wind": ["wsd", "wset"]}
