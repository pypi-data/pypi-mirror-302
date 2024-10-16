from typing import List

from .clickhouse_base_service import ClickhouseBaseService
from .._clickhouse.clickhouse_partition_cmd import MovePartition
from .._clickhouse_protocols import ClickhousePartitionProtocol


class ClickhousePartitionService(ClickhouseBaseService, ClickhousePartitionProtocol):
    def move_partitions(
        self,
        table: str,
        partitions: List[str],
        to_table: str,
        from_db: str = '',
        to_db: str = '',
        on_cluster: str = '',
    ) -> None:
        for partition in partitions:
            self._client.execute(str(MovePartition(
                table=table,
                partition=partition,
                db=from_db,
                to_table=to_table,
                to_db=to_db,
                on_cluster=on_cluster,
            )))

    def replace_partitions(
        self,
        table: str,
        partitions: List[str],
        from_db: str = '',
        to_db: str = '',
        on_cluster: str = '',
    ) -> None:
        super().replace_partitions(table, partitions, from_db, to_db, on_cluster)

    def drop_partitions(
        self,
        table: str,
        partitions: List[str],
        db: str = '',
        on_cluster: str = '',
    ) -> None:
        super().drop_partitions(table, partitions, db, on_cluster)

    def drop_parts(
        self,
        table: str,
        parts: list, db: str = '',
        on_cluster: str = '',
    ) -> None:
        super().drop_parts(table, parts, db, on_cluster)

    def freeze_partitions(
        self,
        table: str,
        partitions: List[str],
        from_db: str = '',
        to_db: str = '',
        on_cluster: str = '',
        with_name: str = '',
    ) -> None:
        super().freeze_partitions(table, partitions, from_db, to_db, on_cluster, with_name)

    def unfreeze_partitions(
        self,
        table: str,
        partitions: List[str],
        from_db: str = '',
        to_db: str = '',
        on_cluster: str = '',
        with_name: str = '',
    ) -> None:
        super().unfreeze_partitions(table, partitions, from_db, to_db, on_cluster, with_name)




