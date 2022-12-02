import sqlite3

# conn = None
# c = None

def db_connection():
    try:
        conn = sqlite3.connect('sys.db')
    except sqlite3.error as e:
        print(e)
    return conn

def db_init():
    conn = db_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                role VARCHAR(20) NOT NULL,
                first_name VARCHAR(20) NOT NULL,
                middle_initial VARCHAR(20),
                last_name VARCHAR(20) NOT NULL,
                street_number INTEGER NOT NULL,
                street_name VARCHAR(20) NOT NULL,
                apt_number INTEGER,
                city VARCHAR(20) NOT NULL,
                province VARCHAR(20) NOT NULL,
                postal_code VARCHAR(6) NOT NULL,
                SSN INTEGER NOT NULL,
                email VARCHAR(40) NOT NULL,
                gender VARCHAR(20) NOT NULL,
                CONSTRAINT valid_SSN CHECK (SSN <= 999999999 AND SSN >= 100000000)
                );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS branch (
                 branch_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 street_number INTEGER NOT NULL,
                 street_name VARCHAR(20) NOT NULL,
                 city VARCHAR(20) NOT NULL,
                 province VARCHAR(20) NOT NULL,
                 postal_code VARCHAR(20) NOT NULL,
                 manager INTEGER,
                 num_of_receptionist INTEGER,
                 FOREIGN KEY (manager) REFERENCES employee(ID)
                 CONSTRAINT valid_recep CHECK (num_of_receptionist <= 2)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS employee (
                 ID INTEGER UNIQUE NOT NULL,
                 employee_type VARCHAR(20) NOT NULL,
                 salary INTEGER NOT NULL,
                 branch_ID INTEGER NOT NULL,
                 FOREIGN KEY (ID) REFERENCES users(ID)
                 FOREIGN KEY (branch_ID) REFERENCES branch (branch_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS patient (
                 ID INTEGER UNIQUE NOT NULL,
                 insurance VARCHAR(20) NOT NULL,
                 date_of_birth VARCHAR(10) NOT NULL,
                 age INTEGER NOT NULL,
                 FOREIGN KEY (ID) REFERENCES users(ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS appointment (
                 appointment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_ID INTEGER NOT NULL,
                 employee_ID INTEGER NOT NULL,
                 date VARCHAR(10) NOT NULL,
                 start_time VARCHAR(5) NOT NULL,
                 end_time VARCHAR(5) NOT NULL,
                 appointment_type VARCHAR(20) NOT NULL,
                 status VARCHAR(20) NOT NULL,
                 room_number INTEGER NOT NULL,
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID),
                 FOREIGN KEY (employee_ID) REFERENCES employee(ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS insurance_claim (
                 claim_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 claim_code INTEGER NOT NULL
                 );
    """)

    # patient_charge and insurance_charge can be null? maybe?
    # add in appointment_procedure
    c.execute("""CREATE TABLE IF NOT EXISTS patient_billing (
                 payment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_ID INTEGER NOT NULL,
                 patient_charge INTEGER NOT NULL,
                 insurance_charge INTEGER NOT NULL,
                 claim_ID INTEGER NOT NULL,
                 covered_by_emp INTEGER,
                 FOREIGN KEY (claim_ID) REFERENCES insurance_claim(claim_ID),
                 FOREIGN KEY (covered_by_emp) REFERENCES employee(ID),
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID)
                 );
    """)
    # description can be NULL and tooth_involved can also be null if there is no tooth exactly (ex. general cleaning)
    # add in appointment_ID
    c.execute("""CREATE TABLE IF NOT EXISTS appointment_procedure (
                 appPro_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 patient_ID INTEGER NOT NULL,
                 appointment_ID INTEGER NOT NULL,
                 procedure_code INTEGER NOT NULL,
                 procedure_type VARCHAR(20) NOT NULL,
                 description VARCHAR(300),
                 tooth_involved INTEGER,
                 payment_ID INTEGER NOT NULL,
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID),
                 FOREIGN KEY (payment_ID) REFERENCES patient_billing(payment_ID),
                 FOREIGN KEY (appointment_ID) REFERENCES appointment(appointment_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS fee_charge (
                 fee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 appPro_ID INTEGER NOT NULL,
                 fee_code INTEGER NOT NULL,
                 charge INTEGER NOT NULL,
                 FOREIGN KEY (appPro_ID) REFERENCES appointment_procedure(appPro_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS invoice (
                 appPro_ID INTEGER NOT NULL,
                 date_of_issue VARCHAR(10) NOT NULL,
                 patient_ID INTEGER NOT NULL,
                 patient_charge INTEGER NOT NULL,
                 insurance_charge INTEGER NOT NULL,
                 discount INTEGER NOT NULL,
                 penalty INTEGER NOT NULL,
                 fee_ID INTEGER NOT NULL,
                 FOREIGN KEY (appPro_ID) REFERENCES appointment_procedure(appPro_ID),
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID),
                 FOREIGN KEY (fee_ID) REFERENCES fee_charge(fee_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS amount (
                 appPro_ID INTEGER NOT NULL,
                 quantity INTEGER NOT NULL,
                 substance_type VARCHAR(20) NOT NULL,
                 FOREIGN KEY (appPro_ID) REFERENCES appointment_procedure(appPro_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS treatment (
                 treatment_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 appointment_ID INTEGER NOT NULL,
                 appPro_ID INTEGER NOT NULL,
                 treatment_type VARCHAR(20) NOT NULL,
                 medication VARCHAR(20) NOT NULL,
                 comment VARCHAR(300) NOT NULL,
                 FOREIGN KEY (appointment_ID) REFERENCES appointment(appointment_ID),
                 FOREIGN KEY (appPro_ID) REFERENCES appointment_procedure(appPro_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS record (
                 patient_ID INTEGER NOT NULL,
                 treatment_ID INTEGER NOT NULL,
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID),
                 FOREIGN KEY (treatment_ID) REFERENCES treatment(treatment_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS review (
                 patient_ID INTEGER NOT NULL,
                 professionalism INTEGER NOT NULL,
                 communication INTEGER NOT NULL,
                 cleanliness INTEGER NOT NULL,
                 value INTEGER NOT NULL,
                 FOREIGN KEY (patient_ID) REFERENCES patient(ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS guardian (
                 ID INTEGER NOT NULL,
                 insurance VARCHAR(20) NOT NULL,
                 date_of_birth VARCHAR(10) NOT NULL,
                 age INTEGER NOT NULL,
                 looks_over INTEGER NOT NULL,
                 FOREIGN KEY (ID) REFERENCES users(ID),
                 FOREIGN KEY (looks_over) REFERENCES patient(ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS phone (
                 ID INTEGER NOT NULL,
                 type VARCHAR(20) NOT NULL,
                 phone_number VARCHAR(13) NOT NULL,
                 FOREIGN KEY (ID) REFERENCES users(ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS payment (
                 payment_ID INTEGER NOT NULL,
                 payment_type VARCHAR(20) NOT NULL,
                 payment_number INTEGER,
                 FOREIGN KEY (payment_ID) REFERENCES patient_billing(payment_ID)
                 );
    """)

    c.execute("""CREATE TABLE IF NOT EXISTS symptom (
                 treatment_ID INTEGER NOT NULL,
                 symptom_type VARCHAR(20) NOT NULL,
                 FOREIGN KEY (treatment_ID) REFERENCES treatment(treatment_ID)
                 );
    """)
    conn.commit()

# -- Create table symptom(
# -- 	treatment_ID integer not null,
# -- 	symptom_type varchar(20) not null,
# -- 	Foreign Key (treatment_ID) references treatment(treatment_ID)
# -- );

# Only use this function after the termination of all data / tables
# def initialize_data():
#     conn = db_connection()
#     c = conn.cursor()
#     db_init()
#     # insert branch first, to insert emp
#     c.execute(f"INSERT INTO branch VALUES (1, 1, 'street_name', 'city', 'province', 'postal_code', 1, 2)")
#     c.execute(f"INSERT INTO users VALUES (1, 'admin_role', 'f_name', 'm_init', 'l_name', 1, 'street', NULL, 'city', 'province', 'A1AB2B', 999999999, 'admin@email.com', 'gender')")
#     conn.commit()

# Do not use this function unless needed
def delete_all_data():
    conn = db_connection()
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS employee")
    c.execute("DROP TABLE IF EXISTS patient")
    c.execute("DROP TABLE IF EXISTS branch")
    c.execute("DROP TABLE IF EXISTS appointment")
    c.execute("DROP TABLE IF EXISTS insurance_claim")
    c.execute("DROP TABLE IF EXISTS patient_billing")
    c.execute("DROP TABLE IF EXISTS appointment_procedure")
    c.execute("DROP TABLE IF EXISTS fee_charge")
    c.execute("DROP TABLE IF EXISTS invoice")
    c.execute("DROP TABLE IF EXISTS amount")
    c.execute("DROP TABLE IF EXISTS treatment")
    c.execute("DROP TABLE IF EXISTS record")
    c.execute("DROP TABLE IF EXISTS review")
    c.execute("DROP TABLE IF EXISTS guardian")
    c.execute("DROP TABLE IF EXISTS phone")
    c.execute("DROP TABLE IF EXISTS payment")
    c.execute("DROP TABLE IF EXISTS symptom")
    db_init()
    conn.commit()

# Make sure the data is initialized by the function initialize_data
def create_sample_data():
    # street_number, street_name, city, province, postal_code, manager, num_of_receptionist
    insert_branch(290, 'Bremner', 'Toronto', 'ON', 'M5V3L9', 'NULL', 0)
    insert_branch(2000, 'Meadowvale', 'Toronto', 'ON', 'M1B5K7', 'NULL', 0)

    # emp_type, salary, branch_ID, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender
    insert_emp('FT', 60000, 1, 'emp', 'Alexander', 'KS', 'Yu', 27, 'Ambercroft', 'NULL', 'Scarborough', 'ON', 'M1W2Z6', 300120635, 'ayu041@uottawa.ca', 'male')
    assign_man(1, 1)
    insert_emp('FT', 65000, 2, 'den', 'Alexis', 'R', 'Verana', 90, 'University', 'NULL', 'Ottawa', 'ON', 'K1N6N5', 300116080, 'avera086@uottawa.ca', 'female')
    assign_man(2, 2)
    insert_emp('FT', 60000, 1, 'recep', 'Vanisha', 'NULL', 'Bagga', 45, 'Mann', 36, 'Ottawa', 'ON', 'K1N6Y7', 300191679, 'vbagg019@uottawa.ca', 'female')
    insert_emp('FT', 62000, 2, 'dass', 'Christiane', 'A', 'Meherete', 350, 'Victoria', 'NULL', 'Toronto', 'ON', 'M5B2K3', 300116269, 'cmehe017@uottawa.ca', 'female')
    insert_emp('FT', 65000, 1, 'den', 'Coralie', 'B', 'Ostertag', 27, 'College', 'NULL', 'Toronto', 'ON', 'M5S1A1', 300174530, 'coste017@uottawa.ca', 'female')
    insert_emp('FT', 40000, 2, 'recep', 'Toto', 'NULL', 'Wolff', 54, 'University', 'NULL', 'Toronto', 'ON', 'M5S2L1', 932049561, 'totoWolff@f1merc.ca', 'male')

    # insurance, date_of_birth, age, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender
    insert_pat('Manulife', '1972/12/15', 49, 'pat', 'Emily', 'R', 'Cruz', 23, 'King Edward', 'NULL', 'Ottawa', 'ON', 'K2N5G6', 151312658, 'emil54@yahoo.ca', 'female')
    insert_pat('Desjardins', '1999/06/25', 21, 'pat', 'Sheena', 'M', 'Lam', 4, 'Rideau', 'NULL', 'Ottawa', 'ON', 'K1N2F3', 192568463, 'sheeshna09@gmail.com', 'female')
    insert_pat('Aviva', '2001/02/13', 21, 'pat', 'Daniel', 'NULL', 'Ng', 5, 'Huntwood', 'NULL', 'Scarborough', 'ON', 'M1W5G7', 753126145, 'dannyphantom@gmail.com', 'male')

    # patient_ID, employee_ID, date, start_time, end_time, appointment_type, status, room_number
    insert_appointment(get_users_SSN(151312658)[0], 2, '2022/04/15', '11:25', '13:10', 'cleaning', 'scheduled', 14)
    insert_appointment(get_users_SSN(753126145)[0], 5, '2022/04/01', '10:15', '12:30', 'Root Canal', 'completed', 3)
    insert_appointment(get_users_SSN(753126145)[0], 5, '2022/04/02', '16:30', '17:00', 'Checkup', 'completed', 3)

    insert_insurance_claim(5000)
    insert_insurance_claim(6500)

    # patient_ID, patient_charge, insurance_charge, claim_ID, covered_by_emp
    insert_patient_billing(get_users_SSN(151312658)[0], 250, 50, 1, 'NULL')
    insert_patient_billing(get_users_SSN(753126145)[0], 500, 2400, 2, 'NULL')

    # patient_ID, appointment_ID, procedure_code, procedure_type, description, tooth_involved, payment_ID
    insert_appointment_procedure(get_users_SSN(151312658)[0], get_appointment_patient_info(get_users_SSN(151312658)[0], '2022/04/15')[0], 5, 'cleaning', 'General cleaning', 'NULL', 1)
    insert_appointment_procedure(get_users_SSN(753126145)[0], get_appointment_patient_info(get_users_SSN(753126145)[0], '2022/04/01')[0], 13, 'Root Canal', 'T10 RC', 10, 2)

    # no fee charge as user was not late / cancelled 24 hours before
    # appPro_ID, fee_code, charge
    insert_fee_charge(1, 0, 0)
    insert_fee_charge(2, 0, 0)

    # appPro_ID, date_of_issue, patient_ID, patient_charge, insurance_charge, discount, penalty, fee_ID
    insert_invoice(1, '2022/04/21', get_users_SSN(151312658)[0], 250, 50, 0, 0, 1)
    insert_invoice(2, '2022/04/10', get_users_SSN(753126145)[0], 500, 2400, 0, 0, 2)

    # appPro_ID, quantity, substance_type
    insert_amount(1, 50, 'Flouride')
    insert_amount(2, 30, 'Procaine')

    # appointment_ID, appPro_ID, treatment_type, medication, comment
    insert_treatment(1, 1, 'None', 'None', 'General cleaning')
    insert_treatment(2, 2, 'Pain killers', 'opioid', 'T10 RT completed wait till checkup')

    # patient_ID, treatment_ID
    insert_record(get_users_SSN(151312658)[0], 1)
    insert_record(get_users_SSN(753126145)[0], 2)

    # patient_ID, professionalism, communication, cleanliness, value
    insert_review(get_users_SSN(151312658)[0], 5, 5, 5, 5)
    insert_review(get_users_SSN(753126145)[0], 5, 3, 4, 5)

    insert_pat('Sunlife', '2015/01/15', 7, 'pat', 'John', 'B', 'Flabs', 13, 'Marylane', 'NULL', 'Ottawa', 'ON', 'K1N3Z7', 301242471, 'jflabs@gmail.com', 'male')
    # insurance, date_of_birth, age, looks_over, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender
    insert_guard('Sunlife', '1995/03/12', 27, get_users_SSN(301242471)[0], 'guard', 'Claire', 'NULL', 'Flabs', 13, 'Marylane', 'NULL', 'Ottawa', 'ON', 'K1N3Z7', 687478291, 'claire23@gmail.com', 'female')

    # ID, type, phone_number
    insert_phone(get_users_SSN(300120635)[0], 'Cell', '(647)123-4567')
    insert_phone(get_users_SSN(300120635)[0], 'Work', '(416)123-4567')
    insert_phone(get_users_SSN(753126145)[0], 'Cell', '(647)214-7589')
    insert_phone(get_users_SSN(753126145)[0], 'Work', '(416)007-6530')

    # payment_ID, payment_type, payment_number
    insert_payment(get_patient_billing_patient_ID(get_users_SSN(151312658)[0])[0][0], 'credit card', 111111111111)
    insert_payment(get_patient_billing_patient_ID(get_users_SSN(151312658)[0])[0][0], 'debit card', 123412341234)

    # treatment_ID, symptom_type
    insert_symptom(2, 'drowsy')

# Please do not use this function to insert, use the insert_emp or insert_pat
def insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE SSN = {SSN}")
    list = c.fetchall()
    if(SSN >  999999999 or SSN < 99999999):
        print("ERROR: Invalid SSN")
        return "ERROR: Invalid SSN"
    elif (len(list) != 0):
        print("ERROR: SSN is already in the system")
        return "ERROR: SSN is already in the system"

    c.execute(f"""INSERT INTO users (role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender)
                  VALUES ('{role}', '{first_name}', '{middle_initial}', '{last_name}', {street_number}, '{street_name}', {apt_number}, '{city}', '{province}', '{postal_code}', {SSN}, '{email}', '{gender}');""")
    conn.commit()
    entry = get_users_SSN(SSN)
    return entry

def insert_emp(emp_type, salary, branch_ID, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    entry = insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender)
    conn.commit()
    if (isinstance(entry, str)):
        return entry
    c.execute(f"""INSERT INTO employee (ID, employee_type, salary, branch_ID)
                  VALUES ({entry[0]}, '{emp_type}', {salary}, {branch_ID});""")
    conn.commit()

    if (role == 'recep'):
        status = assign_recep(branch_ID, entry[0])
        if(isinstance(status, str)):
            c.execute(f"""DELETE FROM employee WHERE ID = {entry[0]}""")
            c.execute(f"""DELETE FROM users WHERE ID = {entry[0]}""")
            conn.commit()
            return status
    newEntry = get_emp_ID(entry[0])
    return newEntry

def insert_pat(insurance, date_of_birth, age, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    entry = insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender)
    conn.commit()
    if(isinstance(entry, str)):
        return entry
    c.execute(f"""INSERT INTO patient (ID, insurance, date_of_birth, age)
                  VALUES ({entry[0]}, '{insurance}', '{date_of_birth}', {age})""")
    conn.commit()
    newEntry = get_pat_ID(entry[0])
    return newEntry

def insert_branch(street_number, street_name, city, province, postal_code, manager, num_of_receptionist):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO branch (street_number, street_name, city, province, postal_code, manager, num_of_receptionist)
                  VALUES ({street_number}, '{street_name}', '{city}', '{province}', '{postal_code}', {manager}, '{num_of_receptionist}')""")
    conn.commit()
    entry = get_branch_street(street_number, street_name)
    return entry

def insert_appointment(patient_ID, employee_ID, date, start_time, end_time, appointment_type, status, room_number):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO appointment (patient_ID, employee_ID, date, start_time, end_time, appointment_type, status, room_number)
                  VALUES ({patient_ID}, {employee_ID}, '{date}', '{start_time}', '{end_time}', '{appointment_type}', '{status}', {room_number})""")
    conn.commit()
    entry = get_appointment_patient_info(patient_ID, date)
    return entry

def insert_insurance_claim(claim_code):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO insurance_claim (claim_code)
                  VALUES ({claim_code})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM insurance_claim WHERE rowid = {row_ID}""")
    claim_ID = c.fetchone()[0]
    entry = get_insurance_claim_ID(claim_ID)
    return entry

def insert_patient_billing(patient_ID, patient_charge, insurance_charge, claim_ID, covered_by_emp):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO patient_billing (patient_ID, patient_charge, insurance_charge, claim_ID, covered_by_emp)
                  VALUES ({patient_ID}, {patient_charge}, {insurance_charge}, {claim_ID}, {covered_by_emp})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM patient_billing WHERE rowid = {row_ID}""")
    payment_ID = c.fetchone()[0]
    entry = get_patient_billing_payment_ID(payment_ID)
    return entry

def insert_appointment_procedure(patient_ID, appointment_ID, procedure_code, procedure_type, description, tooth_involved, payment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO appointment_procedure (patient_ID, appointment_ID, procedure_code, procedure_type, description, tooth_involved, payment_ID)
                  VALUES ({patient_ID}, {appointment_ID}, {procedure_code}, '{procedure_type}', '{description}', {tooth_involved}, {payment_ID})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM appointment_procedure WHERE rowid = {row_ID}""")
    appPro_ID = c.fetchone()[0]
    entry = get_appointment_procedure_appPro_ID(appPro_ID)
    return entry

def insert_fee_charge(appPro_ID, fee_code, charge):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO fee_charge (appPro_ID, fee_code, charge)
                  VALUES ({appPro_ID}, {fee_code}, {charge})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM fee_charge WHERE rowid = {row_ID}""")
    fee_ID = c.fetchone()[0]
    entry = get_fee_charge_fee_ID(fee_ID)
    return entry

def insert_invoice(appPro_ID, date_of_issue, patient_ID, patient_charge, insurance_charge, discount, penalty, fee_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO invoice (appPro_ID, date_of_issue, patient_ID, patient_charge, insurance_charge, discount, penalty, fee_ID)
                  VALUES ({appPro_ID}, '{date_of_issue}', {patient_ID}, {patient_charge}, {insurance_charge}, {discount}, {penalty}, {fee_ID})""")
    conn.commit()
    entry = get_invoice_appPro_ID(appPro_ID)
    return entry

def insert_amount(appPro_ID, quantity, substance_type):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO amount (appPro_ID, quantity, substance_type)
                  VALUES ({appPro_ID}, {quantity}, '{substance_type}')""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM amount WHERE rowid = {row_ID}""")
    tuple = c.fetchone()
    appPro_ID, substance_type = tuple[0], tuple[2]
    entry = get_amount_appPro_ID_substance_type(appPro_ID, substance_type)
    return entry

def insert_treatment(appointment_ID, appPro_ID, treatment_type, medication, comment):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO treatment (appointment_ID, appPro_ID, treatment_type, medication, comment)
                  VALUES ({appointment_ID}, {appPro_ID}, '{treatment_type}', '{medication}', '{comment}')""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM treatment WHERE rowid = {row_ID}""")
    treatment_ID = c.fetchone()[0]
    entry = get_treatment_treatment_ID(treatment_ID)
    return entry

def insert_record(patient_ID, treatment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO record (patient_ID, treatment_ID)
                  VALUES ({patient_ID}, {treatment_ID})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM record WHERE rowid = {row_ID}""")
    return c.fetchone()

def insert_review(patient_ID, professionalism, communication, cleanliness, value):
    conn = db_connection()
    c = conn.cursor()
    # change so that only one review is possible
    c.execute(f"SELECT * FROM review WHERE patient_ID = {patient_ID}")
    list = c.fetchall()
    if (len(list) != 0):
        # print("Patient already made a review!")
        return "Patient already made a review!"

    c.execute(f"""INSERT INTO review (patient_ID, professionalism, communication, cleanliness, value)
                  VALUES ({patient_ID}, {professionalism}, {communication}, {cleanliness}, {value})""")
    conn.commit()
    entry = get_review_patient_ID(patient_ID)
    return entry

def insert_guard(insurance, date_of_birth, age, looks_over, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender):
    conn = db_connection()
    c = conn.cursor()
    entry = insert_users(role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender)
    conn.commit()
    if(isinstance(entry, str)):
        if("system" in entry):
            # user is already in the system we can still add them!
            guard = get_users_SSN(SSN)
            c.execute(f"""INSERT INTO guardian (ID, insurance, date_of_birth, age, looks_over)
                          VALUES ({guard[0]}, '{insurance}', '{date_of_birth}', {age}, {looks_over})""")
            conn.commit()
            row_ID = c.lastrowid
            c.execute(f"""SELECT * FROM guardian WHERE rowid = {row_ID}""")
            guard_ID = c.fetchone()[0]
            newEntry = get_guard_ID(guard_ID)
            return newEntry

        return entry
    c.execute(f"""INSERT INTO guardian (ID, insurance, date_of_birth, age, looks_over)
                  VALUES ({entry[0]}, '{insurance}', '{date_of_birth}', {age}, {looks_over})""")
    conn.commit()
    newEntry = get_guard_ID(entry[0])
    return newEntry

def insert_phone(ID, type, phone_number):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO phone (ID, type, phone_number)
                  VALUES ({ID}, '{type}', '{phone_number}')""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM phone WHERE rowid = {row_ID}""")
    return c.fetchone()

def insert_payment(payment_ID, payment_type, payment_number):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO payment (payment_ID, payment_type, payment_number)
                  VALUES ({payment_ID}, '{payment_type}', {payment_number})""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM payment WHERE rowid = {row_ID}""")
    return c.fetchone()

def insert_symptom(treatment_ID, symptom_type):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""INSERT INTO symptom (treatment_ID, symptom_type)
                  VALUES ({treatment_ID}, '{symptom_type}')""")
    conn.commit()
    row_ID = c.lastrowid
    c.execute(f"""SELECT * FROM treatment WHERE rowid = {row_ID}""")
    return c.fetchone()

def assign_man(branch_ID, manager):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""UPDATE branch SET manager = {manager} WHERE branch_ID = {branch_ID}""")
    conn.commit()

def assign_recep(branch_ID, recep):
    conn = db_connection()
    c = conn.cursor()
    entry = get_branch_branch_ID(branch_ID)
    if (entry[-1] == 2):
        print("ERROR: This branch already has two receptionists")
        return "ERROR: This branch already has two receptionists"
    c.execute(f"""UPDATE branch SET num_of_receptionist = {entry[-1] + 1} WHERE branch_ID = {branch_ID}""")
    conn.commit()

def get_users():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users")
    conn.commit()
    return c.fetchall()

def get_pat():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient")
    conn.commit()
    return c.fetchall()

def get_branch():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM branch")
    conn.commit()
    return c.fetchall()

def get_appointment():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment")
    conn.commit()
    return c.fetchall()

def get_insurance_claim():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM insurance_claim")
    conn.commit()
    return c.fetchall()

def get_patient_billing():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient_billing")
    conn.commit()
    return c.fetchall()

def get_appointment_procedure():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment_procedure")
    conn.commit()
    return c.fetchall()

def get_fee_charge():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM fee_charge")
    conn.commit()
    return c.fetchall()

def get_invoice():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM invoice")
    conn.commit()
    return c.fetchall()

def get_amount():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM amount")
    conn.commit()
    return c.fetchall()

def get_treatment():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM treatment")
    conn.commit()
    return c.fetchall()

def get_record():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM record")
    conn.commit()
    return c.fetchall()

def get_review():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM review")
    conn.commit()
    return c.fetchall()

def get_guard():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM guardian")
    conn.commit()
    return c.fetchall()

def get_phone():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM phone")
    conn.commit()
    return c.fetchall()

def get_payment():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM payment")
    conn.commit()
    return c.fetchall()

def get_symptom():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM symptom")
    conn.commit()
    return c.fetchall()

def get_users_ID(ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE ID = {ID}")
    conn.commit()
    return c.fetchone()

def get_pat_ID(ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient WHERE ID = {ID}")
    conn.commit()
    return c.fetchone()

def get_pat_fName_LName_DOB(first_name, last_name, date_of_birth):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"""SELECT p.ID
                  FROM patient AS p,users AS u
                  WHERE u.first_name = '{first_name}'
                  AND u.last_name = '{last_name}'
                  AND p.date_of_birth = '{date_of_birth}'
                  AND u.role = 'pat'
                  AND p.ID = u.ID""")
    conn.commit()
    return c.fetchall()


def get_users_SSN(SSN):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE SSN = {SSN}")
    conn.commit()
    return c.fetchone()

def get_branch_street(street_number, street_name):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM branch WHERE street_number = {street_number} AND street_name = '{street_name}'")
    conn.commit()
    return c.fetchone()

def get_branch_man(manager):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM branch WHERE manager = {manager}")
    conn.commit()
    return c.fetchone()

def get_branch_branch_ID(branch_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM branch WHERE branch_ID = {branch_ID}")
    conn.commit()
    return c.fetchone()

def get_emp():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM employee")
    conn.commit()
    return c.fetchall()

def get_emp_ID(ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM employee WHERE ID = {ID}")
    conn.commit()
    return c.fetchone()

def get_appointment_patient_info(patient_ID, date):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment WHERE patient_ID = {patient_ID} AND date = '{date}'")
    conn.commit()
    return c.fetchone()

def get_appointment_list_patient_info(patient_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT appointment_ID FROM appointment WHERE patient_ID = {patient_ID}")
    conn.commit()
    return c.fetchall()

def get_insurance_claim_ID(claim_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM insurance_claim WHERE claim_ID = {claim_ID}")
    conn.commit()
    return c.fetchone()

def get_patient_billing_payment_ID(payment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient_billing WHERE payment_ID = {payment_ID}")
    conn.commit()
    return c.fetchone()

def get_patient_billing_patient_ID(patient_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM patient_billing WHERE patient_ID = {patient_ID}")
    conn.commit()
    return c.fetchall()

def get_symptom_treatment_ID(treatment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM symptom WHERE treatment_ID = {treatment_ID}")
    conn.commit()
    return c.fetchall()

def get_appointment_procedure_appPro_ID(appPro_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment_procedure WHERE appPro_ID = {appPro_ID}")
    conn.commit()
    return c.fetchone()

def get_appointment_appointment_ID(appointment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment WHERE appointment_ID = {appointment_ID}")
    conn.commit()
    return c.fetchone()

def get_fee_charge_fee_ID(fee_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM fee_charge WHERE fee_ID = {fee_ID}")
    conn.commit()
    return c.fetchone()

def get_invoice_appPro_ID(appPro_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM invoice WHERE appPro_ID = {appPro_ID}")
    conn.commit()
    return c.fetchone()

def get_amount_appPro_ID_substance_type(appPro_ID, substance_type):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM amount WHERE appPro_ID = {appPro_ID} AND substance_type = '{substance_type}'")
    conn.commit()
    return c.fetchone()

def get_treatment_treatment_ID(treatment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM treatment WHERE treatment_ID = {treatment_ID}")
    conn.commit()
    return c.fetchone()

def get_record_patient_ID(patient_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM record WHERE patient_ID = {patient_ID}")
    conn.commit()
    return c.fetchall()

def get_appointment_procedure_patient_ID(patient_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment_procedure WHERE patient_ID = {patient_ID}")
    conn.commit()
    return c.fetchall()

def get_review_patient_ID(patient_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM review WHERE patient_ID = {patient_ID}")
    conn.commit()
    return c.fetchone()

def get_guard_ID(guard_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM guardian WHERE ID = {guard_ID}")
    conn.commit()
    return c.fetchone()

def get_phone_ID(ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM phone WHERE ID = {ID}")
    conn.commit()
    return c.fetchall()

def get_phone_ID_type(ID, type):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM phone WHERE ID = {ID} AND type = '{type}'")
    conn.commit()
    return c.fetchone()

def get_payment_payment_ID(payment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM payment WHERE payment_ID = {payment_ID}")
    conn.commit()
    return c.fetchall()

def get_appointment_procedure_appointment_ID(appointment_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM appointment_procedure WHERE appointment_ID = {appointment_ID}")
    conn.commit()
    return c.fetchall()

def get_invoice_patient_ID(patient_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM invoice WHERE patient_ID = {patient_ID}")
    conn.commit()
    return c.fetchall()

def get_treatment_appointment_ID_appPro_ID(appointment_ID, appPro_ID):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM treatment WHERE appointment_ID = {appointment_ID} AND appPro_ID = {appPro_ID}")
    conn.commit()
    return c.fetchone()

def update_treatment_treatment_type_treatment_ID(treatment_ID, treatment_type):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"UPDATE treatment SET treatment_type = '{treatment_type}' WHERE treatment_ID = {treatment_ID}")
    conn.commit()

def update_treatment_medication_treatment_ID(treatment_ID, medication):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"UPDATE treatment SET medication = '{medication}' WHERE treatment_ID = {treatment_ID}")
    conn.commit()

def update_treatment_comment_treatment_ID(treatment_ID, comment):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"UPDATE treatment SET comment = '{comment}' WHERE treatment_ID = {treatment_ID}")
    conn.commit()

def print_tables():
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT name FROM sqlite_schema WHERE type='table'")
    print(c.fetchall())

def printer(table, table_name):
    conn = db_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table_name}")
    print(f"\nTable: {table_name}\n")
    names = list(map(lambda a: a[0], c.description))
    print(names)
    for x in table:
        print(x)
    print("*******************************************************************")

def main():
    delete_all_data()
    # initialize_data()
    create_sample_data()
    # print_tables()
    # printer(get_users(), 'users')
    # printer(get_emp(), 'employee')
    # printer(get_pat(), 'patient')
    # printer(get_branch(), 'branch')
    # printer(get_appointment(), 'appointment')
    # printer(get_insurance_claim(), 'insurance_claim')
    # printer(get_patient_billing(), 'patient_billing')
    # printer(get_appointment_procedure(), 'appointment_procedure')
    # printer(get_fee_charge(), 'fee_charge')
    # printer(get_invoice(), 'invoice')
    # printer(get_amount(), 'amount')
    # printer(get_treatment(), 'treatment')
    # printer(get_record(), 'record')
    # printer(get_review(), 'review')
    # printer(get_guard(), 'guardian')
    # printer(get_phone(), 'phone')
    # printer(get_payment(), 'payment')
    # printer(get_symptom(), 'symptom')

main()
