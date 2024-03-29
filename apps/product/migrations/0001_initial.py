# Generated by Django 4.1.7 on 2023-03-03 14:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("logo", models.URLField(blank=True, null=True)),
                ("rotate_duration", models.FloatField(null=True)),
            ],
        ),
    ]
