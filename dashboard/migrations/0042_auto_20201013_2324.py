# Generated by Django 2.2 on 2020-10-13 18:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0041_auto_20201013_0123'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mcqanswers',
            old_name='Answers1',
            new_name='Answers',
        ),
    ]
