#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/14 下午1:13
# @Author  : @Zhenxi Zhang
# @File    : __init__.py.py
# @Software: PyCharm

import logging
from typing import Callable, List

import pandas as pd
from LockonToolkit.decorator_utils import func_logging

from .data_api import WindDataNeuron
from .._tricks import MetaNeuron
from ..influx_conn import InfluxConn


class InfluxNeuron(MetaNeuron):
    """
    InfluxNeuron类代表一个与InfluxDB交互的神经元单元，它继承自MetaNeuron基类。

    参数:
        instance_id (int): 实例ID，用于标识特定的神经元实例。
        bucket_name (str): InfluxDB中的存储桶名称，用于写入或查询数据。
        logs_writer (logging.Handler): 日志记录器，用于记录日志信息。
        logging_level (int): 日志记录级别。

    属性:
        _bucket (str): 存储桶名称。
        _conn (InfluxConn): 与InfluxDB的连接实例。
        query (Callable[[str], pd.DataFrame]): 查询方法，接收SQL查询语句并返回DataFrame结果。
        write (Callable[[pd.DataFrame, str], None]): 写入方法，接收DataFrame和测量名来写入数据。
        write_batching (Callable[[List[pd.DataFrame], str], None]): 批量写入方法，接收多个DataFrame和测量名进行批量写入。
        delete_by_predicate (Callable[[str], None]): 删除方法，根据提供的条件语句删除数据。
    """

    # _conn = None  # 类级别的InfluxDB连接引用

    @func_logging
    def __init__(
        self,
        cerebro: object,
        instance_id: int,
        bucket_name: str,
        logs_writer: logging.Handler,
        logging_level: int,
    ) -> None:
        # 设置存储桶名称
        self._bucket = bucket_name
        self.cerebro = cerebro

        # 调用父类构造函数完成日志记录器的初始化
        super().__init__(instance_id, logging_level, logs_writer)

        # 获取大脑(InfluxConn实例)中的连接
        self._conn = InfluxConn(self.cerebro.conf_fp, instance_id, logging_level, logs_writer)

        # 将InfluxDB操作绑定到当前实例上
        self.query: Callable[[str], pd.DataFrame] = self._conn.query_df
        self.write: Callable[[pd.DataFrame, str], None] = self._conn.write_df
        self.write_batching: Callable[[List[pd.DataFrame], str], None] = (
            self._conn.write_df_batching
        )
        self.delete_by_predicate: Callable[[str], None] = self._conn.delete_by_predicate
