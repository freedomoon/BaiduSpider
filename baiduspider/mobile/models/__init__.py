import re
from datetime import datetime, timedelta
from typing import Union


def convert_time(t) -> Union[datetime, None]:
    """将字符串形式的日期转换为`datetime.datetime`形式的时间"""
    if t is None:
        return None
    if t == "今天":
        return datetime.now()
    if "-" in t and len(t.split("-")) == 2:
        t = str(datetime.now().year) + "-" + t
    flag = False
    if "昨天" in t:
        delta = 1
        flag = True
    elif "前天" in t:
        delta = 2
        flag = True
    if flag:
        t = t.replace("昨天", "").replace("前天", "").split(":")
        _ = datetime.now() - timedelta(days=delta)
        s = datetime(_.year, _.month, _.day, int(t[0]), int(t[-1]))
        return s
    delta = int(re.findall("\d+", t)[0])
    if "秒" in t:
        s = datetime.now() - timedelta(seconds=delta)
    elif "分钟" in t:
        s = datetime.now() - timedelta(minutes=delta)

    elif "小时" in t:
        s = datetime.now() - timedelta(hours=delta)
    elif "天" in t:
        s = datetime.now() - timedelta(days=delta)
    # elif '年' in t:
    #     s = (datetime.now() - timedelta(days=365 * delta))
    elif "年" in t and "月" in t and "日" in t:
        s = datetime.strptime(t, "%Y年%m月%d日")
    elif "-" in t:
        s = datetime.strptime(t, "%Y-%m-%d")
    else:
        s = None
    return s


def get_attr(d: dict, t: str):
    """获取字典`d`下的`t`"""
    try:
        return d[t]
    except:
        return None
