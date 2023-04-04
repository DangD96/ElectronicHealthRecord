from django.contrib.auth.models import User
from django.db import models
from django.core import validators

# Create your models here.
class Patient(models.Model):
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    age = models.IntegerField(validators=[validators.MinValueValidator(5),validators.MaxValueValidator(90)], null=True)
    photo = models.ImageField(upload_to='images/', blank=True, null=True) # saves to MEDIA_ROOT/upload_to
    email = models.EmailField(null=True, blank=True)

class Doctor(models.Model):
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) # To reverse from User, use lowercase name of the class
    assigned_patients = models.ManyToManyField(Patient, related_name='responsible_providers', blank=True)
    SORT_CHOICES = [
        ('Default', 'Default'),
        ('First Name', 'First Name'),
        ('Last Name', 'Last Name'),
        ('Age', "Age")
    ]
    sort_preference = models.CharField(max_length=10, choices=SORT_CHOICES, default='Default')

class Medication(models.Model):
    patient = models.ManyToManyField(Patient, related_name='meds')
    name = models.CharField(max_length=100, default='')
    dose = models.IntegerField(validators=[validators.MinValueValidator(0),validators.MaxValueValidator(9000)], null=True)
    dose_units = models.CharField(max_length=8, default='')

    # Serialize to send via HTTP
    def serialize(self):
        return {
            "name": self.name,
            "dose": self.dose,
            "doseUnits": self.dose_units
        }

class Message(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='received_messages', null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='sent_messages', null=True)
    content = models.CharField(max_length=200, default='')
    instant = models.DateTimeField(auto_now_add=True, null=True)
