#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Saka
@File    ：data_api.py
@Author  ：zhenxi_zhang@cx
@Date    ：2024/9/11 下午4:56
@explain : 文件说明
"""
import concurrent.futures
from abc import ABCMeta, abstractmethod
from datetime import date
from typing import Dict, Any, Union
from typing import List, Optional

import LockonToolkit.dateutils as kit_dt
import pandas as pd
from LockonToolkit.decorator_utils import func_logging
from WindPy import w

from .._tricks import MetaNeuron, split_codes_into_chunks
from .._version_params import _DATA_SOURCE_FUNC


def wsd_res_df_formatted(df: pd.DataFrame, fields: list[str]) -> pd.DataFrame:
    """
    对给定的数据框进行格式化处理，使其符合特定的数据格式要求。

    参数:
        df (pd.DataFrame): 原始数据框，通常包含多列数据。
        fields (list[str]): 需要展开并保留的字段列表。

    返回:
        pd.DataFrame: 格式化后的数据框，其中除了'id_code'外还包括fields中指定的所有字段，
                      并且原始数据中的多余列已经被展开成单列形式。

    示例:
        如果原始df包含['id_code', 'value1', 'value2']三列，
        且fields为['value1', 'value2']，
        则返回的df结构为:
        - id_code: 来自原始df的第一列。
        - value1: 来自原始df的第二列，作为展开后的变量。
        - value2: 来自原始df的第三列，作为展开后的变量。
    """

    # 使用melt函数将DataFrame转换成长格式，忽略默认索引
    melted_df = df.melt(ignore_index=False)

    # 创建新的列名列表，以'id_code'开始，后跟fields中的元素
    new_columns = ["id_code"] + fields

    # 更新DataFrame的列名为新的列名列表
    melted_df.columns = new_columns

    # 返回格式化后的DataFrame
    return melted_df


class DataSourceNeuron(metaclass=ABCMeta):
    """
    数据源神经元抽象基类，用于定义获取金融数据的方法。

    这个类作为抽象基类，定义了一系列方法，子类需要实现这些方法来提供具体的数据访问功能。
    """

    @abstractmethod
    def get_former_trade_calender(self, start_date: date, end_date: date) -> List[date]:
        """
        获取两个日期之间的交易日历。

        参数:
            start_date (date): 开始日期。
            end_date (date): 结束日期。

        返回:
            List[date]: 在[start_date, end_date]区间内的所有交易日日期列表。

        抛出:
            NotImplementedError: 如果子类没有实现这个方法。
        """
        pass

    @abstractmethod
    def get_total_ashare_code(self, _date: date) -> List[str]:
        """
        获取在指定日期下的所有A股股票代码。

        参数:
            date (date): 查询的日期。

        返回:
            List[str]: 所有A股股票的代码列表。

        抛出:
            NotImplementedError: 如果子类没有实现这个方法。
        """
        pass

    @abstractmethod
    def query(self) -> Optional[dict]:
        """
        查询数据的一般方法。

        返回:
            Optional[dict]: 查询的结果，可能为None如果查询失败或者没有数据。

        抛出:
            NotImplementedError: 如果子类没有实现这个方法。
        """
        pass

    @abstractmethod
    def query_multithread(self) -> Optional[dict]:
        """
        使用多线程查询数据的方法。

        返回:
            Optional[dict]: 查询的结果，可能为None如果查询失败或者没有数据。

        抛出:
            NotImplementedError: 如果子类没有实现这个方法。
        """
        pass


class WindDataNeuron(MetaNeuron):
    @staticmethod
    def check_w_decorator(func):
        """
        一个装饰器，用于在调用被装饰的函数前检查 `w` 的连接状态。

        如果 `w` 没有连接，则启动 `w`。
        """

        def wrapper(*args, **kwargs):
            # 在调用原始函数前检查 `w` 的连接状态
            if not w.isconnected():
                w.start()
            return func(*args, **kwargs)

        return wrapper

    @func_logging
    @check_w_decorator
    def get_former_trade_calender(self, start_date, end_date):
        """
        从Wind数据库中获取时间段内的交易日历，含头含尾
        Parameters
        ----------
        start_date : 开始日期，格式为"YYYY-MM-DD"
        end_date : 结束日期，格式为"YYYY-MM-DD"

        Returns
        -------
        list
            包含从开始日期到结束日期范围内所有交易日的日期列表，格式为date对象
        """
        # response = w.wsd(used_code, "pct_chg", start_date, end_date, "", usedf=True)[1]
        # return response.index.tolist()
        response = w.tdays(start_date, end_date).Data[0]
        ret = [i.date() for i in response]
        return ret

    @func_logging
    @check_w_decorator
    def get_total_ashare_code(self, _date):
        """
        根据给定日期获取所有 A 股的 Wind 代码及证券名称。

        Parameters
        ----------
        _date : datetime-like
            需要获取数据的日期。

        Returns
        -------
        pandas.DataFrame
            包含 'wind_code' 和 'sec_name' 两列的 DataFrame。
        """

        # 确保 Wind 已经连接
        if not w.isconnected():
            w.start()

        # 构建请求参数
        request_params = f"date={kit_dt.date2str(_date)};sectorid=a001010100000000"

        try:
            self.debug(f"get_total_ashare_code_from_wind")
            # 发送请求
            response = w.wset("sectorconstituent", request_params, usedf=True)

            # 检查响应
            # resp_code = response[0]  # 可以保留这部分用于调试
            df = response[1]

            # 返回结果
            return df[["wind_code", "sec_name"]]

        except Exception as e:
            # 更具体的错误处理
            error_message = f"Wind 获取 A 股代码失败: {type(e).__name__} - {str(e)}"
            self.error(error_message)
            raise ValueError(error_message) from e

    @func_logging
    @check_w_decorator
    def query(
        self, wind_query_type: str, *args: Union[str, List[str]]
    ) -> Union[pd.DataFrame, None]:
        """
        根据指定的 Wind 查询类型执行查询。

        参数:
            wind_query_type (str): 需要执行的查询类型，例如 "wsd" 或 "wset"。
            *args (Union[str, List[str]]): 查询所需的额外参数，这些参数根据查询类型的不同而不同。

        返回:
            Union[pd.DataFrame, None]: 查询结果的 DataFrame 或者在出现错误时返回 None。

        抛出:
            ValueError: 如果提供的查询类型无效。

        示例:
            调用 `query("wsd", ["code1", "code2"], "pct_chg", "2023-01-01", "2023-12-31")`
            将会查询 `code1` 和 `code2` 的 `pct_chg` 数据。
        """
        qtypes = _DATA_SOURCE_FUNC["Wind"]
        if wind_query_type not in qtypes:
            self.error(f"Invalid wind query type: {wind_query_type}")
            raise ValueError(f"Invalid wind query type: {wind_query_type}")

        if wind_query_type == "wsd":
            # 提取数据字段作为索引
            field = args[1]
            wsd_result = self._wsd_query(*args)
            print(wsd_result)
            return wsd_res_df_formatted(wsd_result, [field])

        elif wind_query_type == "wset":
            self.debug("wset_query")
            return self._wset_query(*args)

    @func_logging
    @check_w_decorator
    def query_multithread(
        self, wind_query_type: str, *args: Union[str, List[str]]
    ) -> Optional[pd.DataFrame]:
        """
        使用多线程根据指定的 Wind 查询类型执行查询。

        参数:
            wind_query_type (str): 需要执行的查询类型，例如 "wsd"。
            *args (Union[str, List[str]]): 查询所需的额外参数，这些参数根据查询类型的不同而不同。

        返回:
            Optional[pd.DataFrame]: 查询结果的 DataFrame，或者在出现错误时返回 None。

        抛出:
            ValueError: 如果提供的查询类型无效。

        示例:
            调用 `query_multithread("wsd", ["code1", "code2"], "pct_chg", "2023-01-01", "2023-12-31")`
            将会使用多线程查询 `code1` 和 `code2` 的 `pct_chg` 数据。
        """
        qtypes = _DATA_SOURCE_FUNC["Wind"]
        if wind_query_type not in qtypes:
            self.error(f"Invalid wind query type: {wind_query_type}")
            raise ValueError(f"Invalid wind query type: {wind_query_type}")

        if wind_query_type == "wsd":
            return self._wsd_query_multi_threads(*args)

    @func_logging
    @check_w_decorator
    def _wset_query(self, wset_query: str, args: Dict[str, Any]) -> pd.DataFrame:
        """
        执行 Wind 数据集查询。

        参数:
            wset_query (str): 数据集代码。
            args (Dict[str, Any]): 查询参数字典。

        返回:
            pd.DataFrame: 查询结果的数据帧。

        示例:
            调用 `_wset_query("sectorconstituent", {"sectorid": "a001010100000000"})`
            将会返回对应板块的成分股列表。
        """
        # 打印调试信息（注释掉实际使用时可以删除）
        # print(wset_query, args)

        # 执行 Wind 数据集查询并返回结果
        return w.wset(wset_query, args, usedf=True)[1]

    @func_logging
    @check_w_decorator
    def _wsd_query(
        self, codes, wind_data_field, start_date, end_date, opt="", wind_batch_times=1
    ):
        """
        从 Wind.wsd获取数据的函数。该函数按批次从 Wind 数据库中提取股票或其他金融数据，以提高效率和避免连接问题。

        Parameters
        ----------
        codes : list
            需要获取数据的股票代码列表。
        wind_data_field : str
            需要获取的 Wind 数据字段，例如 pct_chg 等。
        start_date : str
            数据的起始日期, 格式为 YYYY-MM-DD。
        end_date : str
            数据的结束日期, 格式为 YYYY-MM-DD。
        wind_batch_times : int, optional
            分批请求数据的批次数量，用于控制每次请求的代码数量，避免因请求过多导致的问题。
            默认值为 1，表示不分批。
        opt:str,optional
            表示用于wind查询的可选项，如ALLDAYS等参数

        Returns
        -------
        pandas.DataFrame or None
            包含所请求数据的 DataFrame，如果发生错误则返回 None。

        Raises
        ------
        ValueError
            如果 `wind_batch_times` 为 None 或者不是正整数。
        """

        if wind_batch_times is None:
            raise ValueError("Wind batch times cannot be None")

        if start_date == end_date:
            # 如果只查询单日数据，为了防止wind返回的结构不一致，这里将起始日前移一天
            start_date = kit_dt.get_last_trade_date(start_date)

        try:
            i = 0
            if wind_batch_times > 0:
                ret_total = []
                code_sets = split_codes_into_chunks(self, codes, wind_batch_times)
                for codes_chunk in code_sets:
                    i += 1
                    data = w.wsd(
                        codes_chunk,
                        wind_data_field,
                        start_date,
                        end_date,
                        opt,
                        usedf=True,
                    )[1]
                    ret_total.append(data)
                    self.debug(f"No. {i} batch data fetching")

                # 合并数据
                result = pd.concat(ret_total, axis=1)

                if len(codes) == 1:
                    result.columns = [codes[0]]

                return result
            else:
                self.error(
                    f"Wind batch times should be a positive integer,input-{wind_batch_times}"
                )
                raise ValueError("Wind batch times should be a positive integer")
        except Exception as e:
            self.error(f"Error occurred while fetching data: {e}")
            return None

    @func_logging
    @check_w_decorator
    def _wsd_query_multi_threads(
        self, codes, wind_data_field, start_date, end_date, opt="", wind_batch_times=1
    ):
        """
        从 Wind.wsd 多线程获取数据的函数。该函数按批次从 Wind 数据库中提取股票或其他金融数据，以提高效率和避免连接问题。

        Parameters
        ----------
        codes : list
            需要获取数据的股票代码列表。
        wind_data_field : str
            需要获取的 Wind 数据字段，例如 pct_chg 等。
        start_date : str
            数据的起始日期, 格式为 YYYY-MM-DD。
        end_date : str
            数据的结束日期, 格式为 YYYY-MM-DD。
        wind_batch_times : int, optional
            分批请求数据的批次数量，用于控制每次请求的代码数量，避免因请求过多导致的问题。
            默认值为 1，表示不分批。

        Returns
        -------
        pandas.DataFrame or None
            包含所请求数据的 DataFrame，如果发生错误则返回 None。

        Raises
        ------
        ValueError
            如果 `wind_batch_times` 为 None 或者不是正整数。
        """
        if not w.isconnected():
            w.start()

        if wind_batch_times is None:
            raise ValueError("Wind batch times cannot be None")

        if start_date == end_date:
            # 如果只查询单日数据，为了防止 Wind 返回的结构不一致，这里将起始日前移一天
            start_date = kit_dt.get_last_trade_date(start_date)

        try:
            if wind_batch_times > 0:
                code_sets = split_codes_into_chunks(self, codes, wind_batch_times)

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [
                        executor.submit(
                            w.wsd,
                            codes_chunk,
                            wind_data_field,
                            start_date,
                            end_date,
                            opt,
                            usedf=True,
                        )
                        for codes_chunk in code_sets
                    ]

                    # 等待所有任务完成
                    results = [future.result()[1] for future in futures]

                # 合并数据
                result = pd.concat(results, axis=1)
                return result
            else:
                self.error(
                    f"Wind batch times should be a positive integer,input-{wind_batch_times}"
                )
                raise ValueError("Wind batch times should be a positive integer")
        except Exception as e:
            self.error(f"Error occurred while fetching data: {e}")
            return None
