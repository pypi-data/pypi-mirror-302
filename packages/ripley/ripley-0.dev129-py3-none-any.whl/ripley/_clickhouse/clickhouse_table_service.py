from .clickhouse_base_service import ClickhouseBaseService
from .._clickhouse_protocols import ClickhouseTableProtocol
from .._sql_cmd.base_sql_cmd import Table


class ClickhouseTableService(ClickhouseBaseService, ClickhouseTableProtocol):
    def create_table_as(self, table_name: str, from_table: str, db: str = '', from_db: str = '', order_by: list = None,
                        partition_by: list = None, engine: str = '') -> None:
        if partition_by:
            partition_by = f'PARTITION BY {", ".join(partition_by)}'

        if order_by:
            order_by = f'ORDER BY {", ".join(order_by)}'

        if not all([order_by, partition_by, engine]):
            params = self._client.execute("""
                SELECT engine_full
                  FROM system.tables
                 WHERE database = %(from_db)s AND name = %(from_table)s
                 LIMIT 1
                """, params={'from_db': from_db or self.active_db, 'from_table': from_table},
            )

            full: str = params[0][0]
            full_low = full.lower()
            if not engine:
                engine = full[0:full_low.find(' partition by')]

            if not partition_by:
                partition_by = full[
                   full_low.find('partition by', 1):full_low.find('order by', 1)
                ]

            if not order_by:
                order_by = full[
                   full_low.find('order by', 1):full_low.rfind('settings', 1)
                ]

        self._client.execute(f"""
            CREATE TABLE {Table(table_name, db)}
            engine = {engine}
            {order_by}
            {partition_by}
            AS {Table(from_table, from_db)};
        """)

    def insert_from_table(self, from_table: str, to_table: str, from_db: str = '', to_db: str = '') -> None:
        super().insert_from_table(from_table, to_table, from_db, to_db)
