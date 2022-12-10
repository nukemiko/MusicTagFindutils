# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Literal, TypedDict

from mutagen import apev2, flac, id3, oggvorbis
from locale import getlocale

from .utils import make_apev2_coverart, make_flac_picture, make_id3_apic, make_vcomment_metadata_block_picture

BINARIES_DIR = Path(__file__).parent / 'binaries'

LANGCODE, ENCODING = getlocale()


class _KeyMaps(TypedDict):
    musicName: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TIT2]]
    artists: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TPE1]]
    album: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TALB]]
    publishDate: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TDRC]]
    copyright: tuple[str, Callable[[str], apev2.APETextValue] | Callable[[str], list[str]] | Callable[[str], id3.TXXX]]


@dataclass
class MusicInfo:
    musicName: str = ''
    musicId: int = 0
    artists: list[str] = field(default_factory=list)
    artistsIds: dict[str, int] = field(default_factory=dict)
    album: str = ''
    albumId: int = 0
    aliases: list[str] = field(default_factory=list)
    translations: list[str] = field(default_factory=list)
    coverUrl: str = ''
    coverData: bytes = ''
    publishDate: datetime = None
    copyright: str = ''

    def to_mutagen_tag(self,
                       tag_type: Literal['APEv2', 'FLAC', 'ID3', 'VorbisComment']
                       ) -> apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis:
        if tag_type == 'APEv2':
            tag: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis = apev2.APEv2()
            keymaps: _KeyMaps = {
                'musicName'  : ('TITLE', apev2.APETextValue),
                'artists'    : ('ARTIST', lambda _: apev2.APETextValue('\x00'.join(_))),
                'album'      : ('ALBUM', apev2.APETextValue),
                'publishDate': ('YEAR', lambda _: apev2.APETextValue(str(_.year))),
                'copyright'  : ('LABEL', apev2.APETextValue),
            }

            def embed_cover(tag_: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis,
                            cover_data: bytes
                            ) -> None:
                if cover_data:
                    coverart = make_apev2_coverart(self.coverData)
                    if coverart:
                        tag_['Cover Art (Front)'] = coverart
        elif tag_type == 'FLAC':
            with open(BINARIES_DIR / 'empty.flac', 'rb') as _f:
                # 受 mutagen 功能限制，编辑 FLAC 标签之前必须打开一个空 FLAC 文件
                tag: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis = flac.FLAC(_f)
            keymaps: _KeyMaps = {
                'musicName'  : ('title', lambda _: [_]),
                'artists'    : ('artist', lambda _: list(_)),
                'album'      : ('album', lambda _: [_]),
                'publishDate': ('date', lambda _: [(str(_.year))]),
                'copyright'  : ('label', lambda _: [_]),
            }

            def embed_cover(tag_: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis,
                            cover_data: bytes
                            ) -> None:
                if cover_data:
                    picture = make_flac_picture(self.coverData)
                    if picture:
                        tag_.add_picture(picture)
        elif tag_type == 'ID3':
            tag: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis = id3.ID3()
            keymaps: _KeyMaps = {
                'musicName'  : ('TIT2', lambda _: id3.TIT2(text=[_], encoding=3)),
                'artists'    : ('TPE1', lambda _: id3.TPE1(text=list(_), encoding=3)),
                'album'      : ('TALB', lambda _: id3.TALB(text=[_], encoding=3)),
                'publishDate': ('TDRC', lambda _: id3.TDRC(text=[str(_.year)], encoding=3)),
                'copyright'  : ('TXXX:LABEL', lambda _: id3.TXXX(text=[_], desc='LABEL', encoding=3)),
            }

            def embed_cover(tag_: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis,
                            cover_data: bytes
                            ) -> None:
                if cover_data:
                    apic = make_id3_apic(self.coverData)
                    if apic:
                        tag_['APIC:'] = apic
        elif tag_type == 'VorbisComment':
            # 受 mutagen 功能限制，编辑 OggVorbis 标签之前必须打开一个空 OggVorbis 文件
            with open(BINARIES_DIR / 'empty.ogg', 'rb') as _f:
                tag: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis = oggvorbis.OggVorbis(_f)
            keymaps: _KeyMaps = {
                'musicName'  : ('title', lambda _: [_]),
                'artists'    : ('artist', lambda _: list(_)),
                'album'      : ('album', lambda _: [_]),
                'publishDate': ('date', lambda _: [(str(_.year))]),
                'copyright'  : ('label', lambda _: [_]),
            }

            def embed_cover(tag_: apev2.APEv2 | flac.FLAC | id3.ID3 | oggvorbis.OggVorbis,
                            cover_data: bytes
                            ) -> None:
                if cover_data:
                    mbp = make_vcomment_metadata_block_picture(self.coverData)
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

        embed_cover(tag, self.coverData)

        return tag
