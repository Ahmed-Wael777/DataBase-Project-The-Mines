from django.shortcuts import render
from django.db import connection

def login_view(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        is_doctor = request.POST.get('is_doctor') == 'on'  # checkbox from attallah

        if is_doctor:
            # Doctor login
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM doctor WHERE email = %s AND password = %s", [email, password])
                result = cursor.fetchone()

            if result:
                doctor_id = result[0]
                with connection.cursor() as cursor:
                    cursor.execute("SELECT fname, lname, id FROM doctor WHERE id = %s", [doctor_id])
                    cols = [col[0] for col in cursor.description]
                    doctor = dict(zip(cols, cursor.fetchone()))
                return render(request, 'welcome_doctor.html', {'data': doctor})
            else:
                error = "Invalid email or password"

        else:
            # Patient login
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM patient WHERE email = %s AND password = %s", [email, password])
                result = cursor.fetchone()

            if result:
                patient_id = result[0]
                with connection.cursor() as cursor:
                    cursor.execute("SELECT fname, lname, id,bloodtype FROM patient WHERE id = %s", [patient_id])
                    cols = [col[0] for col in cursor.description]
                    patient = dict(zip(cols, cursor.fetchone()))
                return render(request, 'welcome_patient.html', {'data': patient})
            else:
                error = "Invalid email or password"

    return render(request, 'login.html', {'error': error})


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
        is_doctor = request.POST.get('is_doctor') == 'on'  # Checkbox input

        # Check if any field is missing
        if not all([email, password, birthdate, gender, fname, lname]):
            error = "All fields are required."
        else:
            try:
                table = 'doctor' if is_doctor else 'patient'
                with connection.cursor() as cursor:
                    cursor.execute(f"""
                        INSERT INTO {table} (email, password, birthdate, gender, fname, lname)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, [email, password, birthdate, gender, fname, lname])
                return render(request, 'login.html', {'fname': fname}) ### what should be in context here??
            except Exception as e:
                error = "Error: " + str(e)

    return render(request, 'signup.html', {'error': error})



