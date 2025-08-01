import sqlite3

# Connects to a new database (creates it if it doesn't exist)
conn = sqlite3.connect("insurance.db")

cursor = conn.cursor()
#group_coverage dataset
cursor.execute('''
CREATE TABLE IF NOT EXISTS group_coverage (
    personid TEXT,
    proposalnumber TEXT,
    coverage_status TEXT,
    coveragestartdate TEXT,
    proposaldate TEXT,
    coveragesumassured REAL,
    customerfirstname TEXT,
    customermiddlename TEXT,
    customerlastname TEXT,
    customerdob TEXT,
    customergender TEXT,
    correspondenceaddress1 TEXT,
    correspondenceaddress2 TEXT,
    correspondenceaddress3 TEXT,
    correspondencecity TEXT,
    correspondencestate TEXT,
    correspondencepostcode TEXT,
    permanentaddress1 TEXT,
    permanentaddress2 TEXT,
    permanentaddress3 TEXT,
    permanentcity TEXT,
    permanentstate TEXT,
    permanentpostcode TEXT,
    pannumber TEXT,
    uin TEXT,
    productnumber TEXT,
    policy_number TEXT,
    dateofdeath TEXT
)
''')
#group_contactmaster dataset
cursor.execute('''
CREATE TABLE IF NOT EXISTS group_contactmaster (
    personid TEXT,
    contact_mobile TEXT,
    emailid TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS iib_portal_upload_test (
    policy_proposal_no TEXT,
    uploaded_by TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_product (
    product_number TEXT,
    uin TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS death_claim_intimation (
    la_id TEXT,
    incident_reason TEXT,
    sub_cause_of_death TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS person_info (
    pr_person_id TEXT,
    pr_pan TEXT,
    pr_pan_num TEXT,
    gp_annual_inc REAL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS iib_mapping (
    type TEXT,
    iib_values TEXT,
    mis_values TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS iib_qq_clean_data_grp (
    policy_number TEXT,
    proposalnumber TEXT,
    query_type TEXT,
    dop_doc TEXT,
    sum_assured REAL,
    la_first_name TEXT,
    la_middle_name TEXT,
    la_last_name TEXT,
    la_dob TEXT,
    la_gender TEXT,
    la_current_address TEXT,
    la_permanent_address TEXT,
    la_pin_code TEXT,
    la_pan TEXT,
    la_aadhar TEXT,
    la_ckyc TEXT,
    la_passport TEXT,
    la_dl TEXT,
    la_voter_id TEXT,
    la_phone_number_1 TEXT,
    la_phone_number_2 TEXT,
    la_email_1 TEXT,
    la_email_2 TEXT,
    date_of_death TEXT,
    company_number TEXT,
    product_type TEXT,
    product_uin TEXT,
    annual_income TEXT,
    cause_of_death TEXT,
    extraction_date TEXT,
    uploaded_by TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS iib_qq_bad_data_grp (
    policy_number TEXT,
    proposalnumber TEXT,
    query_type TEXT,
    dop_doc TEXT,
    sum_assured REAL,
    la_first_name TEXT,
    la_middle_name TEXT,
    la_last_name TEXT,
    la_dob TEXT,
    la_gender TEXT,
    la_current_address TEXT,
    la_permanent_address TEXT,
    la_pin_code TEXT,
    la_pan TEXT,
    la_aadhar TEXT,
    la_ckyc TEXT,
    la_passport TEXT,
    la_dl TEXT,
    la_voter_id TEXT,
    la_phone_number_1 TEXT,
    la_phone_number_2 TEXT,
    la_email_1 TEXT,
    la_email_2 TEXT,
    date_of_death TEXT,
    company_number TEXT,
    product_type TEXT,
    product_uin TEXT,
    annual_income TEXT,
    cause_of_death TEXT,
    extraction_date TEXT,
    uploaded_by TEXT,
    remark TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS individual_coverage (
    personid TEXT,
    proposalnumber TEXT,
    policy_number TEXT,
    coverage_status TEXT,
    coveragestartdate TEXT,
    proposaldate TEXT,
    coveragesumassured REAL,
    customerfirstname TEXT,
    customermiddlename TEXT,
    customerlastname TEXT,
    customerdob TEXT,
    customergender TEXT,
    pannumber TEXT,
    uin TEXT,
    productnumber TEXT,
    dateofdeath TEXT,
    applicationnumber TEXT,
    aadharno TEXT,
    ckyc TEXT,
    passport TEXT,
    drivinglicense TEXT,
    voterid TEXT,
    permanentaddress1 TEXT,
    permanentaddress2 TEXT,
    permanentaddress3 TEXT,
    permanentcity TEXT,
    permanentstate TEXT,
    permanentpostcode TEXT,
    correspondenceaddress1 TEXT,
    correspondenceaddress2 TEXT,
    correspondenceaddress3 TEXT,
    correspondencecity TEXT,
    correspondencestate TEXT,
    correspondencepostcode TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS individual_contactmaster (
    personid TEXT,
    contact_mobile TEXT,
    emailid TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS iib_qq_clean_data_indv (
    policy_number TEXT,
    proposalnumber TEXT,
    query_type TEXT,
    dop_doc TEXT,
    sum_assured REAL,
    la_first_name TEXT,
    la_middle_name TEXT,
    la_last_name TEXT,
    la_dob TEXT,
    la_gender TEXT,
    la_current_address TEXT,
    la_permanent_address TEXT,
    la_pin_code TEXT,
    la_pan TEXT,
    la_aadhar TEXT,
    la_ckyc TEXT,
    la_passport TEXT,
    la_dl TEXT,
    la_voter_id TEXT,
    la_phone_number_1 TEXT,
    la_phone_number_2 TEXT,
    la_email_1 TEXT,
    la_email_2 TEXT,
    date_of_death TEXT,
    company_number TEXT,
    product_type TEXT,
    product_uin TEXT,
    annual_income TEXT,
    cause_of_death TEXT,
    extraction_date TEXT,
    uploaded_by TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS iib_qq_bad_data_indv (
    policy_number TEXT,
    proposalnumber TEXT,
    query_type TEXT,
    dop_doc TEXT,
    sum_assured REAL,
    la_first_name TEXT,
    la_middle_name TEXT,
    la_last_name TEXT,
    la_dob TEXT,
    la_gender TEXT,
    la_current_address TEXT,
    la_permanent_address TEXT,
    la_pin_code TEXT,
    la_pan TEXT,
    la_aadhar TEXT,
    la_ckyc TEXT,
    la_passport TEXT,
    la_dl TEXT,
    la_voter_id TEXT,
    la_phone_number_1 TEXT,
    la_phone_number_2 TEXT,
    la_email_1 TEXT,
    la_email_2 TEXT,
    date_of_death TEXT,
    company_number TEXT,
    product_type TEXT,
    product_uin TEXT,
    annual_income TEXT,
    cause_of_death TEXT,
    extraction_date TEXT,
    uploaded_by TEXT,
    remark TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS temp_contract_input (
    policy_number TEXT,
    uploaded_by TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS iib_portal_temp_contract_clean (
    policy_number TEXT,
    la_name TEXT,
    pan_number TEXT,
    dob TEXT,
    uploaded_by TEXT
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS iib_portal_temp_contract_bad (
    policy_number TEXT,
    la_name TEXT,
    pan_number TEXT,
    dob TEXT,
    uploaded_by TEXT,
    remark TEXT
)
''')
conn.commit()
conn.close()


