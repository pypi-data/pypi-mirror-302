from dataclasses import KW_ONLY
from pathlib import Path
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._collections import FrozenMapping, FrozenSequence, frozendict
from .._data_source.csv import create_csv_params as _get_options
from .._identification import TableIdentifier
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from .._split_globfree_absolute_path_and_glob_pattern import (
    split_globfree_absolute_path_and_glob_pattern,
)
from ..client_side_encryption_config import ClientSideEncryptionConfig
from .data_load import DataLoad, LoadIntoTable


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class CsvLoad(DataLoad):
    path: Path | str
    _: KW_ONLY
    columns: FrozenMapping[str, str] | FrozenSequence[str] = frozendict()
    separator: str | None = ","
    encoding: str = "utf-8"
    process_quotes: bool | None = True
    array_separator: str | None = None
    date_patterns: FrozenMapping[str, str] = frozendict()
    client_side_encryption: ClientSideEncryptionConfig | None = None
    parser_thread_count: int | None = None
    """:meta private:"""
    buffer_size_kb: int | None = None
    """:meta private:"""

    @override
    def _load(
        self,
        identifier: TableIdentifier,
        /,
        *,
        load_into_table: LoadIntoTable,
        scenario_name: str | None,
    ) -> None:
        globfree_absolute_path, glob_pattern = (
            split_globfree_absolute_path_and_glob_pattern(self.path, ".csv")
        )

        options = _get_options(
            globfree_absolute_path,
            columns=self.columns,
            separator=self.separator,
            encoding=self.encoding,
            process_quotes=self.process_quotes,
            array_separator=self.array_separator,
            glob_pattern=glob_pattern,
            date_patterns=self.date_patterns,
            client_side_encryption=self.client_side_encryption,
            parser_thread_count=self.parser_thread_count,
            buffer_size_kb=self.buffer_size_kb,
        )

        load_into_table(
            identifier,
            options=options,
            scenario_name=scenario_name,
            source_key="CSV",
        )
