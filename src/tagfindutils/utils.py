# -*- coding: utf-8 -*-
from __future__ import annotations


def guess_picture_mimetype(picture_data: bytes | bytearray, /) -> str | None:
    for header, mimetype in {
        b'\x89PNG\r\n\x1a\n'                   : 'image/png',
        b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01': 'image/jpeg',
        b'\xff\xd8\xff\xee'                    : 'image/jpeg',
        b'\xff\xd8\xff\xe1'                    : 'image/jpeg',
        b'BM'                                  : 'image/bmp'
    }.items():
        if picture_data.startswith(header):
            return mimetype
