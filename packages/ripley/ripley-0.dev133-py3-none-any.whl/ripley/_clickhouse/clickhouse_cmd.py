from .._sql_cmd.base_sql_cmd import BaseAlter


class ClickHouseAlterCmd(BaseAlter):
    def __init__(self, table: str, db: str = '', on_cluster: str = ''):
        super().__init__(table, db)
        self._on_cluster = on_cluster

    def __str__(self) -> str:
        cmd = super().__str__()
        cmd = f"{cmd} ON CLUSTER '{self._on_cluster}'" if self._on_cluster else cmd
        return cmd
