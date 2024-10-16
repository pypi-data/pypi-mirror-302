import re
from typing import List, Any, Type

from .clickhouse_base_service import ClickhouseBaseService
from ..models.clickhouse_db import ClickhouseDbModel
from ..models.clickhouse_disk import ClickhouseDiskModel
from ..models.clickhouse_global_counter import ClickhouseGlobalCounterModel
from ..models.clickhouse_partition import ClickhousePartitionModel
from ..models.clickhouse_process import ClickhouseProcessModel
from ..models.clickhouse_table import ClickhouseTableModel
from .._clickhouse_protocols import ClickhouseSystemProtocol


class ClickhouseSystemService(ClickhouseBaseService, ClickhouseSystemProtocol):
    def _exec(self, sql: str, params: dict = None, with_column_types: bool = False):
        return self._client.execute(sql, params=params, with_column_types=with_column_types)

    def _get_records(self, sql: str, model: Type = None, params: dict = None) -> List[Any]:
        data, columns = self._exec(sql, params, True)
        columns = [re.sub(r'\W', '_', name) for name, type_ in columns]
        records = []

        for rec in data:
            params = {columns[ix_]: value_ for ix_, value_ in enumerate(rec)}
            records.append(model(**params) if model else params)

        return records

    @property
    def active_db(self) -> str:
        return self._client.get_connection().database

    def get_databases(self) -> List[ClickhouseDbModel]:
        return self._get_records("""
            SELECT *
              FROM system.databases
             WHERE lower(name) != 'information_schema' AND name != 'system'
             ORDER BY name
        """, model=ClickhouseDbModel)

    def get_database_by_name(self, name: str = '') -> ClickhouseDbModel:
        name = name or self.active_db
        for schema in self.get_databases():
            if schema.name == name:
                return schema

    def get_tables_by_db(self, db: str = '') -> List[ClickhouseTableModel]:
        return self._get_records("""
            SELECT *
              FROM system.tables
             WHERE database = %(database)s
        """, params={'database': db or self.active_db}, model=ClickhouseTableModel)

    def get_table_partitions(self, table: str, db: str = '') -> List[ClickhousePartitionModel]:
        return self._get_records("""
            SELECT partition,
                   partition_id,
                   active,
                   database,
                   table,
                   sum(rows) AS rows,
                   sum(bytes_on_disk) AS bytes_on_disk,
                   sum(data_compressed_bytes) AS data_compressed_bytes,
                   sum(data_uncompressed_bytes) AS data_uncompressed_bytes,
                   max(modification_time) AS modification_time,
                   min(remove_time) AS remove_time,
                   min(last_removal_attemp_time) AS last_removal_attemp_time,
                   min(delete_ttl_info_min) AS delete_ttl_info_min,
                   max(delete_ttl_info_max) AS delete_ttl_info_max
              FROM system.parts
             WHERE database = %(database)s AND table = %(table)s
             GROUP BY database, table, partition_id, partition, active
             ORDER BY partition
        """, params={'database': db or self.active_db, 'table': table}, model=ClickhousePartitionModel)

    def get_processes(self) -> List[ClickhouseProcessModel]:
        return self._get_records('SELECT * FROM system.processes', model=ClickhouseProcessModel)

    def get_process_by_query_id(self, query_id: str) -> ClickhouseProcessModel:
        for process in self.get_processes():
            if process.query_id == query_id:
                return process

    def get_disks(self) -> List[ClickhouseDiskModel]:
        return self._get_records('SELECT * FROM system.disks', model=ClickhouseDiskModel)

    def get_global_counters(self) -> ClickhouseGlobalCounterModel:
        data = self._get_records("""
        SELECT 'processes' AS name,
                toUInt64(count()) AS value
           FROM system.processes
          UNION ALL
         SELECT 'data_compressed_bytes',
                sum(data_compressed_bytes)
           FROM system.parts
          UNION ALL
         SELECT 'data_uncompressed_bytes',
                sum(data_uncompressed_bytes)
           FROM system.parts
          UNION ALL
         SELECT 'bytes_on_disk',
                sum(bytes_on_disk)
           FROM system.parts
          UNION ALL
         SELECT 'rows',
                sum(rows)
           FROM system.parts
        """)

        rec = {}
        for item in data:
            rec[item['name']] = item['value']

        return ClickhouseGlobalCounterModel(**rec)
