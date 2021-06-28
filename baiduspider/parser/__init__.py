import json
from datetime import datetime, time
from html import unescape

from baiduspider._spider import BaseSpider
from baiduspider.errors import ParseError
from baiduspider.parser.subparser import WebSubParser
from baiduspider.util import handle_err
from bs4 import BeautifulSoup


class Parser(BaseSpider):
    def __init__(self) -> None:
        super().__init__()
        self.webSubParser = WebSubParser()

    def parse_web(self, content: str, exclude: list) -> dict:
        """解析百度网页搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度网页搜索HTML源码.
            exclude (list): 要屏蔽的控件.

        Returns:
            dict: 解析后的结果
        """
        soup = BeautifulSoup(content, "html.parser")
        if soup.find("div", id="content_left") is None:
            return {"results": [], "pages": 0}
        # 获取搜索结果总数
        num = int(
            str(soup.find("span", class_="nums_text").text)
            .strip("百度为您找到相关结果约")
            .strip("个")
            .replace(",", "")
        )
        # 定义预结果（运算以及相关搜索）
        pre_results = []
        # 预处理新闻
        if "news" not in exclude:
            news = soup.find(
                "div", class_="result-op", tpl="sp_realtime_bigpic5", srcid="19"
            )
            news_detail = self.webSubParser.parse_news_block(news)
        # 预处理短视频
        if "video" not in exclude:
            video = soup.find("div", class_="op-short-video-pc")
            video_results = self.webSubParser.parse_video_block(video)
        # 预处理运算
        if "calc" not in exclude:
            calc = soup.find("div", class_="op_new_cal_screen")
        # 预处理相关搜索
        if "related" not in exclude:
            try:
                _related = soup.find("div", id="rs").find("table").find_all("th")
            except AttributeError:
                _related = []
            related = []
            # 一个一个append相关搜索
            for _ in _related:
                if _.text:
                    related.append(_.text)
        # 预处理百科
        if "baike" not in exclude:
            baike = soup.find("div", class_="c-container", tpl="bk_polysemy")
            baike = self.webSubParser.parse_baike_block(baike)
        # 预处理贴吧
        if "tieba" not in exclude:
            tieba = BeautifulSoup(content, "html.parser").find("div", srcid="10")
            tieba = self.webSubParser.parse_tieba_block(tieba)
        if "music" not in exclude:
            music = BeautifulSoup(content, "html.parser").find(
                "div", class_="result-op", tpl="yl_music_song"
            )
            music = self.webSubParser.parse_music_block(music)
        # 预处理博客
        article_tags = BeautifulSoup(content, "html.parser").findAll("article")
        if "blog" not in exclude:
            blog = None
            for tmp in article_tags:
                if tmp["class"][-1].startswith("open-source-software-blog"):
                    blog = tmp
                    break
            blog = self.webSubParser.parse_blog_block(blog)
        # 预处理码云
        if "gitee" not in exclude:
            gitee = None
            for tmp in article_tags:
                if tmp["class"][-1].startswith("osc-gitee"):
                    gitee = tmp
                    break
            gitee = self.webSubParser.parse_gitee_block(gitee)
        # 加载贴吧
        if "tieba" not in exclude and tieba:
            pre_results.append(dict(type="tieba", result=tieba))
        # 加载博客
        if "blog" not in exclude and blog:
            pre_results.append(dict(type="blog", result=blog))
        # 加载码云
        if "gitee" not in exclude and gitee:
            pre_results.append(dict(type="gitee", result=gitee))
        # 加载搜索结果总数
        if num != 0:
            pre_results.append(dict(type="total", result=num))
        # 加载运算
        if "calc" not in exclude and calc:
            pre_results.append(
                dict(
                    type="calc",
                    process=str(
                        calc.find("p", class_="op_new_val_screen_process")
                        .find("span")
                        .text
                    ),
                    result=str(
                        calc.find("p", class_="op_new_val_screen_result")
                        .find("span")
                        .text
                    ),
                )
            )
        # 加载相关搜索
        if "related" not in exclude and related:
            pre_results.append(dict(type="related", results=related))
        # 加载资讯
        if "news" not in exclude and news_detail:
            pre_results.append(dict(type="news", results=news_detail))
        # 加载短视频
        if "video" not in exclude and video_results:
            pre_results.append(dict(type="video", results=video_results))
        # 加载百科
        if "baike" not in exclude and baike:
            pre_results.append(dict(type="baike", result=baike))
        # 加载音乐
        if "music" not in exclude and music:
            pre_results.append(dict(type="music", result=music))
        # 预处理源码
        soup = BeautifulSoup(content, "html.parser")
        results = soup.findAll("div", class_="result")
        res = []
        for result in results:
            des = None
            try:
                result["tpl"]
            except:
                continue
            soup = BeautifulSoup(self._minify(str(result)), "html.parser")
            # 链接
            href = soup.find("a").get("href").strip()
            # 标题
            title = self._format(str(soup.find("a").text))
            # 时间
            try:
                time = self._format(
                    soup.findAll("div", class_="c-abstract")[0]
                    .find("span", class_="newTimeFactor_before_abs")
                    .text
                )
            except (AttributeError, IndexError):
                time = None
            try:
                # 简介
                des = soup.find_all("div", class_="c-abstract")[0].text
                soup = BeautifulSoup(str(result), "html.parser")
                des = self._format(des).lstrip(str(time)).strip()
            except IndexError:
                try:
                    des = des.replace("mn", "")
                except (UnboundLocalError, AttributeError):
                    des = None
            if time:
                time = time.split("-")[0].strip()
            # 因为百度的链接是加密的了，所以需要一个一个去访问
            # 由于性能原因，分析链接部分暂略
            # if href is not None:
            #     try:
            #         # 由于性能原因，这里设置1秒超时
            #         r = requests.get(href, timeout=1)
            #         href = r.url
            #     except:
            #         # 获取网页失败，默认换回原加密链接
            #         href = href
            #     # 分析链接
            #     if href:
            #         parse = urlparse(href)
            #         domain = parse.netloc
            #         prepath = parse.path.split('/')
            #         path = []
            #         for loc in prepath:
            #             if loc != '':
            #                 path.append(loc)
            #     else:
            #         domain = None
            #         path = None
            try:
                result["tpl"]
            except:
                pass
            is_not_special = (
                result["tpl"]
                not in [
                    "short_video_pc",
                    "sp_realtime_bigpic5",
                    "bk_polysemy",
                    "tieba_general",
                    "yl_music_song",
                ]
                and result.find("article") is None
            )
            domain = None
            if is_not_special:  # 确保不是特殊类型的结果
                # 获取可见的域名
                try:
                    domain = (
                        result.find("div", class_="c-row")
                        .find("div", class_="c-span-last")
                        .find("div", class_="se_st_footer")
                        .find("a", class_="c-showurl")
                        .text
                    )
                except Exception:
                    try:
                        domain = (
                            result.find("div", class_="c-row")
                            .find("div", class_="c-span-last")
                            .find("p", class_="op-bk-polysemy-move")
                            .find("span", class_="c-showurl")
                            .text
                        )
                    except Exception:
                        try:
                            domain = (
                                result.find("div", class_="se_st_footer")
                                .find("a", class_="c-showurl")
                                .text
                            )
                        except:
                            domain = None
                if domain:
                    domain = domain.replace(" ", "")
            # 加入结果
            if title and href and is_not_special:
                res.append(
                    {
                        "title": title,
                        "des": des,
                        "origin": domain,
                        "url": href,
                        "time": time,
                        "type": "result",
                    }
                )
        soup = BeautifulSoup(content, "html.parser")
        soup = BeautifulSoup(str(soup.findAll("div", id="page")[0]), "html.parser")
        # 分页
        pages_ = soup.findAll("span", class_="pc")
        pages = []
        for _ in pages_:
            pages.append(int(_.text))
        # 如果搜索结果仅有一页时，百度不会显示底部导航栏
        # 所以这里直接设置成1，如果不设会报错`TypeError`
        if not pages:
            pages = [1]
        # 设置最终结果
        result = pre_results
        result.extend(res)
        return {
            "results": result,
            # 最大页数
            "pages": max(pages),
        }

    @handle_err
    def parse_pic(self, content: str) -> dict:
        """解析百度图片搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度图片搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        # 从JavaScript中加载数据
        # 因为JavaScript很像JSON（JavaScript Object Notation），所以直接用json加载就行了
        # 还有要预处理一下，把函数和无用的括号过滤掉
        error = None
        try:
            data = json.loads(
                content.split("flip.setData('imgData', ")[1]
                .split("flip.setData(")[0]
                .split("]);")[0]
                .replace(");", "")
                .replace("<\\/strong>", "</strong>")
                .replace("\\'", "'")
                .replace('\\"', "'"),
                strict=False,
            )
        except Exception as err:
            error = err
            if type(err) in [IndexError, AttributeError]:
                raise ParseError("Invalid HTML content.")
        finally:
            if error:
                raise ParseError(str(error))
        results = []
        for _ in data["data"][:-1]:
            if _:
                # 标题
                title = str(_["fromPageTitle"]).encode("utf-8").decode("utf-8")
                # 去除标题里的HTML
                title = unescape(self._remove_html(title))
                # 链接
                url = _["objURL"]
                # 来源域名
                host = _["fromURLHost"]
                # 生成结果
                result = {"title": title, "url": url, "host": host}
                results.append(result)  # 加入结果
        # 获取分页
        bs = BeautifulSoup(content, "html.parser")
        pages_ = bs.find("div", id="page").findAll("span", class_="pc")
        pages = []
        for _ in pages_:
            pages.append(int(_.text))
        return {
            "results": results,
            # 取最大页码
            "pages": max(pages),
        }

    def parse_zhidao(self, content: str) -> dict:
        """解析百度知道搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度知道搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(self._minify(content), "html.parser")
        # 所有搜索结果
        list_ = bs.find("div", class_="list").findAll("dl")
        results = []
        for item in list_:
            # 屏蔽企业回答
            if "ec-oad" in item["class"]:
                continue
            # print(item.prettify() + '\n\n\n\n\n\n\n')
            # 标题
            title = item.find("dt").text.strip("\n")
            # 链接
            try:
                url = item.find("dt").find("a")["href"]
            except KeyError:
                url = item.find("dt").find("a")["data-href"]
            if item.find("dd", class_="video-content") is not None:
                # 问题
                __ = item.find("dd", class_="summary")
                question = __.text.strip("问：") if __ is not None else None
                item = item.find("div", class_="right")
                tmp = item.findAll("div", class_="video-text")
                # # 简介
                # des = self._format(tmp[2].text)
                answer = None
                # 回答者
                answerer = tmp[0].text.strip("\n").strip("回答:\u2002")
                # 发布日期
                date = self._format(tmp[1].text.strip("时间:"))
                # 回答总数
                count = None
                # 赞同数
                try:
                    agree = int(tmp[2].text.strip("获赞:\u2002").strip("次"))
                except ValueError:
                    agree = 0
                    answer = tmp[2].text.strip()
                type_ = "video"
            else:
                # 回答
                __ = item.find("dd", class_="answer")
                answer = __.text.strip("答：") if __ is not None else None
                # 问题
                __ = item.find("dd", class_="summary")
                question = __.text.strip("问：") if __ is not None else None
                tmp = item.find("dd", class_="explain").findAll("span", class_="mr-8")
                # 发布日期
                date = (
                    item.find("dd", class_="explain").find("span", class_="mr-7").text
                )
                # 回答总数
                try:
                    count = int(str(tmp[-1].text).strip("\n").strip("个回答"))
                except:
                    count = None
                # 回答者
                answerer = tmp[-2].text.strip("\n").strip("回答者:\xa0")
                # 赞同数
                __ = item.find("dd", class_="explain").find("span", class_="ml-10")
                agree = int(__.text.strip()) if __ is not None else 0
                type_ = "normal"
            # 生成结果
            result = {
                "title": title,
                "question": question,
                "answer": answer,
                "date": date,
                "count": count,
                "url": url,
                "agree": agree,
                "answerer": answerer,
                # "type": type_
            }
            results.append(result)  # 加入结果
        # 获取分页
        wrap = bs.find("div", class_="pager")
        pages_ = wrap.findAll("a")[:-2]
        if "下一页" in pages_[-1].text:
            total = pages_[-2].text
        else:
            total = pages_[-1].text
        return {
            "results": results,
            # 取最大页码
            "pages": int(total),
        }

    def parse_video(self, content: str) -> dict:
        """解析百度视频搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度视频搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(content, "html.parser")
        # 锁定结果div
        data = bs.findAll("div", class_="video_short")
        if len(data) == 0:
            return {"results": None}
        results = []
        for res in data:
            __ = res.find("div", class_="video_small_intro")
            _ = __.find("a")
            # 标题
            title = self._format(_.text)
            # 链接
            url = _["href"]
            # 封面图片链接
            img = res.find("img", class_="border-radius")["src"].rsplit("?", 1)[0]
            # 时长
            length_ = res.find("span", class_="video_play_timer").text
            _ = [int(i) for i in length_.split(":")]
            if len(_) < 3:
                length_ = time(minute=_[0], second=_[1])
            else:
                length_ = time(_[0], _[1], _[2])
            # 简介
            try:
                des = __.find("div", class_="c-color-text").text
            except AttributeError:
                des = None
            # 来源
            try:
                origin = self._format(__.find("span", class_="wetSource").text).strip(
                    "来源："
                )
            except AttributeError:
                origin = None
            # 发布时间
            pub_time: str = __.findAll("span", class_="c-font-normal")[-1].text.strip(
                "发布时间："
            )
            try:
                __ = [int(i) for i in pub_time.split("-")]
            except ValueError:
                __ = self._convert_time(pub_time, True)
            pub_time = datetime(__[0], __[1], __[2])
            # 生成结果
            result = {
                "title": title,
                "url": url,
                "img": img,
                "length": length_,
                "des": des,
                "origin": origin,
                "pub_time": pub_time,
            }
            results.append(result)  # 加入结果
        return {"results": results}

    def parse_news(self, content: str) -> dict:
        """解析百度资讯搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度资讯搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(self._format(content), "html.parser")
        # 搜索结果容器
        data = (
            bs.find("div", id="content_left")
            .findAll("div")[1]
            .findAll("div", class_="result-op")
        )
        results = []
        for res in data:
            # 标题
            title = self._format(res.find("h3").find("a").text)
            # 链接
            url = res.find("h3").find("a")["href"]
            # 简介
            des = (
                res.find("div", class_="c-span-last")
                .find("span", class_="c-color-text")
                .text
            )
            _ = res.find("div", class_="c-span-last")
            # 作者
            author = _.find("span", class_="c-gap-right").text
            # 发布日期
            try:
                date = _.find("span", class_="c-color-gray2").text
            except AttributeError:
                date = None
            # 封面图片
            try:
                cover = res.find("div", class_="c-img-radius-large").find("img")["src"]
            except:
                cover = None
            # 生成结果
            result = {
                "title": title,
                "author": author,
                "date": date,
                "des": des,
                "url": url,
                "cover": cover,
            }
            results.append(result)  # 加入结果
        # 获取所有页数
        pages_ = bs.find("div", id="page").findAll("a")
        # 过滤页码
        if "< 上一页" in pages_[0].text:
            pages_ = pages_[1:]
        if "下一页 >" in pages_[-1].text:
            pages_ = pages_[:-1]
        return {"results": results, "pages": int(pages_[-1].text)}

    def parse_wenku(self, content: str) -> dict:  # pragma: no cover
        """解析百度文库搜索的页面源代码，目前不可用。

        Args:
            content (str): 已经转换为UTF-8编码的百度文库搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        bs = BeautifulSoup(content, "html.parser")
        data = bs.findAll("dl")
        results = []
        for res in data:
            dt = res.find("dt")
            type_ = self._format(
                dt.find("p", class_="fl").find("span", class_="ic")["title"]
            ).upper()
            _ = dt.find("p", class_="fl").findAll("a")
            try:
                if _[-1].find("span", class_="ico-vip").text.strip() == "VIP":
                    is_vip = True
                else:
                    is_vip = False
            except:
                is_vip = False
            tmp = _[0]
            title = self._format(tmp.text)
            url = tmp["href"]
            try:
                quality = float(
                    self._format(
                        res.find("p", class_="fr").findAll("span", class_="ib")[1].text
                    )
                )
            except:
                quality = None
            dd = res.find("dd", class_="clearfix").find("div", class_="summary-box")
            des = self._format(dd.find("p", class_="summary").text)
            try:
                dd_tags = res.find("dd", class_="tag-tips")
                tags = []
                for a in dd_tags.findAll("a"):
                    tags.append(self._format(a.text))
            except AttributeError:
                tags = []
            detail = dd.find("div", class_="detail").find("div", class_="detail-info")
            date = self._format(detail.text.split("|")[0])
            pages = int(
                self._format(
                    detail.text.split("|")[1].replace("共", "").replace("页", "")
                )
            )
            downloads = int(self._format(detail.text.split("|")[2].strip("次下载")))
            uploader = {
                "name": detail.find("a").text.strip("\n"),
                "url": "https://wenku.baidu.com" + detail.find("a")["href"],
            }
            result = {
                "title": title,
                "type": type_,
                "url": url,
                "des": des,
                "pub_date": date,
                "pages": pages,
                "downloads": downloads,
                "quality": quality,
                "uploader": uploader,
                "is_vip": is_vip,
            }
            results.append(result)
        try:
            pages_ = bs.find("div", class_="page-content").findAll("a")
            if "尾页" in pages_[-1].text:
                total = int(
                    int(pages_[-1]["href"].split("&")[-1].strip("pn=")) / 10 + 1
                )
            else:
                total = int(
                    bs.find("div", class_="page-content")
                    .find("span", class_="cur")
                    .text
                )
        except:
            total = 1
        return {"results": results, "pages": total}

    def parse_jingyan(self, content: str) -> dict:
        """解析百度经验搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度经验搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        # 最小化代码
        code = self._minify(content)
        bs = BeautifulSoup(code, "html.parser")
        # 加载搜索结果
        data = bs.find("div", class_="search-list").findAll("dl")
        results = []
        for res in data:
            # 标题
            title = self._format(res.find("dt").find("a").text)
            # 链接
            url = "https://jingyan.baidu.com/" + res.find("dt").find("a")["href"]
            # 简介
            des = self._format(
                res.find("dd")
                .find("div", class_="summary")
                .find("span", class_="abstract")
                .text
            )
            # 获取发布日期和分类，位于`<span class="cate"/>`中
            _ = res.find("dd").find("div", class_="summary").find("span", class_="cate")
            tmp = self._format(_.text).split("-")
            # 发布日期
            pub_date = self._format(tmp[1]).replace("/", "-")
            # 分类
            category = self._format(tmp[-1]).strip("分类：").split(">")
            # 发布者
            publisher = {
                "name": self._format(_.find("a").text),
                "url": "https://jingyan.baidu.com" + _.find("a")["href"],
            }
            # 支持票数
            votes = int(
                self._format(
                    res.find("dt").find("span", class_="succ-times").text
                ).strip("得票")
            )
            # 是否为原创经验
            try:
                res.find("span", class_="i-original").text
                original = True
            except:
                original = False
            # 是否为优秀经验
            try:
                res.find("span", class_="i-good-exp").text
                outstanding = True
            except:
                outstanding = False
            # 生成结果
            result = {
                "title": title,
                "url": url,
                "des": des,
                "pub_date": pub_date,
                "category": category,
                "votes": votes,
                "publisher": publisher,
                "is_original": original,
                "is_outstanding": outstanding,
            }
            results.append(result)  # 加入结果到集合中
        # 获取分页
        pages_ = bs.find("div", class_="pager-wrap").findAll("a", class_="pg-btn")
        if not pages_:
            return {"results": results, "pages": 1}
        if "下一页" in pages_[-1].text:
            pages_ = pages_[:-1]
        total = int(self._format(pages_[-1].text))
        return {"results": results, "pages": total}

    def parse_baike(self, content: str) -> dict:
        """解析百度百科搜索的页面源代码.

        Args:
            content (str): 已经转换为UTF-8编码的百度百科搜索HTML源码

        Returns:
            dict: 解析后的结果
        """
        code = self._minify(content)
        # 创建BeautifulSoup对象
        soup = (
            BeautifulSoup(code, "html.parser")
            .find("div", class_="body-wrapper")
            .find("div", class_="searchResult")
        )
        # 获取百科总数
        total = int(
            soup.find("div", class_="result-count")
            .text.strip("百度百科为您找到相关词条约")
            .strip("个")
        )
        # 获取所有结果
        container = soup.findAll("dd")
        results = []
        for res in container:
            # 链接
            url = "https://baike.baidu.com" + self._format(
                res.find("a", class_="result-title")["href"]
            )
            # 标题
            title = self._format(res.find("a", class_="result-title").text)
            # 简介
            des = self._format(res.find("p", class_="result-summary").text)
            # 更新日期
            upd_date = self._format(res.find("span", class_="result-date").text)
            # 生成结果
            results.append(
                {"title": title, "des": des, "upd_date": upd_date, "url": url}
            )
        return {"results": results, "total": total}
