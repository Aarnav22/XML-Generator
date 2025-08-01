import os
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime

def export_to_xml(table_name, emp_id):
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "insurance.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch data
    cursor.execute(f"SELECT * FROM {table_name} WHERE uploaded_by = ?", (emp_id,))
    rows = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Build XML
    root = ET.Element(table_name)
    for row in rows:
        record_elem = ET.SubElement(root, "record")
        for col_name, value in zip(column_names, row):
            col_elem = ET.SubElement(record_elem, col_name)
            col_elem.text = str(value) if value is not None else ""

    # Prepare output folder
    os.makedirs("output", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    xml_file = os.path.join("output", f"{emp_id}_{table_name}_{timestamp}.xml")

    # Write XML
    tree = ET.ElementTree(root)
    tree.write(xml_file, encoding="utf-8", xml_declaration=True)

    conn.close()
    print(f"✅ XML exported: {xml_file}")
