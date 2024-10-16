from typing import Protocol, List

from .models.clickhouse_db import ClickhouseDbModel
from .models.clickhouse_disk import ClickhouseDiskModel
from .models.clickhouse_global_counter import ClickhouseGlobalCounterModel
from .models.clickhouse_partition import ClickhousePartitionModel
from .models.clickhouse_process import ClickhouseProcessModel
from .models.clickhouse_table import ClickhouseTableModel


class ClickhouseSystemProtocol(Protocol):
    """
    Provides some information / stats / data from clickhouse
    see: models/clickhouse_*.py
    """
    def get_databases(self) -> List[ClickhouseDbModel]:
        """
        system.databases
        """

    def get_database_by_name(self, name: str = '') -> 'ClickhouseDbModel':
        """
        system.databases
        """

    def get_tables_by_db(self, db: str = '') -> List[ClickhouseTableModel]:
        """
        system.tables
        """

    def get_table_partitions(self, table: str, db: str = '') -> List[ClickhousePartitionModel]:
        """
        system.parts
        """

    def get_processes(self) -> List[ClickhouseProcessModel]:
        """
        system.processes
        """

    def get_process_by_query_id(self, query_id: str) -> ClickhouseProcessModel:
        """
        system.processes
        """

    def get_disks(self) -> List[ClickhouseDiskModel]:
        """
        system.disks
        """

    def get_global_counters(self) -> ClickhouseGlobalCounterModel:
        pass


class ClickhousePartitionProtocol(Protocol):
    """
    https://clickhouse.com/docs/en/sql-reference/statements/alter/partition
    """
    def move_partitions(
        self,
        table: str,
        partitions: List[str],
        to_table: str,
        from_db: str = '',
        to_db: str = '',
        on_cluster: str = '',
    ) -> None:
        pass

    def replace_partitions(
        self,
        table: str,
        partitions: List[str],
        from_db: str = '',
        to_db: str = '',
        on_cluster: str = '',
    ) -> None:
        pass

    def drop_partitions(self, table: str, partitions: List[str], db: str = '', on_cluster: str = '') -> None:
        pass

    def drop_parts(self, table: str, parts: list, db: str = '', on_cluster: str = '') -> None:
        pass

    def freeze_partitions(
        self,
        table: str,
        partitions: List[str],
        from_db: str = '',
        to_db: str = '',
        on_cluster: str = '',
        with_name: str = '',
    ) -> None:
        pass

    def unfreeze_partitions(
        self,
        table: str,
        partitions: List[str],
        from_db: str = '',
        to_db: str = '',
        on_cluster: str = '',
        with_name: str = '',
    ) -> None:
        pass


class ClickhouseTableProtocol(Protocol):
    def create_table_as(
        self,
        table_name: str,
        from_table: str,
        db: str = '',
        from_db: str = '',
        order_by: list = None,
        partition_by: list = None,
        engine: str = '',
    ) -> None:
        """
        Creates a table with the same structure or with custom ORDER BY / PARTITION BY
        """

    def insert_from_table(self, from_table: str, to_table: str, from_db: str = '', to_db: str = '') -> None:
        """
        INSERT INTO db1.table1 SELECT * FROM db2.table2
        """


class ClickhouseProtocol(ClickhouseSystemProtocol, ClickhousePartitionProtocol, ClickhouseTableProtocol):
    def ping(self) -> bool:
        pass
