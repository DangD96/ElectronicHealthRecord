# Generated by Django 4.1.5 on 2023-03-11 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0015_alter_patient_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='assigned_patients',
            field=models.ManyToManyField(blank=True, related_name='responsible_providers', to='ehr.patient'),
        ),
    ]
