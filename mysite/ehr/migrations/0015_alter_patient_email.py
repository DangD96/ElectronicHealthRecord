# Generated by Django 4.1.5 on 2023-03-11 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0014_delete_procedure_message_content_message_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
