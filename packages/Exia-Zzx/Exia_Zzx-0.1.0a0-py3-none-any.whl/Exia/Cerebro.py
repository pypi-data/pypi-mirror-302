#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/14 上午11:14
# @Author  : @Zhenxi Zhang
# @File    : Cerebro.py
# @Software: PyCharm

# %%
from configparser import ConfigParser

from ._tricks import LogUnit
from ._version_params import _AVAILABLE_DATA_SOURCE
from .api import *


class Cerebro(LogUnit):
    DATA_SOURCE_LIST = _AVAILABLE_DATA_SOURCE

    @func_logging
    def __init__(
        self,
        cerebro_conf,
        bucket,
        data_source,
        instance_id,
        logger_level=logging.DEBUG,
        logs_writer=None,
    ):
        super().__init__(instance_id, logger_level, logs_writer)
        self.conf = ConfigParser()
        self.conf_fp = cerebro_conf
        self.conf.read(cerebro_conf, encoding="utf-8")

        self.influx_api = InfluxNeuron(
           self,instance_id, bucket, logs_writer, logger_level
        )

        if data_source not in self.DATA_SOURCE_LIST:
            self.error(f"{data_source} is not supported")
            raise ValueError
        if data_source == "Wind":
            self.data_api = WindDataNeuron(instance_id, logger_level, logs_writer)
        self.neuron_relink2cerebrum()

    def neuron_relink2cerebrum(self):
        """
        遍历类的所有属性，如果属性值是 `MetaNeuron` 的实例，则将其 `cerebrum` 属性设置为当前实例。

        Returns
        -------
        None
        """
        for neuron in vars(self):
            attr = getattr(self, neuron)
            if isinstance(attr, MetaNeuron):
                attr.link2cerebrum(self)
