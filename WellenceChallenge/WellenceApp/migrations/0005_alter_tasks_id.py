# Generated by Django 5.1 on 2024-08-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WellenceApp', '0004_rename_email_tasks_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
