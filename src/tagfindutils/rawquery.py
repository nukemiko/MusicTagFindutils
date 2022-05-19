from __future__ import annotations

import json

import requests


def get_search_results_from_qqmusic(*keywords: str,
                                    result_pageidx: int = 0,
                                    result_size: int = 10,
                                    result_type: int = 0,
                                    raw_response=False
                                    ) -> dict | requests.Response:
    """从 QQ 音乐获取 歌曲/歌单/歌词/专辑/歌手/MV 的信息。

    Args:
        keywords (str): 关键词
        result_pageidx (int): 搜索结果的所在的页码，默认为 0
        result_size (int): 搜索结果的数量，默认为 10
        result_type (int): 搜索的类型
        raw_response (bool): 返回原始响应对象；
            默认为否（返回一个对结果进行 JSON 反序列化后得到的 dict）
    Raises:
        ValueError: 为参数 ``result_type`` 指定了不支持的值
        requests.RequestException: 网络、远端相关错误

    参数 ``result_type`` 为搜索的类型，支持以下值：
        - 0：歌曲
        - 2：歌单
        - 7：歌词
        - 8：专辑
        - 9：歌手
        - 12：MV
    """
    if result_type not in (0, 2, 7, 8, 9, 12):
        raise ValueError(f'不支持的搜索类型：{repr(result_type)}')

    final_keyword: str = ' '.join(keywords)

    if result_type == 2:
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_music_search_songlist'
        params = {
            'remoteplace': 'txt.yqq.playlist',
            'page_no': result_pageidx,
            'num_per_page': result_size,
            'query': final_keyword
        }
    else:
        url = 'http://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        params = {
            'format': 'json',
            'n': result_size,
            'p': result_pageidx + 1,
            'w': final_keyword,
            'cr': 1,
            'g_tk': 5381,
            't': result_type
        }
    headers = {
        'Referer': 'https://y.qq.com'
    }

    resp = requests.get(url=url, headers=headers, params=params)
    resp.raise_for_status()
    if raw_response:
        return resp
    return resp.json()


def get_search_results_from_cloudmusic(*keywords: str,
                                       result_pageidx: int = 0,
                                       result_size: int = 10,
                                       result_type: int = 1,
                                       raw_response=False
                                       ) -> dict | requests.Response:
    """从网易云音乐获取 歌曲/专辑/歌手/歌单/用户/MV/歌词/电台 的信息。

    Args:
        keywords (str): 关键词
        result_pageidx (int): 搜索结果的所在的页码，默认为 0
        result_size (int): 搜索结果的数量，默认为 10
        result_type (int): 搜索的类型
        raw_response (bool): 返回原始响应对象；
            默认为否（返回一个对结果进行 JSON 反序列化后得到的 dict）
    Raises:
        ValueError: 为参数 ``result_type`` 指定了不支持的值
        requests.RequestException: 网络、远端相关错误

    参数 ``result_type`` 为搜索的类型，支持以下值：
        - 1：歌曲
        - 10：专辑
        - 100：歌手
        - 1000：歌单
        - 1002：用户
        - 1004：MV
        - 1006：歌词
        - 1009：电台
    """
    if result_type not in (1, 10, 100, 1000, 1002, 1004, 1006, 1009):
        raise ValueError(f'不支持的搜索类型：{repr(result_type)}')

    final_keyword: str = ' '.join(keywords)

    url = 'https://music.163.com/api/cloudsearch/pc'
    payload = {
        's': final_keyword,
        'type': result_type,
        'limit': result_size,
        'offset': result_pageidx,
        'total': True
    }

    resp = requests.post(url=url, data=payload)
    resp.raise_for_status()
    if raw_response:
        return resp
    return resp.json()


def get_details_from_qqmusic(*songmids: str,
                             raw_response=False
                             ) -> dict[str, list[dict]] | list[requests.Response]:
    """从 QQ 音乐获取一首/多首歌曲的详细信息。

    QQ 音乐的查询接口只允许同时查询一首歌曲的信息，
    因此本函数的本质是对此接口的重复调用。

    Args:
        *songmids: 一个或多个歌曲 ID
        raw_response (bool): 返回一个或多个原始响应对象；
            默认为否（返回一个或多个对结果进行 JSON 反序列化后得到的 dict）
    """
    url = 'http://u.y.qq.com/cgi-bin/musicu.fcg'

    def simple_query(songmid: str) -> requests.Response:
        params = {
            'data': json.dumps(
                {
                    'songinfo': {
                        'method': 'get_song_detail_yqq',
                        'module': 'music.pf_song_detail_svr',
                        'param': {
                            'song_mid': songmid
                        }
                    }
                }
            )
        }

        resp = requests.get(url=url, params=params)
        resp.raise_for_status()
        return resp

    if raw_response:
        return [simple_query(_) for _ in songmids]
    return {'songs': [simple_query(_).json() for _ in songmids]}


def get_details_from_cloudmusic(*songids: int | str,
                                raw_response=False
                                ) -> dict | requests.Response:
    """从网易云音乐获取一首/多首歌曲的详细信息。

    Args:
        *songids: 一个或多个歌曲 ID
        raw_response (bool): 返回原始响应对象；
            默认为否（返回一个对结果进行 JSON 反序列化后得到的 dict）
    """
    songids_ = [int(_) for _ in songids]
    payload = {
        'c': json.dumps(
            [{'id': _} for _ in songids_]
        )
    }
    url = 'https://music.163.com/api/v3/song/detail'

    resp = requests.post(url=url, data=payload)
    if raw_response:
        return resp
    return resp.json()
