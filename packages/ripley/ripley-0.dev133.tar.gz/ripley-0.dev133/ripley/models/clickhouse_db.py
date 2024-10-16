from dataclasses import dataclass
from typing import Any
from uuid import UUID

from .base_model import BaseModel


@dataclass
class ClickhouseDbModel(BaseModel):
    name: str
    engine: str
    data_path: str
    metadata_path: str
    uuid: UUID
    engine_full: str
    comment: str

    def __eq__(self, __value: Any):
        return isinstance(__value, ClickhouseDbModel) and self.__dict__ == __value.__dict__
