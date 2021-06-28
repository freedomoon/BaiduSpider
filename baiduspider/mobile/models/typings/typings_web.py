"""移动端网页搜索结果模型类型注释文件

此模块中定义了所有现有移动端网页搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime, time
from typing import List, Union


class WebVideoDetail(object):
    """网页搜索视频详情搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebVideoDetail`类。
    """

    def __init__(self) -> None:
        self.author: str
        self.author_avatar: str
        self.duration: time
        self.labels: List[str]
        self.poster: str
        self.pub_time: datetime
        self.title: str
        self.url: str
        self.video_num: int
        self.plain: dict


class WebVideoTag(object):
    """网页搜索视频标签搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebVideoTag`类。
    """

    def __init__(self) -> None:
        self.text: str
        self.url: str
        self.plain: dict


class WebVideo(object):
    """网页搜索视频搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebVideo`类。
    """

    def __init__(self) -> None:
        self.results: List[WebVideoDetail]
        self.tags: List[WebVideoTag]
        self.plain: dict


class WebShortVideo(object):
    """网页搜索短视频搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebShort_video`类。
    """

    def __init__(self) -> None:
        self.author: str
        self.author_avatar: str
        self.play_times: int
        self.poster: str
        self.title: str
        self.url: str
        self.plain: dict


class WebBaikeSection(object):
    """网页搜索百科目录搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebBaikeSection`类。
    """

    def __init__(self) -> None:
        self.text: str
        self.url: str
        self.plain: dict


class WebBaike(object):
    """网页搜索百科搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebBaike`类。
    """

    def __init__(self) -> None:
        self.des: str
        self.labels: List[str]
        self.origin: str
        self.poster: str
        self.sections: List[WebBaikeSection]
        self.title: str
        self.plain: dict


class WebReyi(object):
    """网页搜索热议搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebReyi`类。
    """

    def __init__(self) -> None:
        self.author: str
        self.author_avatar: str
        self.comments: int
        self.des: str
        self.images: List[str]
        self.likes: int
        self.origin: str
        self.pub_time: str
        self.site: str
        self.plain: dict


class WebKnowledgeDetail(object):
    """网页搜索相关知识详情搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebKnowledgeDetail`类。
    """

    def __init__(self) -> None:
        self.des: str
        self.image: str
        self.title: str
        self.url: str
        self.plain: dict


class WebKnowledge(object):
    """网页搜索相关知识搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebKnowledge`类。
    """

    def __init__(self) -> None:
        self.results: List[WebKnowledgeDetail]
        self.title: str
        self.plain: dict


class WebNormal(object):
    """网页搜索普通搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebNormal`类。
    """

    def __init__(self) -> None:
        self.des: str
        self.image: str
        self.title: str
        self.url: str
        self.plain: dict


class WebResult(object):
    """网页搜索搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.Web`类。
    """

    def __init__(self) -> None:
        self.video: Union[WebVideo, None]
        self.short_video: Union[WebShortVideo, None]
        self.baike: Union[WebBaike, None]
        self.reyi: Union[WebReyi, None]
        self.normal: List[WebNormal]
        self.knowledge: Union[WebKnowledge, None]
        self.plain: dict
