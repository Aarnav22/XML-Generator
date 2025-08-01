# import sqlite3

# conn = sqlite3.connect("insurance.db")
# cursor = conn.cursor()

# # 1. group_coverage
# cursor.execute("""
# INSERT INTO group_coverage (
#     personid, proposalnumber, coverage_status, coveragestartdate,
#     coveragesumassured, customerfirstname, customermiddlename,
#     customerlastname, customerdob, customergender,
#     correspondenceaddress1, correspondenceaddress2, correspondenceaddress3,
#     correspondencecity, correspondencestate, correspondencepostcode,
#     permanentaddress1, permanentaddress2, permanentaddress3,
#     permanentcity, permanentstate, permanentpostcode,
#     proposaldate, dateofdeath, uin
# ) VALUES (
#     'P080', 'PROP080', 'Death Claim Intimated', '2023-01-01',
#     500000, 'Alice', 'M', 'Wonderland', '1990-06-15', 'F',
#     'Street 1', 'Block A', '', 'DreamCity', 'StateDream', '111111',
#     'Perm Street', 'Perm Block', '', 'PermCity', 'PermState', '222222',
#     '2023-01-01', '2024-12-25', '111ABC999'
# )
# """)

# # 2. group_contactmaster
# cursor.execute("""
# INSERT INTO group_contactmaster (personid, contact_mobile, emailid)
# VALUES ('P080', '9123456780', 'alice@example.com')
# """)

# # 3. death_claim_intimation
# cursor.execute("""
# INSERT INTO death_claim_intimation (la_id, incident_reason, sub_cause_of_death)
# VALUES ('P080', 'Accident', 'Car crash')
# """)

# # 4. person_info
# cursor.execute("""
# INSERT INTO person_info (pr_person_id, pr_pan, gp_annual_inc)
# VALUES ('P080', 'XYZAB1234C', '1000000')
# """)

# # 5. iib_portal_upload_test
# cursor.execute("""
# INSERT INTO iib_portal_upload_test (policy_proposal_no, uploaded_by)
# VALUES ('P080', 'user_1720592391540')
# """)

# conn.commit()
# conn.close()

# print("✅ Clean test record for P080 inserted.")

import sqlite3

conn = sqlite3.connect("insurance.db")
cursor = conn.cursor()

records = [
    {
        "personid": "P081", "name": ("Bob", "K", "Builder"), "dob": "1985-05-20", "gender": "M",
        "mobile": "9123456781", "email": "bob@example.com", "pan": "ABCPB1234L", "income": "850000"
    },
    {
        "personid": "P082", "name": ("Carol", "", "Smith"), "dob": "1992-02-14", "gender": "F",
        "mobile": "9123456782", "email": "carol@example.com", "pan": "QWERT5678U", "income": "920000"
    },
    {
        "personid": "P083", "name": ("David", "J", "Lee"), "dob": "1980-12-01", "gender": "M",
        "mobile": "9123456783", "email": "david@example.com", "pan": "ZXCVB6789M", "income": "780000"
    },
    {
        "personid": "P084", "name": ("Eva", "A", "Jones"), "dob": "1975-07-30", "gender": "F",
        "mobile": "9123456784", "email": "eva@example.com", "pan": "PLMKO8765X", "income": "860000"
    },
    {
        "personid": "P085", "name": ("Frank", "", "Ocean"), "dob": "1990-03-25", "gender": "M",
        "mobile": "9123456785", "email": "frank@example.com", "pan": "ASDFG3456R", "income": "990000"
    },
    {
        "personid": "P086", "name": ("Grace", "", "Kim"), "dob": "1988-11-11", "gender": "F",
        "mobile": "9123456786", "email": "grace@example.com", "pan": "TYUIO2345P", "income": "870000"
    },
    {
        "personid": "P087", "name": ("Henry", "", "Ford"), "dob": "1970-08-19", "gender": "M",
        "mobile": "9123456787", "email": "henry@example.com", "pan": "BNMVF9876Q", "income": "1020000"
    },
    {
        "personid": "P088", "name": ("Irene", "C", "Wong"), "dob": "1983-10-10", "gender": "F",
        "mobile": "9123456788", "email": "irene@example.com", "pan": "LKJHG1234T", "income": "940000"
    },
    {
        "personid": "P089", "name": ("Jack", "L", "Black"), "dob": "1981-09-05", "gender": "M",
        "mobile": "9123456789", "email": "jack@example.com", "pan": "MNBVC2345E", "income": "910000"
    },
    {
        "personid": "P090", "name": ("Kara", "M", "Danvers"), "dob": "1993-04-22", "gender": "F",
        "mobile": "9123456790", "email": "kara@example.com", "pan": "WSXED3456Z", "income": "880000"
    }
]

uploaded_by = "user_1720592391540"

for r in records:
    cursor.execute("""
        INSERT INTO group_coverage (
            personid, proposalnumber, coverage_status, coveragestartdate,
            coveragesumassured, customerfirstname, customermiddlename,
            customerlastname, customerdob, customergender,
            correspondenceaddress1, correspondenceaddress2, correspondenceaddress3,
            correspondencecity, correspondencestate, correspondencepostcode,
            permanentaddress1, permanentaddress2, permanentaddress3,
            permanentcity, permanentstate, permanentpostcode,
            proposaldate, dateofdeath, uin
        ) VALUES (?, ?, 'Death Claim Intimated', '2023-01-01',
                  600000, ?, ?, ?, ?, ?,
                  'Street A', 'Block X', '', 'TestCity', 'TestState', '123456',
                  'Perm A', 'Perm B', '', 'PermCity', 'PermState', '654321',
                  '2023-01-01', '2024-12-31', '111ABC999')
    """, (
        r["personid"], f"PROP{r['personid'][1:]}", r["name"][0], r["name"][1], r["name"][2], r["dob"], r["gender"]
    ))

    cursor.execute("""
        INSERT INTO group_contactmaster (personid, contact_mobile, emailid)
        VALUES (?, ?, ?)
    """, (r["personid"], r["mobile"], r["email"]))

    cursor.execute("""
        INSERT INTO death_claim_intimation (la_id, incident_reason, sub_cause_of_death)
        VALUES (?, 'Accident', 'PP')
    """, (r["personid"],))

    cursor.execute("""
        INSERT INTO person_info (pr_person_id, pr_pan, gp_annual_inc)
        VALUES (?, ?, ?)
    """, (r["personid"], r["pan"], r["income"]))

    cursor.execute("""
        INSERT INTO iib_portal_upload_test (policy_proposal_no, uploaded_by)
        VALUES (?, ?)
    """, (r["personid"], uploaded_by))

conn.commit()
conn.close()

print("✅ Inserted 10 clean group test records.")
