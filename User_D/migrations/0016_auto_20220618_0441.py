# Generated by Django 2.0 on 2022-06-18 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0015_auto_20220618_0436'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_data',
            old_name='Used_space',
            new_name='Used_space_mb',
        ),
    ]
