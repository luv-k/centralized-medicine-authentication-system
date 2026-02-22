import uuid
import hashlib
import hmac
import sqlite3
import json
import os
from datetime import datetime


def generate_batch(count: int, secret: str,
                   primary_db="Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration\\managment_side\\database_serials_hashing\\serials_hashes.db",
                   backend_db="Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration\\back_end\\database\\serials_hashes.db",
                   json_path="Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration\\managment_side\\database_serials_hashing\\serials_hashes.json"):

    # Create folders
    os.makedirs(os.path.dirname(primary_db), exist_ok=True)
    os.makedirs(os.path.dirname(backend_db), exist_ok=True)

    # Connect to both databases
    conn_primary = sqlite3.connect(primary_db)
    cursor_primary = conn_primary.cursor()

    conn_backup = sqlite3.connect(backend_db)
    cursor_backup = conn_backup.cursor()

    # Create tables in both
    for cursor in (cursor_primary, cursor_backup):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial TEXT UNIQUE NOT NULL,
                hash TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

    conn_primary.commit()
    conn_backup.commit()

    records = []

    for _ in range(count):
        serial = str(uuid.uuid4())

        hash_value = hmac.new(
            secret.encode(),
            serial.encode(),
            hashlib.sha256
        ).hexdigest()

        timestamp = datetime.utcnow().isoformat()

        # Insert into BOTH databases
        cursor_primary.execute("""
            INSERT INTO products (serial, hash, created_at)
            VALUES (?, ?, ?)
        """, (serial, hash_value, timestamp))

        cursor_backup.execute("""
            INSERT INTO products (serial, hash, created_at)
            VALUES (?, ?, ?)
        """, (serial, hash_value, timestamp))

        records.append({
            "serial": serial,
            "hash": hash_value
        })

    conn_primary.commit()
    conn_backup.commit()

    conn_primary.close()
    conn_backup.close()

    # JSON overwritten (current batch only)
    with open(json_path, "w") as f:
        json.dump(records, f, indent=2)

    return records
