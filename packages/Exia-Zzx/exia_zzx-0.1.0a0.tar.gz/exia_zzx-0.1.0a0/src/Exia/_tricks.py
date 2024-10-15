#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/11 下午5:15
# @Author  : @Zhenxi Zhang
# @File    : _tricks.py
# @Software: PyCharm

import logging
from abc import ABC
from typing import Callable

import numpy as np
from LockonToolkit.decorator_utils import func_logging


class LogUnit(ABC):
    """
    日志单元基类，用于初始化日志记录器及其配置。

    参数:
      instance_id (str | int): 实例的标识符，默认为 -1。
      logger_level (int): 日志级别，默认为 logging.DEBUG。
      logs_writer (logging.Handler): 日志处理器实例，默认为 None。

    属性:
      id (str | int): 实例ID。
      _logger (Logger): 日志记录器实例。
      info (Callable): 日志记录器的 info 方法。
      warn (Callable): 日志记录器的 warning 方法。
      debug (Callable): 日志记录器的 debug 方法。
      error (Callable): 日志记录器的 error 方法。
      critical (Callable): 日志记录器的 critical 方法。
    """

    @func_logging
    def __init__(
        self,
        instance_id: str | int = -1,
        logger_level: int = logging.DEBUG,
        logs_writer: logging.Handler = None,
    ) -> None:

        self.id: str | int = instance_id  # 实例ID
        self._logger = logging.getLogger(f"{__name__}.{instance_id}")
        self._logger.setLevel(logger_level)
        if logs_writer is not None:
            self._logger.addHandler(logs_writer)

        self.info: Callable = self._logger.info  # 日志记录器的info方法
        self.warn: Callable = self._logger.warning  # 日志记录器的warning方法
        self.debug: Callable = self._logger.debug  # 日志记录器的debug方法
        self.error: Callable = self._logger.error  # 日志记录器的error方法
        self.critical: Callable = self._logger.critical  # 日志记录器的critical方法


class MetaNeuron(LogUnit):
    cerebro = None

    def link2cerebrum(self, cerebro):
        """
        将当前实例与 cerebrum 关联。
        """
        self.cerebro = cerebro


def split_codes_into_chunks(neuro, raw_list, times=5):
    """
    将代码列表分割成多个子列表（块）。

    Parameters
    ----------
    neuro: MetaNeuron
        调用此函数的神经单元self

    raw_list : list
        需要分割的代码列表。
    times : int, optional
        分割的块数，默认为 5。

    Returns
    -------
    list
        包含分割后的代码块的列表。

    Raises
    ------
    ValueError
        如果 `test_codes` 不是列表，或者 `times` 不是正整数。
    """
    # 输入验证
    if not isinstance(raw_list, list):
        neuro.error(f"test_codes must be a list.Input-{raw_list}")
        raise ValueError("test_codes must be a list.")
    if not isinstance(times, int) or times <= 0:
        neuro.error(f"times must be a positive integer.Input-{times}")
        raise ValueError("times must be a positive integer.")

    codes_num = len(raw_list)
    # 提前计算每个分段的结束索引
    chunk_sizes = [int(np.ceil((i + 1) * codes_num / times)) for i in range(times)]

    res = []
    start_index = 0
    for end_index in chunk_sizes:
        # 显式地检查边界条件
        end_index = min(end_index, codes_num)
        res.append(raw_list[start_index:end_index])
        start_index = end_index
    return res
