# Generated by Django 4.2.12 on 2024-08-17 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Accounts",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Tasks",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task", models.CharField(max_length=255)),
                ("due_by", models.DateTimeField()),
                (
                    "priority",
                    models.IntegerField(
                        choices=[(1, "Low"), (2, "Medium"), (3, "High")], default=1
                    ),
                ),
                ("is_urgent", models.BooleanField(default=False)),
                (
                    "userEmail",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="WellenceApp.accounts",
                    ),
                ),
            ],
        ),
    ]
