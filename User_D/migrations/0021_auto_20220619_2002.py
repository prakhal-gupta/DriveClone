# Generated by Django 2.0 on 2022-06-19 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0020_uploaded_files_file_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uploaded_files',
            old_name='file_size',
            new_name='Size_kb',
        ),
    ]