# Generated by Django 2.0 on 2022-06-23 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0031_uploaded_folder_parent_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploaded_folder',
            name='Parent_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='User_D.Uploaded_folder'),
        ),
    ]
