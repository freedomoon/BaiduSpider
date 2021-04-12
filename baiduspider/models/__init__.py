from datetime import datetime, timedelta
import re

def convert_time(t) -> datetime:
    if t is None:
        return None
    delta = int(re.findall('\d+', t)[0])
    if '秒' in t:
        s = (datetime.now() - timedelta(seconds=delta))
    elif '分钟' in t:
        s = (datetime.now() - timedelta(minutes=delta))

    elif '小时' in t:
        s = (datetime.now() - timedelta(hours=delta))
    elif '天' in t:
        s = (datetime.now() - timedelta(days=delta))
    # elif '年' in t:
    #     s = (datetime.now() - timedelta(days=365 * delta))
    elif '年' in t and '月' in t and '日' in t:
        s = datetime.strptime(t, '%Y年%m月%d日')
    else:
        s = datetime.now()
    return s

def get_attr(d: dict, t: str):
    try:
        return d[t]
    except:
        return None
