import sqlite3
import json
import os
from datetime import datetime


def lookup_product_by_hash(
    qr_hash,
    serial_db_path="Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration/back_end/database/serials_hashes.db",
    product_info_db_path="Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration/back_end/database/info_db/info.db",
    output_folder="Technology_Driven_Detection_and_Prevention_of_Medicine_Adulteration/back_end/output_json"
):
    """
    1. Search first DB using hash → get serial
    2. Search second DB using serial → get full product info
    3. Save result as JSON
    4. Return product data (dict) or None
    """

    conn1 = sqlite3.connect(serial_db_path)
    cursor1 = conn1.cursor()

    cursor1.execute(
        "SELECT serial FROM products WHERE hash = ?",
        (qr_hash,)
    )

    result1 = cursor1.fetchone()
    conn1.close()

    if not result1:
        return None

    serial_no = result1[0]

    conn2 = sqlite3.connect(product_info_db_path)
    cursor2 = conn2.cursor()

    cursor2.execute(
        """
        SELECT serial, batch_no, date_expire,
               date_manufacture, colour,
               manufactured_by, manufacturing_license_no
        FROM product_info
        WHERE serial = ?
        """,
        (serial_no,)
    )

    result2 = cursor2.fetchone()
    conn2.close()

    if not result2:
        return None



    product_data = {
        "serial": result2[0],
        "batch_no": result2[1],
        "date_expire": result2[2],
        "date_manufacturing": result2[3],
        "colour": result2[4],
        "manufactured_by": result2[5],
        "manufacturing_license_no": result2[6],
    }

    os.makedirs(output_folder, exist_ok=True)

    filename = f"{output_folder}/{serial_no}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(product_data, f, indent=4)

    return product_data
