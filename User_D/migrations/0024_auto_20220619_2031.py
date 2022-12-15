# Generated by Django 2.0 on 2022-06-19 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0023_auto_20220619_2024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploaded_files',
            name='Size_mb',
        ),
        migrations.AddField(
            model_name='uploaded_files',
            name='Size_kb',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='Used_space_mb',
            field=models.CharField(default=0, max_length=30, null=True),
        ),
    ]