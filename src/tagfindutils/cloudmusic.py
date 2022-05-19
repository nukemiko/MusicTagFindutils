from __future__ import annotations

from copy import deepcopy as dp
from datetime import datetime

import requests

from .rawquery import search_from_cloudmusic
from .structures import SearchResult


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

    def get_details(self):
        raise NotImplementedError


def search(*keywords: str,
           result_pageno: int = 0,
           result_size: int = 10,
           ) -> list[CloudMusicSearchResult]:
    _full_result = search_from_cloudmusic(*keywords, result_pageno=result_pageno, result_size=result_size)
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
