from flask import Flask, render_template, flash, request, redirect, url_for
from db import *
from patientsearchform import PatientSearchForm
from patientChooseForm import PatientChooseForm
from patientform import ReceptionForm
from appointform import AppointForm
from patientAppForm import PatientAppForm
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = '6f80377f374a443dd2288eb00e322026'

@app.route("/")
def home():
    # status = insert_emp('client', 'John', 'D', 'Doe', 12, 'Toronto', 'Ontario', 123123123, 'JohnDoe@gmail.com', 'male')
    # if ("ERROR" in status):
    #     return status

    
    
    return render_template('index.html')

@app.route("/users")
def user_info():
    print(get_users())
    return "Users page has rendered!"

@app.route("/patient", methods=['GET', 'POST'])
def patient():
    form = PatientSearchForm()

    if request.method == "POST":

       first_name = request.form.get("fname")
       last_name = request.form.get("lname")
       dob = request.form.get("dob")
       
       try:
           patientID = (get_pat_fName_LName_DOB(first_name, last_name, dob))[0][0]
           
       except IndexError:
            patientID = (get_pat_fName_LName_DOB('Daniel', 'Ng', '2001/02/13'))[0][0]
       try:
            if "app" in request.form:
                patientApp = get_appointment_list_patient_info(patientID)

                nums = ''
                for x in patientApp:
                    for y in x:
                        print(y)
                        nums += str(y) + '&'

                nums = nums[:-1]
                return redirect(url_for('patient_app', patientApp = nums))

            elif "treatment" in request.form:
                return redirect(url_for('patient_treatment', patientID = patientID))

            elif "invoice" in request.form:
                return redirect(url_for('patient_invoice', patientID = patientID))


       except IndexError:
            #return ("No previous or upcoming appointments to show. Have a good!")
            return "error bruv"

    return render_template('patient.html', title='Patient', form=form)

#     print("PATIENT CHOOSE  " + str(patientID))
#     print("STILL  " +  str(patientID))

#     if "app" in request.form:
#         print("APPOINTMENT OPEN")
#         print("APPOINTMENT ID  " + str(patientID))
#         return redirect(url_for('patient_app', patientID = patientID))
    
#     elif "treatment" in request.form: 
#         print("TREATMENT OPEN")
#         return redirect(url_for('patient_treatment', patientID = patientID))
    
#     elif "invoice" in request.form: 
#         print("INVOICE OPENs")
#         return redirect(url_for('patient_invoice', patientID = patientID))

#     return render_template('patient_2.html')  
# this is new
@app.route("/reception", methods=['GET', 'POST'])
def reception():
    form = ReceptionForm()
    if request.method == "POST":
        Modified_Insurance = request.form.get("modIns")
        
        Pfirst_name = request.form.get("pfname")
        Pmiddle_name = request.form.get("pmname") 
        Plast_name = request.form.get("plname") 
        Prole = request.form.get("prle")
        Pgender = request.form.get("pgen")
        Pemail = request.form.get("pem")
        Pssn = request.form.get("pssn")
        Pstreetname = request.form.get("psname")
        Pstreetnum = request.form.get("psnum")
        Papartnum = request.form.get("panum")
        Pcity = request.form.get("pcit")
        Pprovince = request.form.get("pprov")
        Ppostalcode = request.form.get("ppcode")
        Pdob = request.form.get("pdob")
        Pinsurance = request.form.get("pinsur")
        Page = request.form.get("patage")

        Efirst_name = request.form.get("efname")
        Emiddle_name = request.form.get("emname") 
        Elast_name = request.form.get("elname") 
        Erole = request.form.get("erle")
        Egender = request.form.get("egen")
        Ebranch_ID = request.form.get("ebranch")
        Eemployeetype = request.form.get("etype")
        Esalary = request.form.get("esalary")
        Eemail = request.form.get("eem")
        Essn = request.form.get("essn")
        Estreetname = request.form.get("esname")
        Estreetnum = request.form.get("esnum")
        Eapartnum = request.form.get("eanum")
        Ecity = request.form.get("ecit")
        Eprovince = request.form.get("eprov")
        Epostalcode = request.form.get("epcode")

        # insurance, date_of_birth, age, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender
        if "preg" in request.form:
            entry = insert_pat(Pinsurance, Pdob, Page, Prole, Pfirst_name, Pmiddle_name, Plast_name, Pstreetnum, Pstreetname, Papartnum, Pcity, Pprovince, Ppostalcode, Pssn, Pemail, Pgender)
            print("PATIENT ADDED")
        # emp_type, salary, branch_ID, role, first_name, middle_initial, last_name, street_number, street_name, apt_number, city, province, postal_code, SSN, email, gender
        elif "ereg" in request.form:
            entry = insert_pat(Eemployeetype, Esalary, Ebranch_ID, Erole, Efirst_name, Emiddle_initial, Elast_name, Estreetnum, Estreetname, Eapartnum, Ecity, Eprovince, Epostalcode, Essn, Eemail, Egender)
            print("EMPLOYEE ADDED")
        # TO BE IMPLEMENTED USING THE EDIT IN DB
        elif "edit" in request.form: 
            print("")
            return redirect(url_for('patient_treatment'))
        elif "appoint" in request.form: 
            print("CREATE NEW APPOINT OPENs")
            return redirect(url_for("appoint"))
            
            #return redirect(url_for('patient_2', patientID = patientID))  #OPENS NEXT PAGE

    return render_template('reception.html', title = 'Patient Form', form=form)

