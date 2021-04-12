from typing import List
from datetime import datetime

class WebNormal(object):
    """普通搜索结果模型类型注释类。

    详见`baiduspider.models.web.WebNormal`类。
    """
    def __init__(self) -> None:
        self.des: str
        self.origin: str
        self.title: str
        self.url: str
        self.time: datetime
        self.plain: dict

class WebCalc(object):
    def __init__(self) -> None:
        self.process: str
        self.result: str
        self.plain: dict

class WebNews(object):
    def __init__(self) -> None:
        self.author: str
        self.time: str
        self.url: datetime
        self.des: str
        self.plain: dict

class WebVideo(object):
    def __init__(self) -> None:
        self.cover: str
        self.origin: str
        self.length: str
        self.title: str
        self.url: str
        self.plain: dict

class WebBaike(object):
    def __init__(self) -> None:
        self.cover: str
        self.cover_type: str
        self.des: str
        self.title: str
        self.url: str
        self.plain: dict

class WebTiebaHot(object):
    def __init__(self) -> None:
        self.clicks: str
        self.replies: str
        self.title: str
        self.url: str
        self.plain: dict

class WebTieba(object):
    def __init__(self) -> None:
        self.cover: str
        self.des: str
        self.title: str
        self.followers: str
        self.total: str
        self.hot: List[WebTiebaHot]
        self.url: str
        self.plain: dict

class WebBlogBlogs(object):
    def __init__(self) -> None:
        self.title: str
        self.url: str
        self.des: str
        self.origin: str
        self.tags: List[str]
        self.plain: dict

class WebBlog(object):
    def __init__(self) -> None:
        self.title: str
        self.url: str
        self.blogs: List[WebBlogBlogs]
        self.plain: dict

class WebGitee(object):
    def __init__(self) -> None:
        self.title: str
        self.des: str
        self.url: str
        self.star: int
        self.fork: int
        self.watch: int
        self.license: str
        self.lang: str
        self.status: str
        self.plain: dict

class WebResult(object):
    def __init__(self) -> None:
        self.normal: List[WebNormal]
        self.total: int
        self.related: list
        self.calc: WebCalc
        self.news: List[WebNews]
        self.video: List[WebVideo]
        self.baike: WebBaike
        self.tieba: WebTieba
        self.blog: WebBlog
        self.gitee: WebGitee
        self.plain: list
