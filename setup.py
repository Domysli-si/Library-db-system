import json
import pyodbc
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config" / "config.json"
SQL_DIR = BASE_DIR / "sql"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def connect_master(cfg):
    return pyodbc.connect(
        f"DRIVER={cfg['driver']};"
        f"SERVER={cfg['server']};"
        f"UID={cfg['username']};"
        f"PWD={cfg['password']};"
        f"DATABASE=master;",
        autocommit=True
    )

def execute_sql_file(cursor, path):
    with open(path, "r") as f:
        sql = f.read()
    for stmt in sql.split("GO"):
        if stmt.strip():
            cursor.execute(stmt)

def main():
    cfg = load_config()

    conn = connect_master(cfg)
    cursor = conn.cursor()

    cursor.execute(f"""
        IF DB_ID('{cfg['database']}') IS NULL
        CREATE DATABASE {cfg['database']}
    """)

    conn.close()

    conn = pyodbc.connect(
        f"DRIVER={cfg['driver']};"
        f"SERVER={cfg['server']};"
        f"UID={cfg['username']};"
        f"PWD={cfg['password']};"
        f"DATABASE={cfg['database']};"
    )
    cursor = conn.cursor()

    execute_sql_file(cursor, SQL_DIR / "ddl.sql")
    execute_sql_file(cursor, SQL_DIR / "views.sql")

    conn.commit()
    conn.close()

    print("Database setup completed.")

if __name__ == "__main__":
    main()

