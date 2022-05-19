from __future__ import annotations

from copy import deepcopy as dp
from datetime import datetime

import requests

from .rawquery import get_search_results_from_qqmusic
from .structures import SearchResult


class QQMusicSearchResult(SearchResult):
    def __init__(self, raw_result: dict[str, str | int | list | dict]) -> None:
        self._raw_result = dp(raw_result)

    @property
    def album(self) -> str | None:
        return self.type_filter(self._raw_result.get('albumname'), str)

    @property
    def albumid(self) -> int | None:
        return self.type_filter(self._raw_result.get('albumid'), int)

    @property
    def albummid(self) -> str | None:
        return self.type_filter(self._raw_result.get('albummid'), str)

    @property
    def aliases(self) -> list[str]:
        lyric_title = self.type_filter(self._raw_result.get('lyric'), str)
        ret: list[str] = []
        if lyric_title:
            ret.extend(lyric_title.split('|'))

        return ret

    @property
    def translations(self) -> list[str]:
        return []

    @property
    def artists(self) -> list[str]:
        singers: list[dict[str, str | int]] | None = self.type_filter(self._raw_result.get('singer'), list)
        ret: list[str] = []
        if singers:
            for item in singers:
                singername = self.type_filter(item.get('name'), str)
                if singername:
                    ret.append(singername)

        return ret

    @property
    def artistids(self) -> list[int]:
        singers: list[dict[str, str | int]] | None = self.type_filter(self._raw_result.get('singer'), list)
        ret: list[int] = []
        if singers:
            for item in singers:
                singerid = self.type_filter(item.get('id'), int)
                if singerid:
                    ret.append(singerid)

        return ret

    @property
    def artistmids(self) -> list[str]:
        singers: list[dict[str, str | int]] | None = self.type_filter(self._raw_result.get('singer'), list)
        ret: list[str] = []
        if singers:
            for item in singers:
                singermid = self.type_filter(item.get('mid'), str)
                if singermid:
                    ret.append(singermid)

        return ret

    @property
    def coverurl(self) -> str | None:
        albummid = self.type_filter(self.albummid, str)
        if albummid:
            return f'https://y.qq.com/music/photo_new/T002R800x800M000{albummid}.jpg'

    @property
    def songname(self) -> str | None:
        return self.type_filter(self._raw_result.get('songname'), str)

    @property
    def songid(self) -> int | None:
        return self.type_filter(self._raw_result.get('songid'), int)

    @property
    def songmid(self) -> str | None:
        return self.type_filter(self._raw_result.get('songmid'), str)

    @property
    def publish_time(self) -> datetime | None:
        time_ms = self.type_filter(self._raw_result.get('pubtime'), int)
        if time_ms:
            return datetime.fromtimestamp(time_ms)


def search(*keywords: str,
           result_pageidx: int = 0,
           result_size: int = 10,
           ) -> list[QQMusicSearchResult]:
    """根据关键词，从 QQ 音乐获取匹配关键词的歌曲的信息。

    Args:
        keywords (str): 关键词
        result_pageidx (int): 搜索结果的所在的页码，默认为 0
        result_size (int): 搜索结果的数量，默认为 10
    Raises:
        requests.RequestException: 网络、远端相关错误
    """
    _full_result = get_search_results_from_qqmusic(*keywords, result_pageidx=result_pageidx, result_size=result_size)
    if isinstance(_full_result, requests.Response):
        full_result: dict = _full_result.json()
    else:
        full_result: dict = _full_result
    ret = []
    if full_result:
        raw_results: list[dict] = full_result['data']['song']['list']
        for item in raw_results:
            ret.append(QQMusicSearchResult(item))

    return ret
