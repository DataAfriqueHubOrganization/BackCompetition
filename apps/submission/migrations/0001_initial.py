# Generated by Django 4.2.20 on 2025-04-30 00:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("competition", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Leaderboard",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "private_score",
                    models.DecimalField(decimal_places=10, max_digits=20),
                ),
                ("public_score", models.DecimalField(decimal_places=10, max_digits=20)),
                ("rank", models.PositiveIntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("file", models.FileField(upload_to="static/submissions/")),
                ("score", models.FloatField(blank=True, null=True)),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="competition.challenge",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
