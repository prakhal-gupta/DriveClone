# Generated by Django 2.0 on 2022-06-18 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0014_testing_file_size'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_data',
            old_name='Upload_Count',
            new_name='Used_space',
        ),
        migrations.RemoveField(
            model_name='user_data',
            name='Upload_limit',
        ),
        migrations.AddField(
            model_name='testing',
            name='Uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='uploaded_files',
            name='Uploaded_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='user_data',
            name='Upload_limit_mb',
            field=models.IntegerField(default=500, null=True),
        ),
    ]