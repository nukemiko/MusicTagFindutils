from __future__ import annotations

from copy import deepcopy as dp
from datetime import datetime

import requests

from .rawquery import get_details_from_cloudmusic, get_search_results_from_cloudmusic
from .structures import SearchResult, SongDetail


class CloudMusicSongDetail(SongDetail):
    def __init__(self, raw_result: dict[str, str | int | list | dict | None]) -> None:
        self._raw_result = dp(raw_result)

    @property
    def album(self) -> str | None:
        alb: dict[str, str | int | list[str]] | None = self.type_filter(self._raw_result.get('al'), dict)
        if alb:
            albname = self.type_filter(alb.get('name'), str)
            return albname

    @property
    def albumid(self) -> int | None:
        alb: dict[str, str | int | list[str]] | None = self.type_filter(self._raw_result.get('al'), dict)
        if alb:
            albid = self.type_filter(alb.get('id'), int)
            return albid

    @property
    def aliases(self) -> list[str]:
        alia: list[str] | None = self.type_filter(self._raw_result.get('alia'), list)
        ret: list[str] = []
        if alia:
            for item in alia:
                if item:
                    ret.append(self.type_filter(item, str))

        return ret

    @property
    def translations(self) -> list[str]:
        tns: list[str] | None = self.type_filter(self._raw_result.get('tns'), list)
        ret: list[str] = []
        if tns:
            for item in tns:
                if item:
                    ret.append(self.type_filter(item, str))

        return ret

    @property
    def artists(self) -> list[str]:
        arts: list[dict[str, str | int | list[str]]] | None = self.type_filter(self._raw_result.get('ar'), list)
        ret: list[str] = []
        if arts:
            for item in arts:
                artist_name = self.type_filter(item.get('name'), str)
                if artist_name:
                    ret.append(artist_name)

        return ret

    @property
    def artistids(self) -> list[int]:
        arts: list[dict[str, str | int | list[str]]] | None = self.type_filter(self._raw_result.get('ar'), list)
        ret: list[int] = []
        if arts:
            for item in arts:
                artist_id = self.type_filter(item.get('id'), int)
                if artist_id:
                    ret.append(artist_id)

        return ret

    @property
    def coverurl(self) -> str | None:
        alb: dict[str, str | int | list[str]] | None = self.type_filter(self._raw_result.get('al'), dict)
        if alb:
            pic_url = self.type_filter(alb.get('picUrl'), str)
            return pic_url

    @property
    def songname(self) -> str | None:
        return self.type_filter(self._raw_result.get('name'), str)

    @property
    def songid(self) -> int | None:
        return self.type_filter(self._raw_result.get('id'), int)

    @property
    def publish_time(self) -> datetime | None:
        time_us = self.type_filter(self._raw_result.get('publishTime'), int)
        if time_us is not None:
            time_ms: float = time_us / 1000
            return datetime.fromtimestamp(time_ms)

    @property
    def genre(self) -> list[str]:
        return []

    @property
    def company(self) -> list[str]:
        return []


class CloudMusicSearchResult(SearchResult):
    def __init__(self, raw_result: dict[str, str | int | list | dict]) -> None:
        self._raw_result = dp(raw_result)

    @property
    def album(self) -> str | None:
        alb: dict[str, str | int | list[str]] | None = self.type_filter(self._raw_result.get('al'), dict)
        if alb:
            albname = self.type_filter(alb.get('name'), str)
            return albname

    @property
    def albumid(self) -> int | None:
        alb: dict[str, str | int | list[str]] | None = self.type_filter(self._raw_result.get('al'), dict)
        if alb:
            albid = self.type_filter(alb.get('id'), int)
            return albid

    @property
    def aliases(self) -> list[str]:
        alia: list[str] | None = self.type_filter(self._raw_result.get('alia'), list)
        ret: list[str] = []
        if alia:
            for item in alia:
                if item:
                    ret.append(self.type_filter(item, str))

        return ret

    @property
    def translations(self) -> list[str]:
        tns: list[str] | None = self.type_filter(self._raw_result.get('tns'), list)
        ret: list[str] = []
        if tns:
            for item in tns:
                if item:
                    ret.append(self.type_filter(item, str))

        return ret

    @property
    def artists(self) -> list[str]:
        arts: list[dict[str, str | int | list[str]]] | None = self.type_filter(self._raw_result.get('ar'), list)
        ret: list[str] = []
        if arts:
            for item in arts:
                artist_name = self.type_filter(item.get('name'), str)
                if artist_name:
                    ret.append(artist_name)

        return ret

    @property
    def artistids(self) -> list[int]:
        arts: list[dict[str, str | int | list[str]]] | None = self.type_filter(self._raw_result.get('ar'), list)
        ret: list[int] = []
        if arts:
            for item in arts:
                artist_id = self.type_filter(item.get('id'), int)
                if artist_id:
                    ret.append(artist_id)

        return ret

    @property
    def coverurl(self) -> str | None:
        alb: dict[str, str | int | list[str]] | None = self.type_filter(self._raw_result.get('al'), dict)
        if alb:
            pic_url = self.type_filter(alb.get('picUrl'), str)
            return pic_url

    @property
    def songname(self) -> str | None:
        return self.type_filter(self._raw_result.get('name'), str)

    @property
    def songid(self) -> int | None:
        return self.type_filter(self._raw_result.get('id'), int)

    @property
    def publish_time(self) -> datetime | None:
        time_us = self.type_filter(self._raw_result.get('publishTime'), int)
        if time_us is not None:
            time_ms: float = time_us / 1000
            return datetime.fromtimestamp(time_ms)

    def get_detail(self) -> CloudMusicSongDetail | None:
        if self.songid is not None:
            ret = details(self.songid)
            if len(ret) != 0:
                return ret[0]


def search(*keywords: str,
           result_pageidx: int = 0,
           result_size: int = 10,
           ) -> list[CloudMusicSearchResult]:
    """根据关键词，从 QQ 音乐获取匹配关键词的歌曲的信息。

    Args:
        keywords (str): 关键词
        result_pageidx (int): 搜索结果的所在的页码，默认为 0
        result_size (int): 搜索结果的数量，默认为 10
    Raises:
        requests.RequestException: 网络、远端相关错误
    """
    _full_result = get_search_results_from_cloudmusic(*keywords, result_pageidx=result_pageidx, result_size=result_size)
    if isinstance(_full_result, requests.Response):
        full_result: dict = _full_result.json()
    else:
        full_result: dict = _full_result
    ret = []
    if full_result:
        raw_results: list[dict] = full_result['result']['songs']
        for item in raw_results:
            ret.append(CloudMusicSearchResult(item))

    return ret


def details(*songids: int | str) -> list[CloudMusicSongDetail]:
    """根据一个或多个 songid 从网易云音乐获取一首/多首歌曲的详细信息。

    Args:
        *songids: 一个或多个歌曲 ID
    """
    _full_result = get_details_from_cloudmusic(*songids, raw_response=False)
    if isinstance(_full_result, requests.Response):
        full_result: dict = _full_result.json()
    else:
        full_result: dict = _full_result
    ret = []
    if full_result:
        raw_results: list[dict] = full_result['songs']
        for item in raw_results:
            ret.append(CloudMusicSongDetail(item))

    return ret
