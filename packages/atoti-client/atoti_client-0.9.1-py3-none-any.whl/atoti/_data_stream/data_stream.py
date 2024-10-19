from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Protocol

from .._identification import TableIdentifier


class StreamIntoTable(Protocol):
    def __call__(
        self,
        identifier: TableIdentifier,
        /,
        *,
        options: Mapping[str, object],
        scenario_name: str | None,
        source_key: str,
    ) -> None: ...


class DataStream(ABC):
    @abstractmethod
    def _stream(
        self,
        identifier: TableIdentifier,
        /,
        *,
        scenario_name: str | None,
        stream_into_table: StreamIntoTable,
    ) -> None:
        pass
