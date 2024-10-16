from typing import Any, List

from .clickhouse_system_service import ClickhouseSystemService
from .clickhouse_partition_service import ClickhousePartitionService
from .clickhouse_table_service import ClickhouseTableService
from ..models.clickhouse_db import ClickhouseDbModel
from ..models.clickhouse_disk import ClickhouseDiskModel
from ..models.clickhouse_global_counter import ClickhouseGlobalCounterModel
from ..models.clickhouse_partition import ClickhousePartitionModel
from ..models.clickhouse_process import ClickhouseProcessModel
from ..models.clickhouse_table import ClickhouseTableModel
from .._clickhouse_protocols import ClickhouseProtocol


class ClickhouseProxy(ClickhouseProtocol):
    def __init__(self, client: Any) -> None:
        self._client = client
        self._system_service = ClickhouseSystemService(client)
        self._partition_service = ClickhousePartitionService(client)
        self._table_service = ClickhouseTableService(client)

    def ping(self) -> bool:
        return self._client.get_connection().ping()

    def get_databases(self) -> List[ClickhouseDbModel]:
        return self._system_service.get_databases()

    def get_database_by_name(self, name: str = '') -> 'ClickhouseDbModel':
        return self._system_service.get_database_by_name(name)

    def get_tables_by_db(self, db: str = '') -> List[ClickhouseTableModel]:
        return self._system_service.get_tables_by_db(db)

    def get_table_partitions(self, table: str, db: str = '') -> List[ClickhousePartitionModel]:
        return self._system_service.get_table_partitions(table, db)

    def get_processes(self) -> List[ClickhouseProcessModel]:
        return self._system_service.get_processes()

    def get_process_by_query_id(self, query_id: str) -> ClickhouseProcessModel:
        return self._system_service.get_process_by_query_id(query_id)

    def get_disks(self) -> List[ClickhouseDiskModel]:
        return self._system_service.get_disks()

    def get_global_counters(self) -> ClickhouseGlobalCounterModel:
        return self._system_service.get_global_counters()

    def move_partitions(self, table: str, partitions: List[str], to_table: str, from_db: str = '', to_db: str = '',
                        on_cluster: str = '') -> None:
        self._partition_service.move_partitions(table, partitions, to_table, from_db, to_db, on_cluster)

    def create_table_as(self, table_name: str, from_table: str, db: str = '', from_db: str = '', order_by: list = None,
                        partition_by: list = None, engine: str = '') -> None:
        self._table_service.create_table_as(table_name, from_table, db, from_db, order_by, partition_by, engine)
