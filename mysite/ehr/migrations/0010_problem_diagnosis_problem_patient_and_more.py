# Generated by Django 4.1.5 on 2023-03-09 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0009_vital_diastolic_bp_vital_patient_vital_pulse_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='diagnosis',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='patient',
            field=models.ManyToManyField(related_name='problems', to='ehr.patient'),
        ),
        migrations.AlterField(
            model_name='vital',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vitals', to='ehr.patient'),
        ),
    ]
