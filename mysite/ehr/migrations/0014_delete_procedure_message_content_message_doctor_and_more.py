# Generated by Django 4.1.5 on 2023-03-09 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ehr', '0013_alter_allergy_allergen_alter_allergy_reaction_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Procedure',
        ),
        migrations.AddField(
            model_name='message',
            name='content',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='message',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='ehr.doctor'),
        ),
        migrations.AddField(
            model_name='message',
            name='instant',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='ehr.patient'),
        ),
    ]
