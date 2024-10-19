from dataclasses import KW_ONLY
from pathlib import Path
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._collections import FrozenMapping, frozendict
from .._data_source.parquet import (
    create_parquet_params as _get_options,
)
from .._identification import TableIdentifier
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from .._split_globfree_absolute_path_and_glob_pattern import (
    split_globfree_absolute_path_and_glob_pattern,
)
from ..client_side_encryption_config import ClientSideEncryptionConfig
from .data_load import DataLoad, LoadIntoTable


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class ParquetLoad(DataLoad):
    path: Path | str
    _: KW_ONLY
    columns: FrozenMapping[str, str] = frozendict()
    client_side_encryption: ClientSideEncryptionConfig | None = None

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
            split_globfree_absolute_path_and_glob_pattern(self.path, ".parquet")
        )

        options = _get_options(
            globfree_absolute_path,
            glob_pattern=glob_pattern,
            columns=self.columns,
            client_side_encryption=self.client_side_encryption,
        )

        load_into_table(
            identifier,
            options=options,
            scenario_name=scenario_name,
            source_key="PARQUET",
        )
