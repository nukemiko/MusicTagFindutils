# -*- coding: utf-8 -*-
from __future__ import annotations

from base64 import b64encode
from typing import ByteString, Sequence

from mutagen import apev2, flac, id3


def guess_picture_mime_format(picture_data: ByteString, /) -> tuple[str, str] | None:
    for header, mimetype in {
        b'\x89PNG\r\n\x1a\n'                   : ('image/png', 'png'),
        b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01': ('image/jpeg', 'jpg'),
        b'\xff\xd8\xff\xee'                    : ('image/jpeg', 'jpg'),
        b'\xff\xd8\xff\xe1'                    : ('image/jpeg', 'jpg'),
        b'BM'                                  : ('image/bmp', 'bmp')
    }.items():
        if bytes(picture_data).startswith(header):
            return mimetype


def make_flac_picture(picture_data: ByteString, picture_type: int = 3) -> flac.Picture | None:
    picture_data = bytes(picture_data)
    picture_type = int(picture_type)
    guess_result = guess_picture_mime_format(picture_data)
    if guess_result:
        mime, fmt = guess_result
        picture = flac.Picture()
        picture.mime = mime
        picture.data = picture_data
        picture.type = picture_type
        return picture


def make_vcomment_metadata_block_picture(picture_data: ByteString,
                                         picture_type: int = 3
                                         ) -> str | None:
    picture = make_flac_picture(picture_data, picture_type)
    if picture:
        return b64encode(picture.write()).decode('ascii')


def make_apev2_coverart(picture_data: ByteString) -> apev2.APEBinaryValue | None:
    picture_data = bytes(picture_data)
    guess_result = guess_picture_mime_format(picture_data)
    if guess_result:
        mime, fmt = guess_result
        value_prefix = f'Cover Art (Front).{fmt}'.encode('utf-8')
        return apev2.APEBinaryValue(value=b'\x00'.join([value_prefix, picture_data]))


def make_id3_apic(picture_data: ByteString, picture_type: int = 3) -> id3.APIC:
    picture_data = bytes(picture_data)
    picture_type = int(picture_type)
    guess_result = guess_picture_mime_format(picture_data)
    if guess_result:
        mime, fmt = guess_result
        return id3.APIC(type=picture_type, data=picture_data, mime=mime)


def str_sequence_prettify(sequence: Sequence[str], with_last_sep_spec: bool = False) -> str:
    seq = list(sequence)
    if len(seq) <= 0:
        return ''
    elif len(seq) == 1:
        return str(seq[0])
    else:
        seq_common = seq[:-1]
        seq_last = seq[-1]
        seq_common_prettified = '、'.join(seq_common)
        if with_last_sep_spec:
            seq_prettified = '和'.join([seq_common_prettified, seq_last])
        else:
            seq_prettified = '、'.join([seq_common_prettified, seq_last])

        return seq_prettified
