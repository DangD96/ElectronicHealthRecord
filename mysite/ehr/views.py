from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import *
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail

# https://docs.djangoproject.com/en/4.1/topics/auth/default/#the-login-required-decorator
@login_required # Redirects to settings.LOGIN_URL if user not logged in
def index(request):
    user = User.objects.get(username=request.user)
    try:
        doctor = Doctor.objects.get(user=user)
        sort_method = doctor.sort_preference

        if sort_method == 'Age':
            my_patients = doctor.assigned_patients.order_by('age')
        elif sort_method == 'First Name':
            my_patients = doctor.assigned_patients.order_by('first_name')
        elif sort_method == 'Last Name':
            my_patients = doctor.assigned_patients.order_by('last_name')
        else:
            my_patients = doctor.assigned_patients.order_by('id')

        is_doctor = True
        paginator = Paginator(my_patients, 5) # 5 patients per page
        page_number = request.GET.get('page', default=1) # Defaults to 1 if no value
        page_obj = paginator.page(page_number)
    except:
        is_doctor = False
        doctor = None
        page_obj = None

    return render(request, 'ehr/index.html', {
        "is_doctor": is_doctor,
        "doctor": doctor,
        "page_obj": page_obj
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("ehr:index"))
        else:
            return render(request, "ehr/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ehr/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("ehr:index"))

def patient_view(request, id):
    is_doctor = True
    patient = Patient.objects.get(pk=id)
    return render(request, 'ehr/patient_chart.html', {
        "patient": patient,
        "is_doctor": is_doctor
    })

def new_patient(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        email = request.POST['email']
        try:
            photo = request.FILES['photo'] # The Form element needs special attribute so this isn't blank when you provide an image
        except:
            photo = None
        
        # Create Patient object and save it
        new_patient = Patient.objects.create(first_name=first_name, last_name=last_name, age=age, email=email, photo=photo) # Create and save in one step

        # Assumption: If a doctor is creating this patient, they're responsible for the patient
        user = User.objects.get(username=request.user)
        doctor = Doctor.objects.get(user=user)
        doctor.assigned_patients.add(new_patient) # Add to doctor's list of assignments
        
        # Redirect to patient list
        return HttpResponseRedirect(reverse('ehr:index'))
    else:
        try:
            user = User.objects.get(username=request.user)
            doctor = Doctor.objects.get(user=user)
            is_doctor = True
        except:
            is_doctor = False
            return HttpResponse('Only doctors may create new patients.')
        
        return render(request, 'ehr/new_pat.html', {
            "is_doctor": True
        })

# API functions
def set_sort_method(request):
    if request.method == 'PUT':
        user = User.objects.get(username=request.user)
        doctor = Doctor.objects.get(user=user)
        data = json.loads(request.body)
        if data.get("sortMethod") is not None:
            doctor.sort_preference = data["sortMethod"]
            doctor.save()
            return HttpResponse(status=302)
        return HttpResponse(status=400)
    else:
        return HttpResponse('This endpoint only supports PUT requests.', status=400)

def get_sort_method(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=request.user)
            doctor = Doctor.objects.get(user=user)
            preference = doctor.sort_preference
        except:
            return JsonResponse({
                "sortPreference": None
            }, status=400)

        # JsonResponse can show the JSON in the browser and the status in the console
        return JsonResponse({
            "sortPreference": preference
            }, status=200)
    else:
        return HttpResponse('This endpoint only supports GET requests.', status=400)
    
def get_patient_meds(request, id):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=request.user)
            doctor = Doctor.objects.get(user=user)
            patient = Patient.objects.get(pk=id)
            patient_meds = patient.meds.all()
        except:
            return JsonResponse({
                "error": "Only doctor may view a patient's meds."
            }, status=400)

        # JsonResponse can show the JSON in the browser and the status in the console
        return JsonResponse({
            "patientMeds": [med.serialize() for med in patient_meds]
            }, status=200)
    else:
        return HttpResponse('This endpoint only supports GET requests.', status=400)

def save_patient_meds(request,id):
    if request.method == 'POST':
        patient = Patient.objects.get(pk=id)
        data = request.POST
        if data.get("medName") and data.get("medDose") and data.get("doseUnit") is not None:
            for med in patient.meds.all():
                if med.name.upper() == data["medName"].upper():
                    return HttpResponse('Med already exists for patient.')
            
            # Direct assignment to the forward side of a many-to-many set is prohibited. Use patient.set() instead.
            # Create med in two steps due to error above
            new_med = Medication.objects.create(name=data["medName"], dose=data["medDose"], dose_units=data["doseUnit"]) # Set everything except Patient
            patient.meds.add(new_med) # Since this is a Many-To-Many relationship, this will link them up. Use add() instead of set() bc the latter replaces what's existing
            patient.save()
            return HttpResponseRedirect(reverse('ehr:patient', args=[patient.id]), status=302)
        return HttpResponse(status=400)
    else:
        return HttpResponse('This endpoint only supports POST requests.', status=400)

def send_email(request):
    if request.method == 'POST':
        email_from = 'finalproject@harvard.edu'
        data = request.POST
        if data.get("recipient") and data.get("subject") and data.get("body") is not None:
            email_to = data["recipient"]
            subject = data["subject"]
            body = data["body"]

            # https://docs.djangoproject.com/en/4.1/topics/email/
            send_mail(subject=subject,message=body,from_email=email_from,recipient_list=[email_to],fail_silently=False)
            return HttpResponseRedirect(reverse('ehr:index'))
    else:
        return HttpResponse('This endpoint only supports POST requests.', status=400)
    