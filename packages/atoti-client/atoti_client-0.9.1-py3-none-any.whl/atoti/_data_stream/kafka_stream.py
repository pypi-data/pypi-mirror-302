from dataclasses import KW_ONLY
from datetime import timedelta
from typing import final

from pydantic.dataclasses import dataclass
from typing_extensions import override

from .._collections import FrozenMapping, frozendict
from .._identification import TableIdentifier
from .._pydantic import PYDANTIC_CONFIG as _PYDANTIC_CONFIG
from .._typing import Duration
from .data_stream import DataStream, StreamIntoTable


@final
@dataclass(config=_PYDANTIC_CONFIG, frozen=True)
class KafkaStream(DataStream):
    bootstrap_server: str
    topic: str
    group_id: str
    _: KW_ONLY
    batch_duration: Duration = timedelta(seconds=1)
    consumer_config: FrozenMapping[str, str] = frozendict()

    @override
    def _stream(
        self,
        identifier: TableIdentifier,
        /,
        *,
        scenario_name: str | None,
        stream_into_table: StreamIntoTable,
    ) -> None:
        options = {
            "bootstrapServers": self.bootstrap_server,
            "topic": self.topic,
            "consumerGroupId": self.group_id,
            "keyDeserializerClass": "org.apache.kafka.common.serialization.StringDeserializer",
            "batchDuration": int(self.batch_duration.total_seconds() * 1000),
            "additionalParameters": self.consumer_config,
        }

        stream_into_table(
            identifier,
            options=options,
            scenario_name=scenario_name,
            source_key="KAFKA",
        )
