# Generated by Django 2.2 on 2020-10-05 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20201005_1638'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendence',
            name='status',
        ),
    ]
