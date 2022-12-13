# -*- coding: utf-8 -*-
from __future__ import annotations

import io
import json
from datetime import datetime

import requests

from .prototypes import MusicInfo


def rawquery_get_matched_items(*keywords: str,
                               result_pageidx: int = 0,
                               result_pagesize: int = 10
                               ) -> dict:
    """从网易云音乐搜索与关键字 ``*keywords`` 匹配/相关的信息。

    Args:
        keywords (str): 关键字，可接受多个
        result_pageidx (int): 搜索结果所在的页码，默认为 0
        result_pagesize (int): 搜索结果的数量，默认为 10
    Raises:
        requests.RequestException: 网络请求相关异常
        ConnectionError: 网络请求正常，但远端服务返回表示报错的状态码
    """
    if not keywords:
        raise ValueError("no keywords were provided")
    final_keyword = ' '.join(keywords)

    url = 'https://music.163.com/api/cloudsearch/pc'
    payload = {
        's'     : final_keyword,
        'type'  : 1,
        'limit' : int(result_pagesize),
        'offset': int(result_pageidx),
        'total' : True
    }

    resp = requests.post(url=url, data=payload)
    resp.raise_for_status()
    try:
        result = resp.json()
    except json.JSONDecodeError:
        raise ConnectionError('JSON Decode failed! Original response text: \n'
                              f'{resp.text}'
                              )
    if result['code'] >= 400:
        raise ConnectionError(
            f"query failed: remote service returns an exceptional status code "
            f"{result['code']}"
        )

    return result


def rawquery_get_item_detail(music_id: int) -> dict:
    """根据 ``music_id``，查找网易云音乐上对应歌曲的信息。"""
    url = 'https://music.163.com/api/v3/song/detail'

    payload = {
        'c': json.dumps(
            [{'id': int(music_id)}]
        )
    }

    resp = requests.post(url, data=payload)
    resp.raise_for_status()
    try:
        results: list[dict] = resp.json()['songs']
    except json.JSONDecodeError:
        raise ConnectionError('JSON Decode failed! Original response text: \n'
                              f'{resp.text}'
                              )
    except KeyError:
        raise ConnectionError('remote service returns invalid query result! '
                              'Original response text: \n'
                              f'{resp.text}'
                              )
    for item in results:
        if item.get('id') == music_id:
            return item
    else:
        raise ConnectionError(f'no item corresponnding to music_id {music_id}')


class MusicInfoFromCloudMusic(MusicInfo):
    @classmethod
    def from_raw_result_item(cls, item: dict):
        musicName: str = str(item['name'])
        musicId: int = int(item['id'])
        musicAliases: list[str] = list(str(_) for _ in item['alia'])
        artists: list[dict] = list(dict(_) for _ in item['ar'])
        artistsNames: list[str] = list(str(_['name']) for _ in artists)
        artistsIds: dict[str, int] = {
            str(_['name']): int(_['id']) for _ in artists}
        artistsAliases: dict[str, list[str]] = {
            str(_['name']): [str(__) for __ in _['alias']] for _ in artists if _['alias']
        }
        artistsTranslations: dict[str, list[str]] = {
            str(_['name']): [str(__) for __ in _['tns']] for _ in artists if _['tns']
        }
        album: dict = dict(item['al'])
        albumName: str = str(album['name'])
        albumId: int = int(album['id'])
        albumTranslations: list[str] = list(str(_) for _ in album['tns'])
        albumCoverUrl: str = str(album['picUrl'])
        publishDate_tmstamp_ns = int(item['publishTime'])
        publishDate = datetime.fromtimestamp(publishDate_tmstamp_ns / 1000)

        instance = cls(
            musicName=musicName,
            musicId=musicId,
            musicAliases=musicAliases,
            artistsNames=artistsNames,
            artistsIds=artistsIds,
            artistsAliases=artistsAliases,
            artistsTranslations=artistsTranslations,
            albumName=albumName,
            albumId=albumId,
            albumTranslations=albumTranslations,
            albumCoverUrl=albumCoverUrl,
            publishDate=publishDate
        )

        return instance

    def fetch_cover_data(self) -> None:
        """下载歌曲的专辑封面图像数据（如果有），存储到 ``albumCoverData`` 字段中。

        如果 ``albumCoverData`` 字段已有数据，本方法什么都不做。
        """
        if not self.albumCoverData:
            if not self.albumCoverUrl:
                raise ValueError('self.albumCoverUrl is not available')
            resp = requests.get(self.albumCoverUrl, stream=True)
            resp.raise_for_status()
            self.albumCoverData = bytes(resp.iter_content(chunk_size=io.DEFAULT_BUFFER_SIZE))


def search(*keywords: str,
           result_len: int = 10,
           result_startidx: int = 0,
           direct: bool = False
           ) -> list[MusicInfoFromCloudMusic] | MusicInfoFromCloudMusic | None:
    """根据关键词 ``keywords`` 在网易云音乐上搜索所有相关的歌曲信息，并以包含
    ``MusicInfoFromCloudMusic`` 对象的列表形式返回。如果未能找到任何信息，则返回一个空列表。

    如果选项 ``direct=True``：

    - 当存在搜索结果列表时，直接返回列表的第一个结果（通常也是相关度最高的那个）；
    - 否则，返回 ``None``。

    Args:
        keywords: 关键词，可接受多个
        result_len: 返回搜索结果列表的最大长度；实际长度取决于找到的结果数量
        result_startidx: 搜索结果列表的开始位置
        direct: 是否直接返回列表的第一个结果；没有结果则返回 None
    """
    if not keywords:
        raise ValueError('no keyword were provided to search')

    result: dict[str, dict | int | str] = rawquery_get_matched_items(*keywords,
                                                                     result_pagesize=result_len,
                                                                     result_pageidx=result_startidx
                                                                     )
    ret = list(MusicInfoFromCloudMusic.from_raw_result_item(_) for _ in result['result'].get('songs', []))
    if direct:
        if len(ret) > 0:
            return ret[0]
        return
    return ret
