from __future__ import annotations

from . import cloudmusic
from . import qqmusic
from .structures import SearchResult

__VERSION__ = '0.1.2'


def supported_sources():
    """列出支持的歌曲信息搜索来源，以及对应的搜索入口函数。

    目前支持的搜索来源：

    - cloudmusic - 网易云音乐
    - qqmusic - QQ 音乐
    """
    return {
        'cloudmusic': cloudmusic.search,
        'qqmusic': qqmusic.search
    }
