# Generated by Django 5.1 on 2024-08-27 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WellenceApp', '0007_alter_tasks_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='task',
            field=models.CharField(max_length=255),
        ),
    ]
