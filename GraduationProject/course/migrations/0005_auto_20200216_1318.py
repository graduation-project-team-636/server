# Generated by Django 2.2.1 on 2020-02-16 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20200214_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_attendance',
            field=models.IntegerField(default=0),
        ),
    ]