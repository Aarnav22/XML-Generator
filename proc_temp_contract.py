import sqlite3
from datetime import datetime

def process_temp_contract(db_path, v_string, intProPol, bTruncate, v_emp_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    v_date = datetime.now().strftime('%Y-%m-%d')

    # Optional deletion step
    if bTruncate == 'D':
        cursor.execute('DELETE FROM iib_portal_upload_test WHERE uploaded_by = ?', (v_emp_id,))
        conn.commit()

    # Split and insert
    lv_appendstring = v_string + '/'
    entries = lv_appendstring.split('/')[:-1]
    for entry in entries:
        entry = entry.strip()
        if intProPol == 1 and len(entry) == 10:
            entry = '0' + entry
        cursor.execute('''
            INSERT INTO iib_portal_upload_test (policy_proposal_no, uploaded_by, upload_date)
            VALUES (?, ?, ?)
        ''', (entry, v_emp_id, v_date))
    conn.commit()

    # Matching logic
    if intProPol == 0:
        cursor.execute('''
            SELECT COUNT(*) FROM (
                SELECT a.policy_proposal_no AS prn, b.proposalnumber AS poli
                FROM iib_portal_upload_test a
                JOIN individual_coverage b ON a.policy_proposal_no = b.proposalnumber
                WHERE a.uploaded_by = ?
            )
        ''', (v_emp_id,))
        match_cnt = cursor.fetchone()[0]

    elif intProPol == 1:
        cursor.execute('''
            SELECT COUNT(*) FROM (
                SELECT a.policy_proposal_no AS prn, b.policynumber AS poli
                FROM iib_portal_upload_test a
                JOIN individual_coverage b ON a.policy_proposal_no = b.policynumber
                WHERE a.uploaded_by = ?
            )
        ''', (v_emp_id,))
        match_cnt = cursor.fetchone()[0]

    elif intProPol == 2:
        cursor.execute('''
            SELECT COUNT(*) FROM (
                SELECT a.policy_proposal_no AS prn, b.personid AS poli
                FROM iib_portal_upload_test a
                JOIN group_coverage b ON a.policy_proposal_no = b.personid
                WHERE a.uploaded_by = ?
            )
        ''', (v_emp_id,))
        match_cnt = cursor.fetchone()[0]

    # Count total uploaded rows
    cursor.execute('SELECT COUNT(*) FROM iib_portal_upload_test WHERE uploaded_by = ?', (v_emp_id,))
    main_cnt = cursor.fetchone()[0]

    conn.close()
    return match_cnt, main_cnt
