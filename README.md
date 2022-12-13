# MusicTagFindutils

这个 Python 库可以帮助你从 QQ 音乐、网易云音乐等平台上，根据一个或多个关键词查询相关信息，以便之后将它们写入到相关音频文件的标签中。

## 重要事项

你现在看到的 README 来源于 0.2.0 开发分支。

0.2.x 相较于 0.1.x，在接口调用方式上存在巨大变化，因此针对 0.1.x 制作的程序无法使用 0.2.x 版本的 MusicTagFindutils。

## 安装

所需依赖：

-   `requests` >= 2.4.2 - 网络请求库
-   `mutagen` - 导出歌曲信息为标签

### PyPI

~~`pip install -U MusicTagFindUtils`~~

_目前不可用_

### 本仓库

`pip install -U git+https://github.com/nukemiko/MusicTagFindutils/tree/0.2.0`

**注意：如果你通过此方式安装，则需要频繁更新，因为本仓库也会频繁接受开发者推送的提交。**

### 发布页

~~最新发布版本：https://github.com/nukemiko/MusicTagFindutils/releases/latest~~

_目前不可用_

## 使用

_此分支自提交 c9b404414ca6cfff91a60f67c6a77331da2f2e88 开始，就可以通过网易云音乐查询歌曲信息。_

### 网易云音乐

```pycon
>>> from tagfindutil import cloudmusic
>>>
>>> results = cloudmusic.search('祭果ての花')
>>> len(results)
8
>>> max_relative = results[0]
>>> max_relative
MusicInfoFromCloudMusic(musicName='祭果ての花', musicAliases=['SPECIAL TRACK'], musicTranslations=[], musicId=515647346, musicMId=None, artistsNames=['中恵光城', '霜月はるか'], artistsAliases={'中恵光城': ['なかえ みつき', 'Mitsuki Nakae']}, artistsTranslations={'霜月はるか': ['霜月遥']}, artistsIds={'中恵光城': 18347, '霜月はるか': 17647}, artistsMIds={}, albumName='Another Flower Special Live 2017 Cross bouquet Live CD', albumAliases=[], albumTranslations=[], albumPublishDate=None, albumId=36525858, albumMId=None, albumCoverUrl='http://p4.music.126.net/XGlidJ4kCyP054jMNE_77w==/109951163052923671.jpg', albumCoverData=b'', publishDate=datetime.datetime(2017, 10, 29, 0, 0), copyright='')
>>> max_relative.prettify()  # 美观地查看歌曲信息，等效于 print(max_relative)
******
曲名
  祭果ての花
  <歌曲 ID> 515647346
  <翻译/别名> SPECIAL TRACK
歌手
  中恵光城 | <歌手 ID> 18347 | <别名> なかえ みつき、Mitsuki Nakae
  霜月はるか | <歌手 ID> 17647 | <翻译> 霜月遥
专辑
  Another Flower Special Live 2017 Cross bouquet Live CD
  <专辑 ID> 36525858
  <封面 URL> http://p4.music.126.net/XGlidJ4kCyP054jMNE_77w==/109951163052923671.jpg
歌曲发布时间
  2017年 10月 29日
******
>>> max_relative.fetch_cover_data()  # 获取封面信息，必须手动进行
>>>
```

### QQ 音乐

_敬请期待_

### 导出为 Mutagen 兼容格式的标签实例

支持以下标签格式（传递给 `max_relative.to_mutagen_tag()`）：

-   `'APEv2'`（APE/Monkey's Audio）
-   `'FLAC'`（FLAC）
-   `'ID3'`（MP3、TTA 等）
-   `'VorbisComment'`（OGG）

```pycon
>>> flactag = max_relative.to_mutagen_tag('FLAC')
>>> flactag
{'album': ['Another Flower Special Live 2017 Cross bouquet Live CD'], 'artist': ['中恵光城', '霜月はるか'], 'date': ['2017'], 'title': ['祭果ての花']}
>>> flactag.pictures
[<Picture 'image/jpeg' (223401 bytes)>]
>>> max_relative.to_mutagen_tag('ID3')
{'TIT2': TIT2(encoding=<Encoding.UTF8: 3>, text=['祭果ての花']), 'TPE1': TPE1(encoding=<Encoding.UTF8: 3>, text=['中恵光城', '霜月はるか']), 'TALB': TALB(encoding=<Encoding.UTF8: 3>, text=['Another Flower Special Live 2017 Cross bouquet Live CD']), 'TDRC': TDRC(encoding=<Encoding.UTF8: 3>, text=['2017']), 'APIC:': APIC(encoding=<Encoding.UTF16: 1>, mime='image/jpeg', type=<PictureType.COVER_FRONT: 3>, desc='', data=b'...')}
>>>
```

### 更新已有文件的标签

#### ID3/APEv2/VorbisComment

此处以 ID3 为例。

```pycon
>>> id3tag = max_relative.to_mutagen_tag('ID3')
>>>
>>> from mutagen import mp3
>>> exists_mp3tag = mp3.MP3('target.mp3')  # 打开已有文件的标签
>>> exists_mp3tag.clear()  # 清空已有标签，可选步骤
>>> exists_mp3tag.update(id3tag)  # 使用导出的标签更新源文件的标签
>>> exists_mp3tag.save()  # 保存更新后的标签到文件
>>>
```

#### FLAC（需要一些额外步骤）

```pycon
>>> flactag = max_relative.to_mutagen_tag('FLAC')
>>>
>>> from mutagen import flac
>>> exists_flactag = mp3.MP3('target.mp3')  # 打开已有文件的标签
>>> exists_flactag.clear()  # 清空已有标签，可选步骤
>>> exists_flactag.update(flactag)  # 使用导出的标签更新源文件的标签
>>> exists_flactag.clear_pictures()  # 额外步骤 1：清空源文件已有的内嵌图片，可选
>>> if len(flactag.pictures) != 0:  # 额外步骤 2：添加封面
...     exists_flactag.add_picture(flactag.pictures[0])
>>> exists_flactag.save()  # 保存更新后的标签到文件
>>>
```
