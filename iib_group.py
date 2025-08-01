import sqlite3
from datetime import datetime

def get_column_names(cursor, table):
    cursor.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cursor.fetchall()]

def insert_invalid_rows(cursor, condition_sql, remark, emp_id):
    columns = get_column_names(cursor, 'iib_qq_clean_data_grp')
    column_list = ', '.join(columns)
    cursor.execute(f"""
        INSERT INTO iib_qq_bad_data_grp ({column_list}, remark)
        SELECT *, ? FROM iib_qq_clean_data_grp
        WHERE {condition_sql} AND uploaded_by = ?
    """, (remark, emp_id))
    cursor.execute(f"DELETE FROM iib_qq_clean_data_grp WHERE {condition_sql} AND uploaded_by = ?", (emp_id,))

def cleanse_grp_data(emp_id):
    conn = sqlite3.connect('insurance.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM iib_qq_clean_data_grp WHERE uploaded_by = ?", (emp_id,))
    conn.commit()

    cursor.execute("""
        INSERT INTO iib_qq_clean_data_grp (
            policy_number, proposalnumber, query_type, dop_doc, sum_assured,
            la_first_name, la_middle_name, la_last_name, la_dob, la_gender,
            la_current_address, la_permanent_address, la_pin_code, la_pan,
            la_aadhar, la_ckyc, la_passport, la_dl, la_voter_id,
            la_phone_number_1, la_phone_number_2, la_email_1, la_email_2,
            date_of_death, company_number, product_type, product_uin,
            annual_income, cause_of_death, extraction_date, uploaded_by
        )
        SELECT
            gc.personid, gc.proposalnumber,
            CASE WHEN gc.coverage_status IN (
                'Death Claim', 'Death Claim Intimated', 'Death claim',
                'Death Claim Paid', 'Death Claim Repudiated',
                'Joint Borrower Death Claim Intimated') THEN '2' ELSE '1' END,
            COALESCE(gc.coveragestartdate, gc.proposaldate),
            COALESCE(gc.coveragesumassured, 0),
            gc.customerfirstname, gc.customermiddlename, gc.customerlastname,
            gc.customerdob,
            CASE
                WHEN gc.customergender IN ('M', 'Male', 'm') THEN 'M'
                WHEN gc.customergender IN ('F', 'Female', 'f') THEN 'F'
                WHEN gc.customergender = 'T' THEN 'T'
                ELSE gc.customergender
            END,
            gc.correspondenceaddress1 || gc.correspondenceaddress2 || gc.correspondenceaddress3 || gc.correspondencecity || gc.correspondencestate || gc.correspondencepostcode,
            gc.permanentaddress1 || gc.permanentaddress2 || gc.permanentaddress3 || gc.permanentcity || gc.permanentstate || gc.permanentpostcode,
            gc.correspondencepostcode,
            pi.pr_pan,
            NULL, NULL, NULL, NULL, NULL,
            gcm.contact_mobile, NULL,
            CASE WHEN instr(trim(gcm.emailid), '@') = 0 THEN NULL ELSE lower(trim(gcm.emailid)) END,
            NULL,
            gc.dateofdeath,
            '111',
            'OT',
            gc.uin,
            CAST(pi.gp_annual_inc AS TEXT),
            di.incident_reason || '-' || IFNULL(di.sub_cause_of_death, ''),
            CURRENT_DATE,
            ?
        FROM group_coverage gc
        LEFT JOIN group_contactmaster gcm ON gc.personid = gcm.personid
        LEFT JOIN death_claim_intimation di ON gc.personid = di.la_id
        LEFT JOIN person_info pi ON gc.personid = pi.pr_person_id
        INNER JOIN iib_portal_upload_test u
        ON TRIM(LOWER(u.policy_proposal_no)) = TRIM(LOWER(gc.personid))
        AND u.uploaded_by = ?    """, (emp_id, emp_id))
    conn.commit()

    validations = [
        ("query_type IS NULL OR query_type NOT IN ('1', '2')", "Invalid QUERY_TYPE"),
        ("dop_doc IS NULL", "DoP_DoC IS NULL"),
        ("sum_assured IS NULL", "SUM_ASSURED IS NULL"),
        ("la_first_name IS NULL OR LENGTH(la_first_name) > 75 OR la_first_name = ' '", "Invalid LA_FIRST_NAME"),
        ("la_dob IS NULL", "LA_DoB IS NULL"),
        ("la_gender IS NULL OR la_gender NOT IN ('M', 'F', 'T', 'I')", "Invalid LA_GENDER"),
        ("query_type = '2' AND (date_of_death IS NULL)", "Missing DATE_OF_DEATH"),
        ("annual_income IS NULL OR LENGTH(annual_income) < 4 OR LENGTH(annual_income) > 15", "Invalid ANNUAL_INCOME"),
        ("query_type = '2' AND (cause_of_death IS NULL OR cause_of_death = '')", "Missing CAUSE_OF_DEATH"),
        ("company_number IS NULL", "Missing COMPANY_NUMBER"),
        ("product_type IS NULL", "Missing PRODUCT_TYPE"),
        ("product_uin IS NULL OR SUBSTR(product_uin, 1, 3) != '111'", "Invalid PRODUCT_UIN"),
    ]

    for condition, remark in validations:
        insert_invalid_rows(cursor, condition, remark, emp_id)

    conn.commit()
    conn.close()

    from utils import export_to_xml
    export_to_xml('iib_qq_clean_data_grp', emp_id)
    return f"✅ Group data cleansed for employee: {emp_id}"
