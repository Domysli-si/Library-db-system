import json
import pyodbc
from contextlib import contextmanager


class DatabaseError(Exception):
    pass


class DatabaseConnection:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> dict:
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise DatabaseError(f"Failed to load config file: {e}")

    def connect(self):
        try:
            return pyodbc.connect(
                f"DRIVER={{{self._config['driver']}}};"
                f"SERVER={self._config['server']};"
                f"DATABASE={self._config['database']};"
                f"UID={self._config['username']};"
                f"PWD={self._config['password']}",
                autocommit=False
            )
        except Exception as e:
            raise DatabaseError(f"Database connection failed: {e}")

    @contextmanager
    def transaction(self):
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

