# Generated by Django 5.1.7 on 2025-03-25 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("back_datatour", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="dataset",
            name="dataset_url",
        ),
        migrations.AddField(
            model_name="dataset",
            name="dataset_submission",
            field=models.FileField(
                default="static/datasets/default_file.csv",
                upload_to="static/dataset_submission/",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dataset",
            name="dataset_test",
            field=models.FileField(
                default="static/datasets/default_file.csv",
                upload_to="static/dataset_test/",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="dataset",
            name="dataset_train",
            field=models.FileField(
                default="static/datasets/default_file.csv",
                upload_to="static/dataset_train/",
            ),
            preserve_default=False,
        ),
    ]
