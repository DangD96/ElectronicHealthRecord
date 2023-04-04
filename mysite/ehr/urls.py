from django.urls import path
from . import views

app_name = 'ehr'

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path('patient/<int:id>', views.patient_view, name='patient'),
    path('create', views.new_patient, name='new_patient'),

    # API routes
    # Set sorting preference
    path('sort', views.set_sort_method, name='set_sort'),

    # Get sorting preference
    path('preference', views.get_sort_method, name='get_sort'),
    
    # Save patient meds
    path('save_meds/<int:id>', views.save_patient_meds, name='save_meds'),

    # Get patient meds
    path('get_meds/<int:id>', views.get_patient_meds, name='get_meds'),

    # Send email to patient
    path('email', views.send_email, name='email')
]