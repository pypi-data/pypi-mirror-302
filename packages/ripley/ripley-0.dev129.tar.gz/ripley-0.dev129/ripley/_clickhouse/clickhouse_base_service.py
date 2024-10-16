from typing import Any


class ClickhouseBaseService:
    def __init__(self, client: Any) -> None:
        self._client = client

    @property
    def active_db(self) -> str:
        return self._client.get_connection().database
