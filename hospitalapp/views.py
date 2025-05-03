import base64
import imghdr

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.db import connection

def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')  # 'doctor' or 'patient'
        picture_data = ""
        base64_string = ""
        img_type = "jpeg"


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
                return render(request, 'home.html', {'data': doctor,'role':role })
            else:
                error = "Invalid email or password"
                return render(request, 'HospitalApp/login.html', {'error': error,})

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
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT picture FROM patient WHERE id = %s", [patient_id])
                        row = cursor.fetchone()
                        if row and row[0]:
                            picture_data = row[0]  # This should be the base64 string
                            img_binary = base64.b64decode(picture_data)
                            detected_type = imghdr.what(None, h=img_binary)
                            img_type = detected_type if detected_type else "jpeg"
                            base64_string = base64.b64encode(img_binary).decode('utf-8')

                        #
                    # Fetch patient diagnoses
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT diagnosis FROM Patient_History WHERE pid = %s",
                            [patient_id]
                        )
                        diagnoses = [row[0] for row in cursor.fetchall()]

                    return render(
                        request,
                        'home.html',
                        {
                            'data': patient,
                            'diagnoses': diagnoses,
                            'role': 'patient',
                            'picture_data': picture_data,
                            'img_type': img_type,
                            'base64_string': base64_string,
                        }
                    )
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
        bloodtype = request.POST.get('bloodtype')
        role = request.POST.get('role')  # Checkbox input
        # Check if any field is missing
        try:
            if role=="doctor":
                table = 'doctor'
            elif role=="patient":
                table = 'patient'
            with connection.cursor() as cursor:
                cursor.execute(f"""
                    INSERT INTO {table} (email, password, birthdate, gender, fname, lname,phone_number,bloodtype)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
                """, [email, password, birthdate, gender, fname, lname, phone_number,bloodtype])
            return render(request, 'HospitalApp/login.html', {'fname': fname}) ### what should be in context here??
        except Exception as e:
            error = "Error: " + str(e)

    return render(request, 'HospitalApp/register.html', {'error': error})


def update_patient(request):
    patient_id = request.session.get('patient_id')  # Make sure this is set during login

    if not patient_id:
        return redirect('login')  # User must be logged in

    message = "Hi there"

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

    return render(request, 'HospitalApp/update.html', {'message': message})


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

def change_pic(request):
    patient_id = request.session.get('patient_id')
    message = ""
    picture_data = None
    img_type = "jpeg"  # default fallback

    if request.method == 'POST':
        uploaded_file = request.FILES.get('change_picture')
        if uploaded_file:
            try:
                file_bytes = uploaded_file.read()
                img_type_detected = imghdr.what(None, h=file_bytes)
                img_type = img_type_detected if img_type_detected else "jpeg"  # fallback

                file_data = base64.b64encode(file_bytes).decode('utf-8')

                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE patient SET picture = %s WHERE id = %s",
                        [file_data, patient_id]
                    )

                message = "Patient picture updated successfully."
            except Exception as e:
                message = f"Error updating patient: {e}"
        else:
            message = "No file uploaded."

    # Fetch the updated picture and type
    with connection.cursor() as cursor:
        cursor.execute("SELECT picture FROM patient WHERE id = %s", [patient_id])
        row = cursor.fetchone()
        if row and row[0]:
            picture_data = row[0]

    return render(request, "HospitalApp/preview.html", {
        'message': message,
        'picture_data': picture_data,
        'img_type': img_type
    })
