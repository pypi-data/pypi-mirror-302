from typing import Any

from ._clickhouse.clickhouse_proxy import ClickhouseProxy as _ClickhouseProxy
from ._clickhouse_protocols import ClickhouseProtocol


def from_clickhouse_driver(client: Any) -> ClickhouseProtocol:
    return _ClickhouseProxy(client)
