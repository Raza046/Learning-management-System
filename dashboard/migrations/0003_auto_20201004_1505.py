# Generated by Django 2.2 on 2020-10-04 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignments',
            name='end_Date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='assignments',
            name='end_Time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='assignments',
            name='start_Date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='assignments',
            name='start_Time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
