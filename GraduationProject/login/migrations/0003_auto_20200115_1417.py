# Generated by Django 2.2.1 on 2020-01-15 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20200111_2140'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['reg_time'], 'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.RenameField(
            model_name='user',
            old_name='c_time',
            new_name='reg_time',
        ),
    ]