@app.route("/appoint", methods=['GET', 'POST'])
def appoint():
    form = AppointForm()
    if request.method == "POST":
        pid= request.form.get("pd")
        eid = request.form.get("ed") 
        date = request.form.get("da") 
        starttime = request.form.get("start")
        endtime = request.form.get("end")
        appointtype = request.form.get("type") 
        status = request.form.get("stat")
        room = request.form.get("ro")

        if "app" in request.form:
            entry = insert_appointment(pid, eid, date, startime, endtime, appointtype, status, room)
            print("APPOINTMENT ADDED")
     

    return render_template('appoint.html', title = 'Appointment Form', form=form)


@app.route("/patient_app", methods=['GET', 'POST'])
def patient_app():

    form = PatientAppForm()
    patientAppId = request.args.get('patientApp')
    nums = patientAppId.split('&')

    table = []
    for x in nums:
        app = []
        data = get_appointment_appointment_ID(x)
        app.append(data[3])
        app.append(data[4])
        app.append(data[5])
        app.append(data[6])
        app.append(data[7])
        app.append(data[8])
        table.append(app)

    print("Table " + str (table))
    return render_template('patient_app.html', table=table)

@app.route("/patient_treatment", methods=['GET', 'POST'])
def patient_treatment():
    patientId = request.args.get('patientID')
    matrixEntry = get_record_patient_ID(patientId)

    treatment = []

    for x in matrixEntry:
        treatment.append(x[1])

    table = []
    for y in treatment:
        row = []
        data = get_treatment_treatment_ID(y)
        # appointment type index = 1
        appID = get_appointment_appointment_ID(data[1])
        row.append(appID[6])
        row.append(data[3])
        row.append(data[4])
        symp = get_symptom_treatment_ID(y)[0]
        row.append(symp[1])
        appPro = get_appointment_procedure_appointment_ID(y)[0]
        row.append(appPro[6])
        row.append(data[5])
        table.append(row)

    return render_template('patient_treatment.html', table=table)

@app.route("/patient_invoice", methods=['GET', 'POST'])
def patient_invoice():

    patientId = request.args.get('patientID')
    matrixEntry = get_invoice_patient_ID(patientId)
    users = get_users_ID(patientId)
    table2 = []
    fName = users[2]
    table2.append(fName)
    mInit = users[3]
    if (users[3] == 'NULL'):
        mInit= ''
    table2.append(mInit)
    lName = users[4]
    table2.append(lName)
    street_number = users[5]
    table2.append(street_number)
    street_name = users[6]
    table2.append(street_name)
    apt = users[7]
    if (users[7] == None):
        apt= ''
    table2.append(apt)
    city = users[8]
    table2.append(city)
    province = users[9]
    table2.append(province)
    code = users[10]
    table2.append(code)
    email = users[12]
    table2.append(email)
    insurance = get_pat_ID(patientId)[1]
    table2.append(insurance)
    phone = get_phone_ID(patientId)
    phoneString = ''
    for a in phone:
        phoneString += a[1] + ': ' + a[2] + ' '
    table2.append(phoneString)

    table = []
    for x in matrixEntry:
        row = []
        row.append(x[1])
        row.append(x[3])
        row.append(x[4])
        row.append(int(x[3]) + int(x[4]))
        row.append(x[5])
        row.append(x[6])
        table.append(row)

    return render_template('patient_invoice.html', table=table, table2=table2)

@app.route("/dentist", methods=['GET', 'POST'])
def dentist():

    if "dentist_btn" in request.form:
        appID = request.form.get("appID")
        appProID = request.form.get("appProID")
        return redirect(url_for('d_edit', appID=appID, appProID=appProID))

    return render_template('dentist.html')

@app.route("/d_edit", methods=['GET', 'POST'])
def d_edit():

    
    appID = request.args.get('appID')
    appProID = request.args.get('appProID')
    
    table = []
    try:
        treatment = get_treatment_appointment_ID_appPro_ID(appID, appProID)
    except sqlite3.OperationalError:
        treatment = get_treatment_appointment_ID_appPro_ID(2, 2)
    treatment_type = treatment[3]
    table.append(treatment_type)
    medication = treatment[4]
    table.append(medication)
    comment = treatment[5]
    table.append(comment)

    treatment_type_update = request.form.get("treatmentType")
    medication_update = request.form.get("medication")
    comment_update = request.form.get("comment")
    
    treatmentId = treatment[0]
    print("treatment id " + str (treatmentId))

    if "edit_submit" in request.form:
        print("=================================BUTTON CLICKED==============================")
        if (treatment_type_update != ""):
            update_treatment_treatment_type_treatment_ID(treatmentId, treatment_type_update)
        
        if (medication_update != ""): 
            update_treatment_medication_treatment_ID(treatmentId, medication_update)
        
        if (comment_update != ""):
            update_treatment_comment_treatment_ID(treatmentId, comment_update)
        
    return render_template('d_edit.html', table=table)


@app.route("/emp")
def emp_info():
    print(get_emp())
    return "Emp page has rendered!"

if __name__ == "__main__":
    app.run()


