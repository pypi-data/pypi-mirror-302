from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Protocol

from .._identification import TableIdentifier


class LoadIntoTable(Protocol):
    def __call__(
        self,
        identifier: TableIdentifier,
        /,
        *,
        options: Mapping[str, object],
        scenario_name: str | None,
        source_key: str,
    ) -> None: ...


class DataLoad(ABC):
    @abstractmethod
    def _load(
        self,
        identifier: TableIdentifier,
        /,
        *,
        load_into_table: LoadIntoTable,
        scenario_name: str | None,
    ) -> None:
        pass
