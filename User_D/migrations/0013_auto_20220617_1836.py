# Generated by Django 2.0 on 2022-06-17 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0012_testing'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='Upload_Count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='user_data',
            name='Upload_limit',
            field=models.IntegerField(default=15, null=True),
        ),
    ]