# Generated by Django 2.2.1 on 2020-02-07 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course_course_attendance_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='video_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
