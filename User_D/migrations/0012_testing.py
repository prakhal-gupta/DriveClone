# Generated by Django 2.0 on 2022-06-16 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_D', '0011_auto_20220616_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='testing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.FileField(blank=True, null=True, upload_to='testing_files/')),
            ],
        ),
    ]
