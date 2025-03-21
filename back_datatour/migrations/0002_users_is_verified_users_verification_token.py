# Generated by Django 5.1.7 on 2025-03-10 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("back_datatour", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="users",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="users",
            name="verification_token",
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
