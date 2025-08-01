from flask import Flask, request, render_template, redirect
import sqlite3
import pandas as pd
import os
from iib_indi import cleanse_indv_data
from iib_group import cleanse_grp_data
import xml.etree.ElementTree as ET
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

status_dict = {}  # In-memory processing tracker


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start-process', methods=['POST'])
def start_process():
    file = request.files['excel']
    data_type = request.form['data_type']
    emp_id = request.form['employee_id']

    file_path = os.path.join(UPLOAD_FOLDER, f"{emp_id}.xlsx")
    file.save(file_path)

    try:
        df = pd.read_excel(file_path)

        if 'policy_proposal_no' not in df.columns:
            raise ValueError("Excel must contain a column named 'policy_proposal_no'.")

        conn = sqlite3.connect("insurance.db")
        cursor = conn.cursor()

        # Delete any previously uploaded data for this user
        cursor.execute("DELETE FROM iib_portal_upload_test WHERE uploaded_by = ?", (emp_id,))

        # Insert new rows from Excel
        for _, row in df.iterrows():
            value = str(row['policy_proposal_no']).strip()
            cursor.execute(
            "INSERT INTO iib_portal_upload_test (policy_proposal_no, uploaded_by) VALUES (?, ?)",
            (value, emp_id)
             )


        conn.commit()
        conn.close()

        status_dict[emp_id] = "processing"

        # Trigger cleansing
        if data_type == "individual":
            cleanse_indv_data(emp_id)
        else:
            cleanse_grp_data(emp_id)

        status_dict[emp_id] = "done"

    except Exception as e:
        print(f"❌ Error during processing for {emp_id}: {str(e)}")
        status_dict[emp_id] = "error"

    return '', 204


@app.route('/check-status/<emp_id>')
def check_status(emp_id):
    return status_dict.get(emp_id, "processing")

@app.route('/results')
def results():
    emp_id = request.args.get("emp_id")
    dtype = request.args.get("dtype")

    conn = sqlite3.connect("insurance.db")
    cursor = conn.cursor()

    if dtype == "individual":
        cursor.execute("SELECT COUNT(*) FROM iib_qq_clean_data_indv WHERE uploaded_by = ?", (emp_id,))
        clean = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM iib_qq_bad_data_indv WHERE uploaded_by = ?", (emp_id,))
        bad = cursor.fetchone()[0]
    else:
        cursor.execute("SELECT COUNT(*) FROM iib_qq_clean_data_grp WHERE uploaded_by = ?", (emp_id,))
        clean = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM iib_qq_bad_data_grp WHERE uploaded_by = ?", (emp_id,))
        bad = cursor.fetchone()[0]

    conn.close()

    return render_template("results.html", clean=clean, bad=bad, emp_id=emp_id, dtype=dtype)


if __name__ == '__main__':
    app.run(debug=True)
