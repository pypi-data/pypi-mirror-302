from typing import Any, Dict, Callable, Optional, Literal, List
from wisecon.types import BaseMapping, ResponseData, BaseRequestData


__all__ = [
    "KLineMapping",
    "KLine",
]


TypePeriod = Literal["1min", "5min", "15min", "30min", "60min", "1day", "1week", "1month"]


class KLineMapping(BaseMapping):
    """"""
    columns: Dict = {
        "open": "开盘",
        "close": "收盘",
        "high": "最高",
        "low": "最低",
        "change_pct": "涨跌幅",
        "change_amt": "涨跌额",
        "volume": "成交量",
        "turnover": "成交额",
        "amplitude": "振幅",
        "turnover_rate": "换手率"
    }


class KLine(BaseRequestData):
    """"""

    def __init__(
            self,
            code: Optional[str] = None,
            end: Optional[str] = "20500101",
            limit: Optional[int] = 120,
            period: Optional[TypePeriod] = "5min",
            adjust: Optional[Literal["前复权", "后赋权", "不赋权"]] = "前复权",
            verbose: Optional[bool] = False,
            logger: Optional[Callable] = None,
            **kwargs: Any
    ):
        self.code = code
        self.end = end
        self.limit = limit
        self.period = period
        self.adjust = adjust
        self.mapping = KLineMapping()
        self.verbose = verbose
        self.logger = logger
        self.kwargs = kwargs
        self.request_set(description="股票 k-line")

    def base_url(self) -> str:
        """"""
        base_url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
        return base_url

    def _adjust_type(self) -> int:
        """"""
        adjust_mapping = {"前复权": 1, "后赋权": 2, "不赋权": 0}
        return adjust_mapping.get(self.adjust, 1)

    def _period(self) -> str:
        """"""
        period_mapping = {
            "1min": "1", "5min": "5", "15min": "15", "30min": "30", "60min": "60",
            "1day": "101", "1week": "102", "1month": "103"
        }
        return period_mapping.get(self.period, "5")

    def params(self) -> Dict:
        """
        :return:
        """
        params = {
            "secid": f"0.{self.code}",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": self._period(),
            "fqt": self._adjust_type(),
            "end": self.end,
            "lmt": self.limit,
        }
        return params

    def clean_json(
            self,
            json_data: Optional[Dict],
    ) -> List[Dict]:
        response = json_data.get("data", {})
        data = response.pop("klines")
        self.metadata.response = response

        def trans_kline_data(line: str) -> Dict:
            """"""
            line_data = line.split(",")
            return dict(zip(list(self.mapping.columns.keys()), line_data))

        data = list(map(trans_kline_data, data))
        return data
