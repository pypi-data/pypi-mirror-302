from dataclasses import dataclass
from datetime import datetime

from .base_model import BaseModel


@dataclass
class ClickhousePartitionModel(BaseModel):
    database: str
    table: str
    partition: str
    partition_id: str
    active: int
    rows: int
    bytes_on_disk: int
    data_compressed_bytes: int
    data_uncompressed_bytes: int
    delete_ttl_info_max: int
    modification_time: datetime
    remove_time: datetime
    last_removal_attemp_time: datetime
    delete_ttl_info_min: datetime

    def __eq__(self, __value):
        return isinstance(__value, ClickhousePartitionModel) and self.__dict__ == __value.__dict__
