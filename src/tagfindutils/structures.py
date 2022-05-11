from __future__ import annotations

from abc import abstractmethod
from datetime import datetime
from typing import Any, Generic, Type, TypeVar

T = TypeVar('T')
T_OUT = TypeVar('T_OUT')


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
        return f"<{self.__class__.__name__}, " \
               f"name: {self.songname if self.songname else 'N/A'}, " \
               f"aliases: {self.property_sep.join(self.aliases) if self.aliases else 'N/A'}, " \
               f"artists: {self.property_sep.join(self.artists) if self.artists else 'N/A'}, " \
               f"album: {self.album if self.album else 'N/A'}, " \
               f"publish time: {self.publish_time if self.publish_time else 'N/A'}>"

    @classmethod
    def type_filter(cls, value: Any | None, t: Type[T_OUT], allow_None=True) -> T_OUT | None:
        if value is None and allow_None:
            return value
        if isinstance(value, t):
            return value
        raise ValueError(f"unexpected type of value from result "
                         f"(should be '{t.__name__}', got '{type(value).__name__}')"  # type: ignore
                         )

    @abstractmethod
    def get_details(self):
        pass
