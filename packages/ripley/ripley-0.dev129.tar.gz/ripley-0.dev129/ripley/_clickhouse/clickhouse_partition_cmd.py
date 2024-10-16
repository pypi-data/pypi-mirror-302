from .._sql_cmd.base_sql_cmd import Table
from .clickhouse_cmd import ClickHouseAlterCmd


class MovePartition(ClickHouseAlterCmd):
    def __init__(self, table: str, partition: str, to_table, db: str = '', to_db: str = '', on_cluster: str = ''):
        super().__init__(table, db, on_cluster)
        self._to_table = to_table
        self._partition = partition
        self._db = db
        self._to_db = to_db

    def __str__(self) -> str:
        cmd = super().__str__()
        return f"{cmd} MOVE PARTITION '{self._partition}' TO TABLE {Table(self._to_table, self._to_db)}"
