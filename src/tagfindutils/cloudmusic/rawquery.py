# -*- coding: utf-8 -*-
from __future__ import annotations

import requests


def get_matched_items(*keywords: str,
                      result_pageidx: int = 0,
                      result_pagesize: int = 10
                      ) -> dict:
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
    result = resp.json()
    if result['code'] >= 400:
        raise ConnectionError(
            f"query failed: remote service returns an exceptional status code "
            f"{result['code']}"
        )

    return result
