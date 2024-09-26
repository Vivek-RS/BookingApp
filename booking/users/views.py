from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Doctor, Patient, Appointment


def index(request):
    if not request.user.is_staff:
        return redirect('login')
    doctors = Doctor.objects.all()
    patient = Patient.objects.all()
    appointment = Appointment.objects.all()
    d = 0;
    p =0;
    a = 0;
    for i in doctors:
        d = d+1
    for i in patient:
        p = p+1
    for i in appointment:
        a = a + 1
    d1 = {'d':d,'p':p,'a':a}
    return render(request,'index.html',d1)

def doctor_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        mobile_num = request.POST.get('mobile_num')
        specialization = request.POST.get('specialization')


        user = User.objects.create_user(username=username, password=password)

        doctor = Doctor.objects.create(
            user=user,
            name=name,
            mobile_num=mobile_num,
            specialization=specialization
        )

        login(request, user)
        return redirect('doctor_dashboard')  # Redirect to doctor dashboard or profile page
    return render(request, 'doctor_registration.html')

def patient_registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        mobile_num = request.POST.get('mobile_num')
        address = request.POST.get('address')


        user = User.objects.create_user(username=username, password=password)

        patient = Patient.objects.create(
            user=user,
            name=name,
            gender=gender,
            mobile_num=mobile_num,
            address=address
        )
        # Log in the newly registered patient
        login(request, user)
        return redirect('patient_dashboard')  # Redirect to patient dashboard or profile page
    return render(request, 'patient_registration.html')

def doctor_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and Doctor.objects.filter(user=user).exists():
            login(request, user)
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard or profile page
        else:
            # Handle invalid login credentials for doctors
            pass
    return render(request, 'doctor_login.html')

def patient_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and Patient.objects.filter(user=user).exists():
            login(request, user)
            return redirect('patient_dashboard')  # Redirect to patient dashboard or profile page
        else:
            # Handle invalid login credentials for patients
            pass
    return render(request, 'patient_login.html')

def doctor_dashboard(request):
    if request.user.is_authenticated and Doctor.objects.filter(user=request.user).exists():
        # Retrieve doctor's appointments, display relevant information
        doctor = Doctor.objects.get(user=request.user)
        appointments = Appointment.objects.filter(doctor=doctor)
        context = {'appointments': appointments}
        return render(request, 'doctor_dashboard.html', context)
    else:
        return redirect('doctor_login')  # Redirect to doctor login page if not authenticated

def patient_dashboard(request):
    if request.user.is_authenticated and Patient.objects.filter(user=request.user).exists():
        # Display available doctors for appointment booking
        doctors = Doctor.objects.all()
        context = {'doctors': doctors}
        return render(request, 'patient_dashboard.html', context)
    else:
        return redirect('patient_login')  # Redirect to patient login page if not authenticated

def Login(request):
    error = None
    if request.method=="POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('index')
        else:
            error = 'yes'
    d = {'error': error}
    return render(request, 'login.html', d)

def logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('login')

def contact(request):
    return render(request,'contact.html')

def View_doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request,'view_doctor.html',d)

def Add_Doctor(request):
    error = ''
    if not request.user.is_staff:
        return redirect('login')
    if request.method=="POST":
        n = request.POST['name']
        c = request.POST['contact']
        s = request.POST['special']
        try:
            Doctor.objects.create(name=n,mobile_num=c,specialization=s)
            error ='no'
        except:
            error='yes'
    d = {'error': error}
    return render(request, 'add_doctor.html', d)

def Delete_Doctor(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    d = {'pat': pat}
    return render(request,'view_patient.html',d)

def Add_Patient(request):
    error = ''
    if not request.user.is_staff:
        return redirect('login')
    if request.method=="POST":
        n = request.POST['name']
        g = request.POST['gender']
        c = request.POST['mobile']
        a = request.POST['address']
        try:
            Patient.objects.create(name=n,gender=g,mobile_num=c,address=a)
            error ='no'
        except:
            error='yes'
    d = {'error': error}
    return render(request, 'add_patient.html', d)

def Delete_Patient(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    return redirect('view_patient')

def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    appoint = Appointment.objects.all()
    d = {'appoint': appoint}
    return render(request,'view_appointment.html',d)

def Add_Appointment(request):
    error = ''
    if not request.user.is_staff:
        return redirect('login')
    doctor1 = Doctor.objects.all()
    patient1 = Patient.objects.all()
    if request.method=="POST":
        d = request.POST['doctor']
        p = request.POST['patient']
        da = request.POST['date']
        t = request.POST['time']
        doctor = Doctor.objects.filter(name=d).first()
        patient = Patient.objects.filter(name=p).first()
        try:
            Appointment.objects.create(doctor=doctor,patient=patient,date1=da,time1=t)
            error ='no'
        except:
            error='yes'
    d = {'doctor': doctor1,'patient': patient1,'error': error}
    return render(request, 'add_appointment.html', d)

def Delete_Appointment(request,pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('view_appointment')
