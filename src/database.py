import sqlite3
import pandas as pd
from .config import DB_PATH

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def initialize_database():
    with connect() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY, order_date TEXT, region TEXT, product TEXT,
            category TEXT, quantity INTEGER, revenue REAL, cost REAL, customer_segment TEXT
        )""")
        count = con.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
        if count == 0:
            rows = [
                ("2026-01-12","North","Laptop","Electronics",3,3600,2700,"Enterprise"),
                ("2026-02-03","South","Phone","Electronics",8,6400,4800,"Consumer"),
                ("2026-03-18","West","Desk","Furniture",5,2500,1500,"SMB"),
                ("2026-04-05","North","Phone","Electronics",6,4800,3600,"Consumer"),
                ("2026-05-21","East","Chair","Furniture",10,1800,900,"SMB"),
                ("2026-06-11","South","Laptop","Electronics",4,4800,3600,"Enterprise"),
                ("2026-07-09","West","Monitor","Electronics",7,2100,1400,"SMB"),
                ("2026-08-14","East","Laptop","Electronics",2,2400,1800,"Enterprise"),
                ("2026-09-02","North","Desk","Furniture",4,2000,1200,"SMB"),
                ("2026-09-19","South","Chair","Furniture",9,1620,810,"Consumer"),
            ]
            con.executemany("""INSERT INTO sales
            (order_date,region,product,category,quantity,revenue,cost,customer_segment)
            VALUES (?,?,?,?,?,?,?,?)""", rows)

def run_readonly_query(sql: str):
    normalized = sql.strip().lower()
    if not normalized.startswith(("select", "with")) or any(x in normalized for x in ("insert ", "update ", "delete ", "drop ", "alter ", "attach ")):
        raise ValueError("Only read-only SELECT queries are allowed.")
    with connect() as con:
        return pd.read_sql_query(sql, con)
