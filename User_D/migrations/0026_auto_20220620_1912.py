# Generated by Django 2.0 on 2022-06-20 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0025_uploaded_files_default_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploaded_files',
            name='Default_img',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
