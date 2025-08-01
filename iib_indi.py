import sqlite3
import os
import pandas as pd
from datetime import datetime

def get_column_names(cursor, table):
    cursor.execute(f"PRAGMA table_info({table})")
    return [row[1] for row in cursor.fetchall()]

def insert_invalid_rows(cursor, condition_sql, remark, emp_id, params=()):
    columns = get_column_names(cursor, 'iib_qq_clean_data_indv')
    column_list = ", ".join(columns)
    cursor.execute(f"""
        INSERT INTO iib_qq_bad_data_indv ({column_list}, remark)
        SELECT *, ? FROM iib_qq_clean_data_indv
        WHERE {condition_sql} AND uploaded_by = ?
    """, (*params, remark, emp_id))
    cursor.execute(f"DELETE FROM iib_qq_clean_data_indv WHERE {condition_sql} AND uploaded_by = ?", (*params, emp_id))

def cleanse_indv_data(emp_id):
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "insurance.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Step 0: Cleanup any previous data for user
    cursor.execute("DELETE FROM iib_qq_clean_data_indv WHERE uploaded_by = ?", (emp_id,))
    cursor.execute("DELETE FROM iib_qq_bad_data_indv WHERE uploaded_by = ?", (emp_id,))
    conn.commit()

    # Step 1: Insert clean data
    cursor.execute("""
        INSERT INTO iib_qq_clean_data_indv (
            policy_number, proposalnumber, query_type, dop_doc, sum_assured,
            la_first_name, la_middle_name, la_last_name, la_dob, la_gender,
            la_current_address, la_permanent_address, la_pin_code, la_pan,
            la_aadhar, la_ckyc, la_passport, la_dl, la_voter_id,
            la_phone_number_1, la_phone_number_2, la_email_1, la_email_2,
            date_of_death, company_number, product_type, product_uin,
            annual_income, cause_of_death, extraction_date, uploaded_by
        )
        SELECT
            ic.policy_number,
            ic.proposalnumber,
            CASE 
                WHEN ic.coverage_status IN (
                    'Death Claim', 'Inactive', 'Death claim',
                    'Death Claim Paid', 'Death Claim Repudiated'
                ) THEN '2' ELSE '1' END,
            COALESCE(ic.coveragestartdate, ic.proposaldate),
            COALESCE(ic.coveragesumassured, 0),
            TRIM(ic.customerfirstname),
            TRIM(ic.customermiddlename),
            TRIM(ic.customerlastname),
            ic.customerdob,
            CASE
                WHEN ic.customergender IN ('Male', 'M', 'm') THEN 'M'
                WHEN ic.customergender IN ('Female', 'F', 'f') THEN 'F'
                WHEN ic.customergender = 'T' THEN 'T'
                ELSE ic.customergender
            END,
            TRIM(ic.correspondenceaddress1 || ' ' || ic.correspondenceaddress2 || ' ' || ic.correspondenceaddress3),
            TRIM(ic.permanentaddress1 || ' ' || ic.permanentaddress2 || ' ' || ic.permanentaddress3),
            ic.permanentpostcode,
            COALESCE(ic.pannumber, pi.pr_pan_num),
            ic.aadharno,
            ic.ckyc,
            ic.passport,
            ic.drivinglicense,
            ic.voterid,
            cm.contact_mobile,
            NULL,
            cm.emailid,
            NULL,
            ic.dateofdeath,
            '111',
            dp.product_number,
            dp.uin,
            pi.gp_annual_inc,
            COALESCE(dc.sub_cause_of_death, 'PP'),
            DATE('now'),
            ?
        FROM iib_portal_upload_test u
        JOIN individual_coverage ic ON ic.policy_number = u.policy_proposal_no OR ic.proposalnumber = u.policy_proposal_no
        LEFT JOIN individual_contactmaster cm ON cm.personid = ic.personid
        LEFT JOIN person_info pi ON pi.pr_person_id = ic.personid
        LEFT JOIN death_claim_intimation dc ON dc.la_id = ic.personid
        LEFT JOIN dim_product dp ON dp.product_number = ic.productnumber
        WHERE u.uploaded_by = ?
    """, (emp_id, emp_id))
    conn.commit()

    

    # Step 2: Mandatory Field Validations
    validations = [
        ("query_type IS NULL OR query_type NOT IN ('1','2')", "Invalid QUERY_TYPE"),
        ("dop_doc IS NULL", "DOP_DOC is NULL"),
        ("sum_assured IS NULL", "SUM_ASSURED is NULL"),
        ("la_first_name IS NULL OR LENGTH(la_first_name) > 75 OR la_first_name = ' '", "Invalid LA_FIRST_NAME"),
        ("la_dob IS NULL", "LA_DOB is NULL"),
        ("la_gender IS NULL OR la_gender NOT IN ('M','F','T','I')", "Invalid LA_GENDER"),
        ("query_type = '2' AND date_of_death IS NULL", "DATE_OF_DEATH required for DEATH CASE"),
        ("query_type = '2' AND (cause_of_death IS NULL OR cause_of_death = '')", "CAUSE_OF_DEATH required for DEATH CASE"),
        ("annual_income IS NULL OR LENGTH(annual_income) < 4 OR LENGTH(annual_income) > 15", "Invalid ANNUAL_INCOME"),
        ("company_number IS NULL", "COMPANY_NUMBER is NULL"),
        ("product_type IS NULL", "PRODUCT_TYPE is NULL"),
        ("product_uin IS NULL OR SUBSTR(product_uin, 1, 3) <> '111'", "Invalid PRODUCT_UIN")
    ]
    for condition, remark in validations:
        insert_invalid_rows(cursor, condition, remark, emp_id)

    # Step 2.5: Mapping Validations
    valid_cod = ['PP', 'A1', 'B2']
    insert_invalid_rows(
        cursor,
        f"cause_of_death NOT IN ({','.join(['?'] * len(valid_cod))})",
        "Invalid CAUSE_OF_DEATH (not in mapping)",
        emp_id,
        valid_cod
    )
    valid_product_types = ['TERM', 'ULIP', 'ENDOW']
    insert_invalid_rows(
        cursor,
        f"product_type NOT IN ({','.join(['?'] * len(valid_product_types))})",
        "Invalid PRODUCT_TYPE (not in mapping)",
        emp_id,
        valid_product_types
    )

    # Step 3: Clean optional fields
    cleanup_rules = [
        ("la_middle_name", "length(la_middle_name) > 25 OR la_middle_name = ' '"),
        ("la_last_name", "length(la_last_name) > 75 OR la_last_name = ' '"),
        ("la_current_address", "length(la_current_address) > 500"),
        ("la_permanent_address", "length(la_permanent_address) > 500"),
        ("la_pin_code", "length(la_pin_code) != 6"),
        ("la_pan", "NOT UPPER(la_pan) GLOB '[A-Z][A-Z][A-Z][A-Z][A-Z][0-9][0-9][0-9][0-9][A-Z]'"),
        ("la_ckyc", "length(la_ckyc) != 14"),
        ("la_passport", "length(la_passport) != 8"),
        ("la_dl", "length(la_dl) < 5"),
        ("la_voter_id", "length(la_voter_id) < 5"),
        ("la_phone_number_1", "NOT la_phone_number_1 GLOB '[6-9][0-9]{9}'"),
        ("la_email_1", "NOT la_email_1 GLOB '*@*.*'"),
        ("la_email_2", "NOT la_email_2 GLOB '*@*.*'")
    ]
    for column, condition in cleanup_rules:
        cursor.execute(f"""
            UPDATE iib_qq_clean_data_indv 
            SET {column} = NULL 
            WHERE {condition} AND uploaded_by = ?
        """, (emp_id,))

    # Step 4: Remove death details for non-death cases
    cursor.execute("""
        UPDATE iib_qq_clean_data_indv 
        SET date_of_death = NULL, cause_of_death = NULL 
        WHERE query_type = '1' AND uploaded_by = ?
    """, (emp_id,))
    conn.commit()

   # STEP 5: Export clean and bad data to Excel
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Make sure the output directory exists
    os.makedirs("output", exist_ok=True)

    clean_df = pd.read_sql_query("SELECT * FROM iib_qq_clean_data_indv WHERE uploaded_by = ?", conn, params=(emp_id,))
    bad_df = pd.read_sql_query("SELECT * FROM iib_qq_bad_data_indv WHERE uploaded_by = ?", conn, params=(emp_id,))

    clean_file = f"output/{emp_id}_clean_indv_{timestamp}.xlsx"
    bad_file = f"output/{emp_id}_bad_indv_{timestamp}.xlsx"

    clean_df.to_excel(clean_file, index=False)
    bad_df.to_excel(bad_file, index=False)

    # Step 6: Cleanup temp tables
    cursor.execute("DELETE FROM iib_qq_clean_data_indv WHERE uploaded_by = ?", (emp_id,))
    cursor.execute("DELETE FROM iib_qq_bad_data_indv WHERE uploaded_by = ?", (emp_id,))
    conn.commit()
    conn.close()

    from utils import export_to_xml
    export_to_xml('iib_qq_clean_data_indv', emp_id)

    return f"✅ Individual data processed and exported for employee: {emp_id}"
