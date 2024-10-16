from dataclasses import dataclass

from .base_model import BaseModel


@dataclass
class ClickhouseGlobalCounterModel(BaseModel):
    processes: int
    data_compressed_bytes: int
    data_uncompressed_bytes: int
    bytes_on_disk: int
    rows: int
