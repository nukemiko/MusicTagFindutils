# MusicTagFindutils

这个 Python 库可以帮助你从 QQ 音乐、网易云音乐等音乐平台上，获取指定歌曲的信息，以便之后将它们写入到音频文件的标签中。

## 安装

所需依赖：

- `requests` - 网络请求库

### PyPI

`pip install -U MusicTagFindutils`

或者[前往 PyPI 页面](https://pypi.org/project/MusicTagFindUtils)。

### 本仓库

`pip install git+https://github.com/nukemiko/MusicTagFindutils`

### 发布页

最新发布版本：https://github.com/nukemiko/MusicTagFindutils/releases/latest

提供 Wheel 包。

## 使用

- 使用网易云音乐作为信息源：

    ```pycon
    >>> from tagfindutils import cloudmusic
    >>> cloudmusic_results = cloudmusic.search('朝が来る')
    >>> matched = None
    >>> if cloudmusic_results:
    ...     matched = cloudmusic_results[0]
    ...
    >>> matched
    <
        name: 朝が来る
        trans: 拂晓将至
        aliases: TV动画《鬼灭之刃 花街篇》片尾曲
        artists: Aimer
        album: 朝が来る
        publish time: 2022-01-10 00:00:00
    >
    >>> # 以下命令输出的格式：((歌名, 歌曲 ID), ((歌手 1, 歌手 1 的 ID), (歌手 2（如果有）, 歌手 2 的 ID（如果有）), ...), (专辑名, 专辑 ID))
    >>> (matched.songname, matched.songid), tuple(zip(matched.artists, matched.artistids)), (matched.album, matched.albumid)
    (('朝が来る', 1902312104), (('Aimer', 16152),), ('朝が来る', 137312734))
    >>> matched.coverurl  # 封面图像的下载链接
    'http://p4.music.126.net/bCQCvWXXufd7XVvtg5iHkw==/109951166714320898.jpg'
    >>>
    ```

- 使用 QQ 音乐作为信息源：

    ```pycon
    >>> from tagfindutils import qqmusic
    >>> qqmusic_results = qqmusic.search('Enemies', 'The Score')
    >>> matched = None
    >>> if qqmusic_results:
    ...     matched = qqmusic_results[0]
    ...
    >>> matched
    <
        name: Enemies
        artists: The Score
        album: Enemies
        publish time: 2022-01-14 00:00:00
    >
    >>> # 以下命令输出的格式：((歌名, 歌曲 mID), ((歌手 1, 歌手 1 的 mID), (歌手 2（如果有）, 歌手 2 的 mID（如果有）), ...), (专辑名, 专辑 mID))
    >>> (matched.songname, matched.songmid), tuple(zip(matched.artists, matched.artistmids)), (matched.album, matched.albummid)
    (('Enemies', '003nYL8b2u6ygu'), (('The Score', '0023TAHr2UmE2p'),), ('Enemies', '000v14Zi196WkA'))
    >>> matched.coverurl  # 封面图像的下载链接
    'https://y.qq.com/music/photo_new/T002R800x800M000000v14Zi196WkA.jpg'
    >>>
    ```

- 从搜索结果获取歌曲的详细信息：

    ```pycon
    [...]
    >>> detail = matched.get_detail()
    >>> detail
    <
        name: Enemies
        artists: The Score
        album: Enemies
        publish time: 2022-01-14 00:00:00
        genre: Pop
        company: INgrooves
    >
    >>> # 详细信息和单个搜索结果项相比，只多了“流派（genre）”、“出版方（company）”两个属性
    >>> # 如果使用网易云音乐作为信息源，这两个属性均返回空列表，因为网易云音乐返回的详细信息不包含这两个字段
    >>> # 以下命令输出的格式：([流派 1, 流派 2（如果有）, ...], [出版方 1, 出版方 2（如果有）, ...])
    >>> (detail.genre, detail.company)
    (['Pop'], ['INgrooves'])
    >>>
    ```
