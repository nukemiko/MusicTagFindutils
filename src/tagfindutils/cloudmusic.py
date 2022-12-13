# -*- coding: utf-8 -*-
from __future__ import annotations

import json

import requests


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
