# Generated by Django 2.2 on 2020-10-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_auto_20201006_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignments',
            name='end_Date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
