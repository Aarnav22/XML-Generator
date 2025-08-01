import sqlite3
import pandas as pd
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree

def convert_to_xml(dataframe, root_tag='Records', row_tag='Record'):
    root = Element(root_tag)

    for _, row in dataframe.iterrows():
        record = SubElement(root, row_tag)
        for col in dataframe.columns:
            value = str(row[col]) if pd.notnull(row[col]) else ''
            child = SubElement(record, col)
            child.text = value

    return ElementTree(root)

def export_clean_data_to_xml(db_path='insurance.db', emp_id='emp123', data_type='individual', output_path='output.xml'):
    table = 'iib_qq_clean_data_indv' if data_type == 'individual' else 'iib_qq_clean_data_grp'

    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table} WHERE uploaded_by = ?"
    df = pd.read_sql_query(query, conn, params=(emp_id,))
    conn.close()

    tree = convert_to_xml(df)
    tree.write(output_path, encoding='utf-8', xml_declaration=True)
    return output_path
