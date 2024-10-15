#!/opt/homebrew/anaconda3/envs/quantfin/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/11 上午11:52
# @Author  : @Zhenxi Zhang
# @File    : influx_conn.py
# @Software: PyCharm

import logging
import warnings
from typing import Optional, Dict, List, Tuple

import pandas as pd
import pytz
from LockonToolkit.decorator_utils import func_logging
from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError

from ._tricks import LogUnit
from ._version_params import _DATAFRAME_FORMAT_ERROR_MSG


class DataFrameFormatError(Exception):
    """自定义异常类，用于处理DataFrame格式错误"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        logging.error(message)
        logging.error(_DATAFRAME_FORMAT_ERROR_MSG)


class InfluxConn(LogUnit):
    """
    InfluxDB连接类，继承自日志单元基类，用于初始化与InfluxDB的连接。

    参数:
      influx_conf_fp (str): InfluxDB配置文件路径。
      instance_id (int): 实例的唯一标识符。
      logger_level (int): 日志级别。
      logs_writer (logging.Handler | None): 日志处理器实例，默认为 None。

    属性:
      _client (InfluxDBClient): 与InfluxDB交互的客户端实例。
    """

    def __init__(
        self,
        influx_conf_fp: str,
        instance_id: int,
        logger_level: int,
        logs_writer: Optional[logging.Handler] = None,
    ) -> None:

        # 初始化InfluxDB客户端
        self._client: InfluxDBClient = InfluxDBClient.from_config_file(
            influx_conf_fp, encoding="utf-8"
        )

        # 调用父类构造函数完成日志记录器的初始化
        super().__init__(instance_id, logger_level, logs_writer)

    @func_logging
    def test_connection(self) -> None:
        """
        测试与InfluxDB的连接。

        返回:
            None
        """
        try:
            self._client.ping()
            self.debug(f"{self.id} Connection established")
        except Exception as err:
            self.warn(f"{self.id} Connection failed: {err}")

    @func_logging
    def get_all_buckets_name(self) -> List[str]:
        """
        获取所有的buckets名称列表。

        返回:
            List[str]: 所有buckets名称的列表。
        """
        buckets = self._client.buckets_api().find_buckets().buckets
        return [bucket.name for bucket in buckets]

    @func_logging
    def is_in_bucket(self, bucket_name: str) -> bool:
        """
        检查指定的bucket名称是否存在于InfluxDB中。

        参数:
            bucket_name (str): 要检查的bucket名称。

        返回:
            bool: 如果bucket存在则返回True，否则返回False。
        """
        return bucket_name in self.get_all_buckets_name()

    @func_logging
    def get_measurements(self, bucket_name: str) -> List[str]:
        """
        获取指定bucket中的所有measurements名称。

        参数:
            bucket_name (str): 要获取measurements的bucket名称。

        返回:
            List[str]: measurements名称的列表。
        """
        query = f'import "influxdata/influxdb/schema" schema.measurements(bucket: "{bucket_name}")'
        results = self._client.query_api().query(query)[0]
        return [record.values["_value"] for record in results.records]

    class BatchingCallback:
        def __init__(self, root: "InfluxConn") -> None:
            self.root: InfluxConn = root

        def success(self, conf: Tuple[str, str, str], data: str) -> None:
            """
            成功写入batch时的回调。

            参数:
                conf (Tuple[str, str, str]): 写入配置。
                data (str): 写入的数据。

            返回:
                None
            """
            self.root.debug(f"Written batch: {conf}, data: {data}")

        def error(
            self, conf: Tuple[str, str, str], data: str, exception: InfluxDBError
        ) -> None:
            """
            写入batch失败时的回调。

            参数:
                conf (Tuple[str, str, str]): 写入配置。
                data (str): 写入的数据。
                exception (InfluxDBError): 异常。

            返回:
                None
            """
            self.root.error(
                f"Cannot write batch: {conf}, data: {data} due: {exception}"
            )

        def retry(
            self, conf: Tuple[str, str, str], data: str, exception: InfluxDBError
        ) -> None:
            """
            写入batch需要重试时的回调。

            参数:
                conf (Tuple[str, str, str]): 写入配置。
                data (str): 写入的数据。
                exception (InfluxDBError): 异常。

            返回:
                None
            """
            self.root.debug(
                f"Retryable error occurs for batch: {conf}, data: {data} retry: {exception}"
            )

    @staticmethod
    @func_logging
    def validate_and_convert_dataframe(_tested_df: pd.DataFrame) -> pd.DataFrame:
        """
        检查并转换给定的DataFrame，使其符合以下条件：
        - 索引为pd.Timestamp类型（如果不是，则尝试转换）
        - 包含至少两列数据
        - 其中一列的列名为'id_code'

        参数:
            _tested_df (pd.DataFrame): 要验证和转换的DataFrame。

        返回:
            pd.DataFrame: 如果转换成功则返回转换后的DataFrame。

        抛出:
            DataFrameFormatError: 如果DataFrame不符合格式要求。
        """
        # 尝试将索引转换为pd.Timestamp类型
        try:
            _tested_df.index = pd.to_datetime(_tested_df.index)
        except Exception as e:
            raise DataFrameFormatError(f"无法将索引转换为pd.Timestamp类型: {e}")

        # 检查DataFrame至少包含两列数据
        if len(_tested_df.columns) < 2:
            raise DataFrameFormatError("DataFrame 至少需要包含两列数据")

        # 检查是否存在名为'id_code'的列
        if "id_code" not in _tested_df.columns:
            raise DataFrameFormatError("DataFrame 必须包含名为 'id_code' 的列")

        return _tested_df

    @func_logging
    def write_df_batching(
        self,
        input_df: pd.DataFrame,
        bucket_name: str,
        measurement_name: str,
        tag_columns: Optional[List[str]] = None,
        _timezone: str = "Asia/Shanghai",
    ) -> None:
        """
        以批量方式写入DataFrame到InfluxDB。

        参数:
            input_df (pd.DataFrame): 要写入的DataFrame。
            bucket_name (str): 目标bucket名称。
            measurement_name (str): measurement名称。
            tag_columns (Optional[List[str]]): 标签列名列表。
            _timezone (str): 时间区域。

        返回:
            None
        """
        input_df = self.validate_and_convert_dataframe(input_df)

        if tag_columns is None:
            tag_columns = ["id_code"]

        callback = self.BatchingCallback(self)
        with self._client.write_api(
            success_callback=callback.success,
            error_callback=callback.error,
            retry_callback=callback.retry,
        ) as wapi:
            from influxdb_client.extras import pd as pd_ex

            wapi.write(
                bucket=bucket_name,
                record=pd_ex.DataFrame(input_df),
                data_frame_measurement_name=measurement_name,
                data_frame_tag_columns=tag_columns,
                data_frame_timestamp_timezone=_timezone,
            )

    @func_logging
    def write_df(
        self,
        input_df: pd.DataFrame,
        bucket_name: str,
        measurement_name: str,
        tag_columns: Optional[List[str]] = None,
        _timezone: str = "Asia/Shanghai",
    ) -> None:
        """
        写入DataFrame到InfluxDB。

        参数:
            input_df (pd.DataFrame): 要写入的DataFrame。
            bucket_name (str): 目标bucket名称。
            measurement_name (str): measurement名称。
            tag_columns (Optional[List[str]]): 标签列名列表。
            _timezone (str): 时间区域。

        返回:
            None
        """
        if tag_columns is None:
            tag_columns = ["id_code"]

        callback = self.BatchingCallback(self)
        with self._client.write_api(
            success_callback=callback.success,
            error_callback=callback.error,
            retry_callback=callback.retry,
        ) as wapi:
            wapi.write(
                bucket=bucket_name,
                record=self.validate_and_convert_dataframe(input_df),
                data_frame_measurement_name=measurement_name,
                data_frame_tag_columns=tag_columns,
                data_frame_timestamp_timezone=_timezone,
            )

    @staticmethod
    def compose_influx_query(
        bucket: str,
        measurement: str,
        start_date: str,
        end_date: str,
        filter_tags: Optional[Dict[str, str]] = None,
        filter_fields: Optional[str] = None,
    ) -> str:
        """
        构建InfluxDB查询语句。

        参数:
            bucket (str): bucket名称。
            measurement (str): measurement名称。
            start_date (str): 开始日期。
            end_date (str): 结束日期。
            filter_tags (Optional[Dict[str, str]]): 过滤标签。
            filter_fields (Optional[str]): 过滤字段。

        返回:
            str: 查询语句。
        """
        prefix = (
            f'from(bucket:"{bucket}") |> range(start:{start_date}, stop:{end_date}) '
        )
        suffix = (
            '|> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
        )
        filter_sentence = ""

        if measurement != "" or filter_tags is not None or filter_fields is not None:
            prefix += "|> filter(fn: (r) => "
            suffix = ")" + suffix

        # 使用参数化查询
        if measurement != "":
            filter_sentence += f'r["_measurement"] == "{measurement}"'

        if filter_fields:
            try:
                field_list = filter_fields.split(",")
            except Exception as e:
                raise ValueError("Invalid filter_fields format.") from e
            code_field_filter_sentence = " or ".join(
                f'r["_field"] == "{field}"' for field in field_list
            )
            filter_sentence += f" and ({code_field_filter_sentence})"

        if filter_tags:
            try:
                tag_name = list(filter_tags.keys())[0]
                tags_list = filter_tags[tag_name].split(",")
            except Exception as e:
                raise ValueError("Invalid filter_fields format.") from e
            code_tag_filter_sentence = " or ".join(
                f'r["{tag_name}"] == "{tag}"' for tag in tags_list
            )
            filter_sentence += f" and ({code_tag_filter_sentence})"

        return prefix + filter_sentence + suffix

    @func_logging
    def query_df(
        self,
        bucket: str,
        measurement: str = "",
        start_date: str = "0",
        end_date: str = "now()",
        filter_tags: Optional[Dict[str, str]] = None,
        filter_fields: Optional[str] = "",
        drop_influx_cols: bool = True,
        tz_info: str = "Asia/Shanghai",
    ) -> pd.DataFrame:
        """
        从InfluxDB查询DataFrame。

        参数:
            bucket (str): bucket名称。
            measurement (str): measurement名称。
            start_date (str): 开始日期。
            end_date (str): 结束日期。
            filter_tags (Optional[Dict[str, str]]): 过滤标签。
            filter_fields (Optional[str]): 过滤字段。
            drop_influx_cols (bool): 是否删除InfluxDB内部列。
            tz_info (str): 时间区域。

        返回:
            pd.DataFrame: 查询结果。
        """
        if filter_tags is None:
            filter_tags = {}

        exist_measurements = self.get_measurements(bucket)
        if measurement not in exist_measurements:
            raise ValueError(f"measurement {measurement} not exist in bucket {bucket}")
        if start_date == end_date:
            start_date = (pd.to_datetime(end_date) - pd.Timedelta(days=1)).strftime(
                "%Y-%m-%d"
            )
        query_sql = self.compose_influx_query(
            bucket, measurement, start_date, end_date, filter_tags, filter_fields
        )
        return self.query_by_sql(query_sql, drop_influx_cols, tz_info)

    @func_logging
    def query_by_sql(
        self, sql: str, drop_influx_cols: bool = True, tz_info: str = "Asia/Shanghai"
    ) -> pd.DataFrame:
        """
        通过SQL查询InfluxDB并返回DataFrame。

        参数:
            sql (str): SQL查询语句。
            drop_influx_cols (bool): 是否删除InfluxDB内部列。
            tz_info (str): 时间区域。

        返回:
            pd.DataFrame: 查询结果。
        """
        self.debug(sql)
        query_api = self._client.query_api()
        df = query_api.query_data_frame(sql)

        # 删除指定的InfluxDB内部列
        if drop_influx_cols:
            columns_to_drop = ["_start", "_stop", "result", "table"]
            df.drop(columns=columns_to_drop, inplace=True, errors="ignore")

        # 设置时间区域
        _tz = pytz.timezone(tz_info)

        # 如果DataFrame为空，则直接返回空DataFrame
        if df.empty:
            return pd.DataFrame()

        # 复制时间列，并将其转换为指定的时间区域
        tmp_series = df["_time"].copy()
        tmp_series = pd.to_datetime(tmp_series).dt.tz_convert(_tz)

        # 忽略警告信息
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            df_time = tmp_series.dt.date
            df["time"] = df_time

        # 设置新的索引为'time'
        return df.set_index("time")

    @func_logging
    def delete_by_predicate(
        self,
        bucket_name: str,
        predicate_lang: str = "",
        _start_time: str = "0",
        _end_time: str = "now()",
    ) -> None:
        """
        根据给定的谓词删除InfluxDB中的数据。

        参数:
            bucket_name (str): 要操作的bucket名称。
            predicate_lang (str): 谓词语言表达式。
            _start_time (str): 删除数据的开始时间。
            _end_time (str): 删除数据的结束时间。

        返回:
            None
        """
        dapi = self._client.delete_api()
        dapi.delete(_start_time, _end_time, predicate_lang, bucket=bucket_name)
