# Generated by Django 2.0 on 2022-06-19 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0022_auto_20220619_2009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploaded_files',
            name='Size_kb',
        ),
        migrations.AddField(
            model_name='uploaded_files',
            name='Size_mb',
            field=models.IntegerField(default=0, null=True),
        ),
    ]