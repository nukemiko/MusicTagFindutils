# -*- coding: utf-8 -*-
from __future__ import annotations

import datetime
import json
import math
import random
import time

import requests


def _rawquery_gen_search_id(n: int) -> int:
    t = n * 18014398509481984
    a = math.ceil(random.random() * 4194304) * 4294967296
    o = datetime.datetime.now()
    r = 1000 * (3600 * o.hour + 60 * o.minute + o.second + o.microsecond)

    return t + a + r


def rawquery_get_matched_items(*keywords: str,
                               result_pageidx: int = 0,
                               result_pagesize: int = 10,
                               user_agent: str = None
                               ) -> dict:
    """从 QQ 音乐搜索与关键字 ``*keywords`` 匹配/相关的信息。

    发送查询请求时，默认使用以下用户代理（User Agent）字符串：

    ``'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/17D50 UCBrowser/12.8.2.1268 Mobile AliApp(TUnionSDK/0.1.20.3)'``

    可通过指定参数 ``user_agent`` 覆盖此设置。

    Args:
        keywords (str): 关键字，可接受多个
        result_pageidx (int): 搜索结果所在的页码，默认为 0
        result_pagesize (int): 搜索结果的数量，默认为 10
        user_agent (str): 发送查询请求时使用的用户代理（User Agent）字符串
    Raises:
        requests.RequestException: 网络请求相关异常
        ConnectionError: 网络请求正常，但远端服务返回表示报错的状态码
    """
    if not keywords:
        raise ValueError("no keywords were provided")
    final_keyword = ' '.join(keywords)
    search_id = _rawquery_gen_search_id(3)
    payload_asdict = {
        'comm' : {
            'g_tk'       : 997034911,
            'uin'        : ''.join(random.sample('1234567890', 10)),
            'format'     : 'json',
            'inCharset'  : 'utf-8',
            'outCharset' : 'utf-8',
            'notice'     : 0,
            'platform'   : 'h5',
            'needNewCode': 1,
            'ct'         : 23,
            'cv'         : 0
        },
        'req_0': {
            'method': 'DoSearchForQQMusicDesktop',
            'module': 'music.search.SearchCgiService',
            'param' : {
                'remoteplace' : 'txt.mqq.all',
                'searchid'    : search_id,
                'query'       : final_keyword,
                'search_type' : 0,
                'page_num'    : int(result_pageidx),
                'num_per_page': int(result_pagesize)
            }
        }
    }
    if user_agent is None:
        user_agent = """Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X; zh-CN) AppleWebKit/537.51.1 (KHTML, like Gecko) Mobile/17D50 UCBrowser/12.8.2.1268 Mobile AliApp(TUnionSDK/0.1.20.3) """
    elif not isinstance(user_agent, str):
        raise TypeError(f"'user_agent' must be str or None, not {type(user_agent).__name__}")

    resp = requests.post(
        url='https://u.y.qq.com/cgi-bin/musicu.fcg?'
            f'_webcgikey=DoSearchForQQMusicDesktop&_={int(round(time.time() * 1000))}',
        headers={
            'Accept'         : '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Referer'        : 'https://y.qq.com/',
            'User-Agent'     : user_agent
        },
        data=json.dumps(payload_asdict, ensure_ascii=False).encode('utf-8')
    )

    resp.raise_for_status()
    result = resp.json()
    if result['req_0']['code'] != 0:
        raise ConnectionError(
            f"query failed: remote service returns an exceptional status code "
            f"{result['req_0']['code']}"
        )

    return result
