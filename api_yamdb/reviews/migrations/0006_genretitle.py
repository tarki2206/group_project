# Generated by Django 3.2 on 2023-08-18 08:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reviews", "0005_auto_20230818_1030"),
    ]

    operations = [
        migrations.CreateModel(
            name="GenreTitle",
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
                (
                    "genre",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reviews.genre",
                    ),
                ),
                (
                    "title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="reviews.title",
                    ),
                ),
            ],
        ),
    ]
