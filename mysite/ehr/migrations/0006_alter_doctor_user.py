# Generated by Django 4.1.5 on 2023-03-08 02:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ehr', '0005_alter_doctor_assigned_patients_alter_doctor_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
