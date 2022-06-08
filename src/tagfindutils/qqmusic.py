from __future__ import annotations

from copy import deepcopy as dp
from datetime import datetime

import requests

from .rawquery import get_details_from_qqmusic, get_search_results_from_qqmusic
from .structures import SearchResult, SongDetail
from .utils import type_filter


class QQMusicSongDetail(SongDetail):
    def __init__(self, raw_result: dict[str, str | int | list | dict | None]) -> None:
        raw_result = dp(raw_result)
        raw_result_data = self.type_filter(raw_result['data'], dict, allow_None=False)
        self._track_info: dict[str, str | int | list | dict] | None = raw_result_data.get('track_info')
        self._extra_info: dict[str, str] | None = raw_result_data.get('extras')
        self._misc_info: dict[str, dict[str, str | list]] | None = raw_result_data.get('info')

    @property
    def album(self) -> str | None:
        if self._track_info:
            alb: dict[str, str | int] | None = self.type_filter(self._track_info.get('album'), dict)
            if alb:
                return self.type_filter(alb.get('name'), str)

    @property
    def albumid(self) -> int | None:
        if self._track_info:
            alb: dict[str, str | int] | None = self.type_filter(self._track_info.get('album'), dict)
            if alb:
                return self.type_filter(alb.get('id'), int)

    @property
    def albummid(self) -> str | None:
        if self._track_info:
            alb: dict[str, str | int] | None = self.type_filter(self._track_info.get('album'), dict)
            if alb:
                return self.type_filter(alb.get('mid'), str)

    @property
    def aliases(self) -> list[str]:
        ret = []
        if self._track_info:
            subtitle: str | None = self.type_filter(self._track_info.get('subtitle'), str)
            if subtitle:
                ret.append(subtitle)

        return ret

    @property
    def translations(self) -> list[str]:
        ret = []
        if self._extra_info:
            transname: str | None = self.type_filter(self._extra_info.get('transname'), str)
            if transname:
                ret.append(transname)

        return ret

    @property
    def artists(self) -> list[str]:
        ret = []
        if self._track_info:
            singers: list[dict[str, str | int]] | None = self.type_filter(self._track_info.get('singer'), list)
            if singers:
                for item in singers:
                    item = self.type_filter(item, dict)
                    singername: str | None = self.type_filter(item.get('name'), str)
                    if singername:
                        ret.append(singername)

        return ret

    @property
    def artistids(self) -> list[int]:
        ret = []
        if self._track_info:
            singers: list[dict[str, str | int]] | None = self.type_filter(self._track_info.get('singer'), list)
            if singers:
                for item in singers:
                    item = self.type_filter(item, dict)
                    singerid: int | None = self.type_filter(item.get('id'), int)
                    if singerid:
                        ret.append(singerid)

        return ret

    @property
    def artistmids(self) -> list[str]:
        ret = []
        if self._track_info:
            singers: list[dict[str, str | int]] | None = self.type_filter(self._track_info.get('singer'), list)
            if singers:
                for item in singers:
                    item = self.type_filter(item, dict)
                    singermid: str | None = self.type_filter(item.get('mid'), str)
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
        if self._track_info:
            return self.type_filter(self._track_info.get('name'), str)

    @property
    def songid(self) -> int | None:
        if self._track_info:
            return self.type_filter(self._track_info.get('id'), int)

    @property
    def songmid(self) -> str | None:
        if self._track_info:
            return self.type_filter(self._track_info.get('mid'), str)

    @property
    def publish_time(self) -> datetime | None:
        if self._track_info:
            pub_time_str = self.type_filter(self._track_info.get('time_public'), str)
            if pub_time_str:
                return datetime.fromisoformat(pub_time_str)

    @property
    def genre(self) -> list[str]:
        ret = []
        if self._misc_info:
            genre_info: dict[str, str | list[dict]] | None = self.type_filter(self._misc_info.get('genre'), dict)
            if genre_info:
                genre_contents: list[dict[str, str | int]] | None = self.type_filter(genre_info.get('content'), list)
                if genre_contents:
                    for item in genre_contents:
                        item = self.type_filter(item, dict)
                        genre_value: str | None = self.type_filter(item.get('value'), str)
                        if genre_value:
                            ret.append(genre_value)

        return ret

    @property
    def company(self) -> list[str]:
        ret = []
        if self._misc_info:
            company_info: dict[str, str | list[dict]] | None = self.type_filter(self._misc_info.get('company'), dict)
            if company_info:
                company_contents: list[dict[str, str | int]] | None = self.type_filter(company_info.get('content'), list)
                if company_contents:
                    for item in company_contents:
                        item = self.type_filter(item, dict)
                        company_value: str | None = self.type_filter(item.get('value'), str)
                        if company_value and company_value != '制作家':
                            ret.append(company_value)

        return ret


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

    def get_detail(self) -> QQMusicSongDetail | None:
        if self.songmid:
            ret = details(self.songmid)
            if len(ret) != 0:
                return ret[0]


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


def details(*songmids: str) -> list[QQMusicSongDetail]:
    """根据一个或多个 songmid 从 QQ 音乐获取一首/多首歌曲的详细信息。

    Args:
        *songmids: 一个或多个歌曲 mID
    """
    _full_result = get_details_from_qqmusic(*songmids, raw_response=False)
    if isinstance(_full_result, requests.Response):
        full_result: dict = _full_result.json()
    else:
        full_result: dict = type_filter(_full_result, dict)
    ret = []
    if full_result:
        raw_results: list[dict] = full_result['songs']
        for item in raw_results:
            ret.append(QQMusicSongDetail(item['songinfo']))

    return ret
