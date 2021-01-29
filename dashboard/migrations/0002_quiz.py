# Generated by Django 2.2 on 2020-10-04 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Section', models.CharField(max_length=10, null=True)),
                ('QuestionAnswers', models.CharField(max_length=1000, null=True)),
                ('files', models.FileField(upload_to='')),
                ('Course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='CAQuiz', to='dashboard.Course')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='TeaQuiz', to='dashboard.Teacher')),
            ],
            options={
                'verbose_name': 'Quiz',
            },
        ),
    ]
