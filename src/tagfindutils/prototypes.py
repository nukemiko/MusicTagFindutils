# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Literal, TypedDict

from mutagen import apev2, flac, id3, oggvorbis

from .utils import (
    make_apev2_coverart,
    make_flac_picture,
    make_id3_apic,
    make_vcomment_metadata_block_picture,
    str_sequence_prettify
)

BINARIES_DIR = Path(__file__).parent / 'binaries'


class _KeyMaps(TypedDict):
    musicName: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TIT2]]
    artists: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TPE1]]
    album: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TALB]]
    publishDate: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TDRC]]
    copyright: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TXXX]]


@dataclass
class MusicInfo:
    def prettify(self) -> None:
        print(self)

    def __str__(self) -> str:
        strseq = ['******']
        if self.musicName:
            music_name_line = ['曲名', str(self.musicName)]
            if self.musicId is not None:
                music_name_line.append(f'<歌曲 ID> {self.musicId}')
            if self.musicMId:
                music_name_line.append(f'<歌曲 MId> {self.musicMId}')
            if self.musicTranslations and self.musicAliases:
                music_name_line.append(
                    f'<翻译> {str_sequence_prettify(self.musicTranslations)}'
                )
                music_name_line.append(
                    f'<别名> {str_sequence_prettify(self.musicAliases)}'
                )
            elif self.musicTranslations:
                music_name_line.append(
                    f'<翻译/别名> {str_sequence_prettify(self.musicTranslations)}'
                )
            elif self.musicAliases:
                music_name_line.append(
                    f'<翻译/别名> {str_sequence_prettify(self.musicAliases)}'
                )
            strseq.append('\n  '.join(music_name_line))
        if self.artistsNames:
            all_artists_line = ['歌手']
            for artist_name in self.artistsNames:
                artist_line = [f'{artist_name}']
                if artist_name in self.artistsIds:
                    artist_line.append(f' | <歌手 ID> {self.artistsIds[artist_name]}')
                if artist_name in self.artistsMIds:
                    artist_line.append(f' | <歌手 MId> {self.artistsMIds[artist_name]}')
                if artist_name in self.artistsTranslations:
                    artist_line.append(
                        f' | <翻译> '
                        f'{str_sequence_prettify(self.artistsTranslations[artist_name])}'
                    )
                if artist_name in self.artistsAliases:
                    artist_line.append(
                        f' | <别名> '
                        f'{str_sequence_prettify(self.artistsAliases[artist_name])}'
                    )
                all_artists_line.append(''.join(artist_line))
            strseq.append('\n  '.join(all_artists_line))
        if self.albumName:
            album_line = ['专辑', str(self.albumName)]
            if self.albumId is not None:
                album_line.append(f'<专辑 ID> {self.albumId}')
            if self.albumMId:
                album_line.append(f'<专辑 MId> {self.albumMId}')
            if self.albumTranslations and self.albumAliases:
                album_line.append(
                    f'<翻译> {str_sequence_prettify(self.albumTranslations)}'
                )
                album_line.append(
                    f'<别名> {str_sequence_prettify(self.artistsAliases)}'
                )
            elif self.albumTranslations:
                album_line.append(
                    f'<翻译/别名> {str_sequence_prettify(self.albumTranslations)}'
                )
            elif self.albumAliases:
                album_line.append(
                    f'<翻译/别名> {str_sequence_prettify(self.artistsAliases)}'
                )
            if self.albumCoverUrl:
                album_line.append(
                    f'<封面 URL> {self.albumCoverUrl}'
                )
            if self.albumPublishDate:
                album_line.append(
                    f'<专辑发布时间> {self.albumPublishDate.strftime("%Y年 %m月 %d日").strip()}'
                )
            strseq.append('\n  '.join(album_line))
        if self.publishDate:
            strseq.append(f'歌曲发布时间\n  {self.publishDate.strftime("%Y年 %m月 %d日").strip()}')
        if self.copyright:
            strseq.append(f'版权信息\n  {self.copyright}')

        strseq.append('******')

        return '\n'.join(strseq)

    musicName: str = ''
    musicAliases: list[str] = field(default_factory=list)
    musicTranslations: list[str] = field(default_factory=list)
    musicId: int = None
    musicMId: str = None
    artistsNames: list[str] = field(default_factory=list)
    artistsAliases: dict[str, list[str]] = field(default_factory=dict)
    artistsTranslations: dict[str, list[str]] = field(default_factory=dict)
    artistsIds: dict[str, int] = field(default_factory=dict)
    artistsMIds: dict[str, str] = field(default_factory=dict)
    albumName: str = ''
    albumAliases: list[str] = field(default_factory=list)
    albumTranslations: list[str] = field(default_factory=list)
    albumPublishDate: datetime = None
    albumId: int = None
    albumMId: str = None
    albumCoverUrl: str = ''
    albumCoverData: bytes = b''
    publishDate: datetime = None
    copyright: str = ''

    def fetch_cover_data(self) -> None:
        """下载歌曲的专辑封面图像数据（如果有），存储到 ``albumCoverData`` 字段中。

        在 ``MusicInfo`` 中，本方法什么都不做，但子类可能会改变这一行为。
        """

    def fetch_details(self) -> None:
        """尝试获取缺失的歌曲信息，存储到 ``albumCoverData`` 字段中。

        受目标音乐平台的限制，本方法不保证会填充所有字段。

        在 ``MusicInfo`` 中，本方法什么都不做，但子类可能会改变这一行为。
        """

    def to_mutagen_tag(self,
                       tag_type: Literal['APEv2', 'FLAC', 'ID3', 'VorbisComment']
                       ) -> apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis:
        """将 MusicInfo 导出为 Mutagen 库使用的标签格式实例：
        ``mutagen.apev2.APEv2``、``mutagen.flac.FLAC``、``mutagen.id3.ID3``、``mutagen.oggvorbis.OggVorbis``。

        Args:
            tag_type: 需要导出为何种格式的标签实例，仅支持 'APEv2'、'FLAC'、'ID3' 和 'VorbisComment'
        """
        if tag_type == 'APEv2':
            tag: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis = apev2.APEv2()
            keymaps: _KeyMaps = {
                'musicName'   : ('TITLE', apev2.APETextValue),
                'artistsNames': ('ARTIST', lambda _: apev2.APETextValue('\x00'.join(_))),
                'albumName'   : ('ALBUM', apev2.APETextValue),
                'publishDate' : ('YEAR', lambda _: apev2.APETextValue(str(_.year))),
                'copyright'   : ('LABEL', apev2.APETextValue),
            }

            def embed_cover(tag_: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis,
                            cover_data: bytes
                            ) -> None:
                if cover_data:
                    coverart = make_apev2_coverart(self.albumCoverData)
                    if coverart:
                        tag_['Cover Art (Front)'] = coverart
        elif tag_type == 'FLAC':
            with open(BINARIES_DIR / 'empty.flac', 'rb') as _f:
                # 受 mutagen 功能限制，编辑 FLAC 标签之前必须打开一个空 FLAC 文件
                tag: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis = flac.FLAC(_f)
            keymaps: _KeyMaps = {
                'musicName'   : ('title', lambda _: [_]),
                'artistsNames': ('artist', lambda _: list(_)),
                'albumName'   : ('album', lambda _: [_]),
                'publishDate' : ('date', lambda _: [(str(_.year))]),
                'copyright'   : ('label', lambda _: [_]),
            }

            def embed_cover(tag_: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis,
                            cover_data: bytes
                            ) -> None:
                if cover_data:
                    picture = make_flac_picture(self.albumCoverData)
                    if picture:
                        tag_.add_picture(picture)
        elif tag_type == 'ID3':
            tag: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis = id3.ID3()
            keymaps: _KeyMaps = {
                'musicName'   : ('TIT2', lambda _: id3.TIT2(text=[_], encoding=3)),
                'artistsNames': ('TPE1', lambda _: id3.TPE1(text=list(_), encoding=3)),
                'albumName'   : ('TALB', lambda _: id3.TALB(text=[_], encoding=3)),
                'publishDate' : ('TDRC', lambda _: id3.TDRC(text=[str(_.year)], encoding=3)),
                'copyright'   : ('TXXX:LABEL', lambda _: id3.TXXX(text=[_], desc='LABEL', encoding=3)),
            }

            def embed_cover(tag_: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis,
                            cover_data: bytes
                            ) -> None:
                if cover_data:
                    apic = make_id3_apic(self.albumCoverData)
                    if apic:
                        tag_['APIC:'] = apic
        elif tag_type == 'VorbisComment':
            # 受 mutagen 功能限制，编辑 OggVorbis 标签之前必须打开一个空 OggVorbis 文件
            with open(BINARIES_DIR / 'empty.ogg', 'rb') as _f:
                tag: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis = oggvorbis.OggVorbis(_f)
            keymaps: _KeyMaps = {
                'musicName'   : ('title', lambda _: [_]),
                'artistsNames': ('artist', lambda _: list(_)),
                'albumName'   : ('album', lambda _: [_]),
                'publishDate' : ('date', lambda _: [(str(_.year))]),
                'copyright'   : ('label', lambda _: [_]),
            }

            def embed_cover(tag_: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis,
                            cover_data: bytes
                            ) -> None:
                if cover_data:
                    mbp = make_vcomment_metadata_block_picture(self.albumCoverData)
                    if mbp:
                        tag_['metadata_block_picture'] = [mbp]
        else:
            raise ValueError(
                "'tag_type' must in 'APEv2', 'FLAC', 'ID3' or 'VorbisComment', not "
                f"{repr(tag_type)}"
            )

        tagkey_constructor: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.Frame]]
        for attrname, tagkey_constructor in keymaps.items():
            tagkey, constructor = tagkey_constructor
            attr = getattr(self, attrname)
            if attr:
                tag[tagkey] = constructor(attr)

        embed_cover(tag, self.albumCoverData)

        return tag
