# Generated by Django 2.2.1 on 2020-02-06 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_auto_20200205_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='attendance_course_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
