"""移动端网页搜索结果模型类型注释文件

此模块中定义了所有现有移动端网页搜索内所有模块的结果模型类型注释类，便于现代编辑器自动补全，提供更好的编码体验。
"""
from datetime import datetime, time
from baiduspider.mobile.models.typings.typings_web import *
from baiduspider.models import get_attr, convert_time


class WebVideoDetail(WebVideoDetail):
    """网页搜索视频详情搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebVideoDetail`类。
    """

    def __init__(self) -> None:
        self.author = ""
        self.author_avatar = ""
        self.duration = None
        self.labels = []
        self.poster = ""
        self.pub_time = None
        self.title = ""
        self.url = ""
        self.video_num = 0
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebVideoDetail:
        __returns = WebVideoDetail()
        __returns.plain = plain
        __returns.author = get_attr(plain, "author")
        __returns.author_avatar = get_attr(plain, "author_avatar")
        try:
            __returns.duration = time(minute=int(get_attr(plain, "duration").split(":")[0]), second=int(get_attr(plain, "duration").split(":")[1]))
        except:
            __returns.duration = None
        for i in get_attr(plain, "labels"):
            __returns.labels.append(i)
        __returns.poster = get_attr(plain, "poster")
        __returns.pub_time = convert_time(get_attr(plain, "pub_time"))
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        __returns.video_num = get_attr(plain, "video_num")
        return __returns


class WebVideoTag(WebVideoTag):
    """网页搜索视频标签搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebVideoTag`类。
    """

    def __init__(self) -> None:
        self.text = ""
        self.url = ""
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebVideoTag:
        __returns = WebVideoTag()
        __returns.plain = plain
        __returns.text = get_attr(plain, "text")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebVideo(WebVideo):
    """网页搜索视频搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebVideo`类。
    """

    def __init__(self) -> None:
        self.results = []
        self.tags = []
        self.plain = {}

    @staticmethod
    def _build_instance(plain: dict) -> WebVideo:
        __returns = WebVideo()
        __returns.plain = plain
        for i in get_attr(plain, "results"):
            __returns.results.append(WebVideoDetail._build_instance(i))
        for i in get_attr(plain, "tags"):
            __returns.tags.append(WebVideoTag._build_instance(i))
        return __returns


class WebShortVideo(WebShortVideo):
    """网页搜索短视频搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebShort_video`类。
    """

    def __init__(self) -> None:
        self.author = ""
        self.author_avatar = ""
        self.play_times = 0
        self.poster = ""
        self.title = ""
        self.url = ""
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebShortVideo:
        __returns = WebShortVideo()
        __returns.plain = plain
        __returns.author = get_attr(plain, "author")
        __returns.author_avatar = get_attr(plain, "author_avatar")
        __returns.play_times = get_attr(plain, "play_times")
        __returns.poster = get_attr(plain, "poster")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebBaikeSection(WebBaikeSection):
    """网页搜索百科目录搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebBaikeSection`类。
    """

    def __init__(self) -> None:
        self.text = ""
        self.url = ""
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebBaikeSection:
        __returns = WebBaikeSection()
        __returns.plain = plain
        __returns.text = get_attr(plain, "text")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebBaike(WebBaike):
    """网页搜索百科搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebBaike`类。
    """

    def __init__(self) -> None:
        self.des = ""
        self.labels = []
        self.origin = ""
        self.poster = ""
        self.sections = []
        self.title = ""
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebBaike:
        __returns = WebBaike()
        __returns.plain = plain
        __returns.des = get_attr(plain, "des")
        for i in get_attr(plain, "labels"):
            __returns.labels.append(i)
        __returns.origin = get_attr(plain, "origin")
        __returns.poster = get_attr(plain, "poster")
        if get_attr(plain, "sections") is not None:
            for i in get_attr(plain, "sections"):
                __returns.sections.append(WebBaikeSection._build_instance(i))
        __returns.title = get_attr(plain, "title")
        return __returns


class WebReyi(WebReyi):
    """网页搜索热议搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebReyi`类。
    """

    def __init__(self) -> None:
        self.author = ""
        self.author_avatar = ""
        self.comments = 0
        self.des = ""
        self.images = []
        self.likes = 0
        self.origin = ""
        self.pub_time = ""
        self.site = ""
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebReyi:
        __returns = WebReyi()
        __returns.plain = plain
        __returns.author = get_attr(plain, "author")
        __returns.author_avatar = get_attr(plain, "author_avatar")
        __returns.comments = get_attr(plain, "comments")
        __returns.des = get_attr(plain, "des")
        if get_attr(plain, "images") is not None:
            for i in get_attr(plain, "images"):
                __returns.images.append(i)
        __returns.likes = get_attr(plain, "likes")
        __returns.origin = get_attr(plain, "origin")
        __returns.pub_time = get_attr(plain, "pub_time")
        __returns.site = get_attr(plain, "site")
        return __returns


class WebKnowledgeDetail(WebKnowledgeDetail):
    """网页搜索相关知识详情搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebKnowledgeDetail`类。
    """

    def __init__(self) -> None:
        self.des = ""
        self.image = ""
        self.title = ""
        self.url = ""
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebKnowledgeDetail:
        __returns = WebKnowledgeDetail()
        __returns.plain = plain
        __returns.des = get_attr(plain, "des")
        __returns.image = get_attr(plain, "image")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebKnowledge(WebKnowledge):
    """网页搜索相关知识搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebKnowledge`类。
    """

    def __init__(self) -> None:
        self.results = []
        self.title = ""
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebKnowledge:
        __returns = WebKnowledge()
        __returns.plain = plain
        for i in get_attr(plain, "results"):
            __returns.results.append(WebKnowledgeDetail._build_instance(i))
        __returns.title = get_attr(plain, "title")
        return __returns


class WebNormal(WebNormal):
    """网页搜索普通搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.WebNormal`类。
    """

    def __init__(self) -> None:
        self.des = ""
        self.image = ""
        self.title = ""
        self.url = ""
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: dict) -> WebNormal:
        __returns = WebNormal()
        __returns.plain = plain
        __returns.des = get_attr(plain, "des")
        __returns.image = get_attr(plain, "image")
        __returns.title = get_attr(plain, "title")
        __returns.url = get_attr(plain, "url")
        return __returns


class WebResult(WebResult):
    """网页搜索搜索结果模型类型注释类。

    详见`baiduspider.mobile.models.web.Web`类。
    """

    def __init__(self) -> None:
        self.video = None
        self.short_video = None
        self.baike = None
        self.reyi = None
        self.normal = []
        self.knowledge = None
        self.plain = {}
    
    @staticmethod
    def _build_instance(plain: list) -> WebResult:
        __returns = WebResult()
        __returns.plain = plain
        for p in plain:
            if get_attr(p, "type") == "result":
                __returns.normal.append(WebNormal._build_instance(p))
            elif get_attr(p, "type") == "video":
                __returns.video = WebVideo._build_instance(p)
            elif get_attr(p, "type") == "short_video":
                __returns.short_video = WebShortVideo._build_instance(p)
            elif get_attr(p, "type") == "reyi":
                __returns.reyi = WebReyi._build_instance(p)
            elif get_attr(p, "type") == "knowledge":
                __returns.knowledge = WebKnowledge._build_instance(p)
        return __returns
