from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from .base_model import BaseModel


@dataclass
class ClickhouseTableModel(BaseModel):
    active_parts: int
    as_select: str

    database: str
    data_paths: List[str]
    dependencies_database: List[str]
    dependencies_table: List[str]

    comment: str
    create_table_query: str

    name: str

    engine: str
    engine_full: str

    uuid: UUID

    metadata_path: str
    metadata_modification_time: datetime

    parts: int
    partition_key: str
    primary_key: str

    sampling_key: str
    storage_policy: str
    sorting_key: str

    is_temporary: int

    total_bytes: int
    total_rows: int
    total_marks: int

    lifetime_rows: int
    lifetime_bytes: int

    has_own_data: int

    loading_dependencies_database: List[str]
    loading_dependencies_table: List[str]
    loading_dependent_database: List[str]
    loading_dependent_table: List[str]

    def __eq__(self, __value):
        return isinstance(__value, ClickhouseTableModel) and self.__dict__ == __value.__dict__
