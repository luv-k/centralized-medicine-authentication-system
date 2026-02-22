import sqlite3
import os


def store_product_info(records,
                       batch_no,
                       date_expire,
                       date_manufacture,
                       colour,
                       manufactured_by,
                       license_no,
                       info_db="Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration\\back_end\\database\\info_db\\info.db"):

    os.makedirs(os.path.dirname(info_db), exist_ok=True)

    conn = sqlite3.connect(info_db)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial TEXT UNIQUE NOT NULL,
            batch_no TEXT NOT NULL,
            date_expire TEXT NOT NULL,
            date_manufacture TEXT NOT NULL,
            colour TEXT,
            manufactured_by TEXT,
            manufacturing_license_no TEXT
        )
    """)

    for record in records:
        serial = record["serial"]

        cursor.execute("""
            INSERT INTO product_info (
                serial,
                batch_no,
                date_expire,
                date_manufacture,
                colour,
                manufactured_by,
                manufacturing_license_no
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            serial,
            batch_no,
            date_expire,
            date_manufacture,
            colour,
            manufactured_by,
            license_no
        ))

    conn.commit()
    conn.close()
