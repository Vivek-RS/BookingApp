# Generated by Django 4.2.7 on 2023-12-10 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_specilisation_doctor_specialization'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='adress',
            new_name='address',
        ),
    ]
