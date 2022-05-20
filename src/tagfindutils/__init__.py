from __future__ import annotations

from typing import Any, Callable, List, Union

from . import cloudmusic
from . import qqmusic
from .structures import SearchResult

__VERSION__ = '0.1.0'

SearchFunc = Union[
    Callable[[Any], List[cloudmusic.CloudMusicSearchResult]],
    Callable[[Any], List[qqmusic.QQMusicSearchResult]]
]


def supported_sources() -> dict[str, SearchFunc]:
    """列出支持的歌曲信息搜索来源，以及对应的搜索入口函数。

    目前支持的搜索来源：

    - cloudmusic - 网易云音乐
    - qqmusic - QQ 音乐
    """
    return {
        'cloudmusic': cloudmusic.search,
        'qqmusic': qqmusic.search
    }
