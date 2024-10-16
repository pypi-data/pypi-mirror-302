from typing import Protocol


class SqlProtocol(Protocol):
    def __str__(self) -> str:
        pass


class Table(SqlProtocol):
    def __init__(self, name: str, db: str = ''):
        self._name = name
        self._db = db

    def __str__(self) -> str:
        return f'{self._db}.{self._name}' if self._db else self._name


class BaseAlter(SqlProtocol):
    def __init__(self, table: str, db: str = ''):
        self._table = table
        self._db = db

    def __str__(self) -> str:
        return f'ALTER TABLE {Table(self._table, self._db)}'
