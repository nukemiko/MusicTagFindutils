from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Generic, Type

from .utils import T, T_OUT, type_filter


class SearchResult(Generic[T]):
    @property
    @abstractmethod
    def album(self) -> str | None:
        pass

    @property
    @abstractmethod
    def albumid(self) -> int | None:
        pass

    @property
    @abstractmethod
    def aliases(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def translations(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def artists(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def artistids(self) -> list[int]:
        pass

    @property
    @abstractmethod
    def coverurl(self) -> str | None:
        pass

    @property
    @abstractmethod
    def songname(self) -> str | None:
        pass

    @property
    @abstractmethod
    def songid(self) -> int | None:
        pass

    @property
    @abstractmethod
    def publish_time(self) -> datetime | None:
        pass

    @property
    def property_sep(self) -> str:
        return '、'

    def __repr__(self) -> str:
        ret_strseg = ['<']

        if self.songname:
            ret_strseg.append(f'name: {self.songname}')
        else:
            ret_strseg.append(f'noname')
        if self.translations:
            ret_strseg.append(f'trans: {self.property_sep.join(self.translations)}')
        if self.aliases:
            ret_strseg.append(f'aliases: {self.property_sep.join(self.aliases)}')
        if self.artists:
            ret_strseg.append(f'artists: {self.property_sep.join(self.artists)}')
        if self.album:
            ret_strseg.append(f'album: {self.album}')
        if self.publish_time:
            ret_strseg.append(f'publish time: {self.publish_time}')

        if len(ret_strseg) <= 1:
            ret_strseg.append('empty result')

        return '\n    '.join(ret_strseg) + '\n>'

    @classmethod
    def type_filter(cls, value: Any, t: Type[T_OUT], allow_None=True) -> T_OUT:
        return type_filter(value=value, t=t, allow_None=allow_None)

    def get_detail(self) -> SongDetail | None:
        pass


class SongDetail(SearchResult):
    @property
    @abstractmethod
    def album(self) -> str | None:
        pass

    @property
    @abstractmethod
    def albumid(self) -> int | None:
        pass

    @property
    @abstractmethod
    def aliases(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def translations(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def artists(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def artistids(self) -> list[int]:
        pass

    @property
    @abstractmethod
    def coverurl(self) -> str | None:
        pass

    @property
    @abstractmethod
    def songname(self) -> str | None:
        pass

    @property
    @abstractmethod
    def songid(self) -> int | None:
        pass

    @property
    @abstractmethod
    def publish_time(self) -> datetime | None:
        pass

    @property
    @abstractmethod
    def genre(self) -> list[str]:
        pass

    @property
    @abstractmethod
    def company(self) -> list[str]:
        pass

    def __repr__(self) -> str:
        ret_strseg = ['<']

        if self.songname:
            ret_strseg.append(f'name: {self.songname}')
        else:
            ret_strseg.append(f'noname')
        if self.translations:
            ret_strseg.append(f'trans: {self.property_sep.join(self.translations)}')
        if self.aliases:
            ret_strseg.append(f'aliases: {self.property_sep.join(self.aliases)}')
        if self.artists:
            ret_strseg.append(f'artists: {self.property_sep.join(self.artists)}')
        if self.album:
            ret_strseg.append(f'album: {self.album}')
        if self.publish_time:
            ret_strseg.append(f'publish time: {self.publish_time}')
        if self.genre:
            ret_strseg.append(f'genre: {self.property_sep.join(self.genre)}')
        if self.company:
            ret_strseg.append(f'company: {self.property_sep.join(self.company)}')

        if len(ret_strseg) <= 1:
            ret_strseg.append('empty result')

        return '\n    '.join(ret_strseg) + '\n>'

    def get_detail(self) -> SongDetail:
        return self
