# Generated by Django 2.2.1 on 2020-02-28 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20200210_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='extract_down',
            field=models.BooleanField(default=False),
        ),
    ]