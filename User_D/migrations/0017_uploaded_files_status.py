# Generated by Django 2.0 on 2022-06-18 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0016_auto_20220618_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploaded_files',
            name='Status',
            field=models.CharField(default='Available', max_length=20, null=True),
        ),
    ]
