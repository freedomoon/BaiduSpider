"""BaiduSpider移动端爬虫"""
import datetime
import time as time_lib
from time import mktime, strptime, time
from typing import Tuple, Union
from urllib.parse import SplitResult, quote

import requests
from bs4 import BeautifulSoup

from baiduspider._spider import BaseSpider
from baiduspider.mobile.parser import MobileParser
from baiduspider.mobile.models.web import WebResult


__all__ = ["BaiduMobileSpider"]


class BaiduMobileSpider(BaseSpider):
    def __init__(self) -> None:
        super().__init__()
        # 爬虫名称（不是请求的，只是用来表识）
        self.spider_name = "BaiduSpider"
        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "Referer": "https://m.baidu.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        }
        self.parser = MobileParser()
        self.EMPTY = {"results": []}

    def search_web(self, query: str, pn: int = 1) -> WebResult:
        error = None
        try:
            text = quote(query, "utf-8")
            url = "https://m.baidu.com/s?word=%s&pn=%d" % (text, ((pn - 1) * 10))
            content = self._get_response(url)
            results = self.parser.parse_web(content)
        except Exception as err:
            error = err
        finally:
            self._handle_error(error, "BaiduSpider", "parse-web")
        return WebResult._build_instance(results["results"])
