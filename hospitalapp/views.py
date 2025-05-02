from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db import connection

def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # 'doctor' or 'patient'


        if role == "doctor":
            # Doctor login
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM doctor WHERE email = %s AND password = %s", [email, password])
                result = cursor.fetchone()

            if result:
                doctor_id = result[0]
                request.session['doctor_id'] = doctor_id  ## save doctor id when logging in
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM doctor WHERE id = %s", [doctor_id])
                    cols = [col[0] for col in cursor.description]
                    doctor = dict(zip(cols, cursor.fetchone()))
                return render(request, 'home.html', {'data': doctor})
            else:
                error = "Invalid email or password"
                return render(request, 'HospitalApp/login.html', {'error': error})

        else:
            # Patient login
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM patient WHERE email = %s AND password = %s", [email, password])
                result = cursor.fetchone()

            if result:
                patient_id = result[0]
                request.session['patient_id'] = patient_id  ## save patient id when logging in
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM patient WHERE id = %s", [patient_id])
                    cols = [col[0] for col in cursor.description]
                    patient = dict(zip(cols, cursor.fetchone()))
                return render(request, 'home.html', {'data': patient})
            else:
                error = "Invalid email or password"
                return render(request, 'HospitalApp/login.html', {'error': error})


    return render(request, 'HospitalApp/login.html', {'error': error})


from django.shortcuts import render
from django.db import connection

def signup_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone_number = request.POST.get('phone_number')
        role = request.POST.get('role')  # Checkbox input
        # Check if any field is missing
        try:
            table = 'doctor' if role=="doctor" else 'patient'
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO {table} (email, password, birthdate, gender, fname, lname,phone_number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [email, password, birthdate, gender, fname, lname, phone_number])
            return render(request, 'HospitalApp/login.html', {'fname': fname}) ### what should be in context here??
        except Exception as e:
            error = "Error: " + str(e)

    return render(request, 'HospitalApp/register.html', {'error': error})


def update_patient(request):
    patient_id = request.session.get('patient_id')  # Make sure this is set during login

    if not patient_id:
        return redirect('login')  # User must be logged in

    message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone_number = request.POST.get('phone_number')
        bloodtype = request.POST.get('bloodtype')

        fields = []
        values = []

        if email:
            fields.append("email = %s")
            values.append(email)
        if password:
            fields.append("password = %s")
            values.append(password)
        if birthdate:
            fields.append("birthdate = %s")
            values.append(birthdate)
        if gender:
            fields.append("gender = %s")
            values.append(gender)
        if fname:
            fields.append("fname = %s")
            values.append(fname)
        if lname:
            fields.append("lname = %s")
            values.append(lname)
        if phone_number:
            fields.append("phone_number = %s")
            values.append(phone_number)
        if bloodtype:
            fields.append("bloodtype = %s")
            values.append(bloodtype)

        if fields:
            values.append(patient_id)  # For WHERE clause
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                        UPDATE patient
                        SET {", ".join(fields)}
                        WHERE id = %s
                    """, values)
                message = "Patient information updated successfully."
            except Exception as e:
                message = f"Error updating patient: {e}"
        else:
            message = "No fields to update."

    return render(request, 'update_patient.html', {'message': message})


def update_doctor(request):
    doctor_id = request.session.get('doctor_id')  # Make sure this is set during login

    if not doctor_id:
        return redirect('login')  # User must be logged in

    message = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        birthdate = request.POST.get('birthdate')
        gender = request.POST.get('gender')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone_number = request.POST.get('phone_number')

        fields = []
        values = []

        if email:
            fields.append("email = %s")
            values.append(email)
        if password:
            fields.append("password = %s")
            values.append(password)
        if birthdate:
            fields.append("birthdate = %s")
            values.append(birthdate)
        if gender:
            fields.append("gender = %s")
            values.append(gender)
        if fname:
            fields.append("fname = %s")
            values.append(fname)
        if lname:
            fields.append("lname = %s")
            values.append(lname)
        if phone_number:
            fields.append("phone_number = %s")
            values.append(phone_number)

        if fields:
            values.append(doctor_id)  # For WHERE clause
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                        UPDATE patient
                        SET {", ".join(fields)}
                        WHERE id = %s
                    """, values)
                message = "Patient information updated successfully."
            except Exception as e:
                message = f"Error updating patient: {e}"
        else:
            message = "No fields to update."

    return render(request, 'update_doctor.html', {'message': message})

def main_view(request):
    return render(request,'home.html')

