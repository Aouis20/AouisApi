# Generated by Django 4.2 on 2023-06-19 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("Categories", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                ("created_at", models.DateField(auto_now_add=True)),
                ("updated_at", models.DateField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("SOLD", "Sold"),
                            ("FOR_SALE", "For sale"),
                            ("EXCHANGED", "Exchanged"),
                            ("TO_EXCHANGE", "To exchange"),
                            ("REFUNDED", "Refunded"),
                            ("TO_REFUNDED", "to_Refunded"),
                            ("RESERVED", "Reserved"),
                            ("PENDING_PAYMENT", "Pending_payment"),
                            ("NEGOTIATING", "Negotiating"),
                        ],
                        default="FOR_SALE",
                        max_length=255,
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Categories.category",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]