# Generated by Django 5.2.3 on 2025-06-29 19:07

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Contact",
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
                ("email", models.EmailField(max_length=254, unique=True)),
                ("country", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("street", models.CharField(max_length=100)),
                ("house_number", models.CharField(max_length=10)),
            ],
            options={
                "verbose_name": "Контакт",
                "verbose_name_plural": "Контакты",
            },
        ),
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
                ("name", models.CharField(max_length=100)),
                ("model", models.CharField(max_length=100)),
                ("release_date", models.DateField()),
            ],
            options={
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
            },
        ),
        migrations.CreateModel(
            name="NetworkNode",
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
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "node_type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Завод"),
                            (1, "Розничная сеть"),
                            (2, "Индивидуальный предприниматель"),
                        ]
                    ),
                ),
                (
                    "debt",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "contact",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="core.contact"
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="children",
                        to="core.networknode",
                    ),
                ),
                ("products", models.ManyToManyField(to="core.product")),
            ],
            options={
                "verbose_name": "Элемент сети",
                "verbose_name_plural": "Элементы сети",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="Employee",
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
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "network_node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.networknode",
                    ),
                ),
            ],
            options={
                "verbose_name": "Сотрудник",
                "verbose_name_plural": "Сотрудники",
            },
        ),
    ]
