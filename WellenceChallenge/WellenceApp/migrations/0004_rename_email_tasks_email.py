# Generated by Django 5.1 on 2024-08-17 17:18

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("WellenceApp", "0003_alter_tasks_email"),
    ]

    operations = [
        migrations.RenameField(
            model_name="tasks",
            old_name="Email",
            new_name="email",
        ),
    ]
