# Generated by Django 5.1 on 2024-08-24 07:32

import datetime

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Brand",
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
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="nom"),
                ),
                (
                    "logo",
                    models.ImageField(default=None, null=True, upload_to="", verbose_name="logo"),
                ),
            ],
            options={
                "verbose_name": "marque",
                "verbose_name_plural": "marques",
            },
        ),
        migrations.CreateModel(
            name="Reference",
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
                    "name",
                    models.CharField(db_index=True, default="-", max_length=100, verbose_name="nom"),
                ),
                (
                    "url",
                    models.URLField(
                        db_index=True,
                        default="http://example.com/",
                        max_length=255,
                        verbose_name="lien",
                    ),
                ),
            ],
            options={
                "verbose_name": "référence",
                "verbose_name_plural": "références",
            },
        ),
        migrations.CreateModel(
            name="PaintOwner",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(blank=True, null=True, verbose_name="last login"),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={"unique": "A user with that username already exists."},
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(blank=True, max_length=150, verbose_name="first name"),
                ),
                (
                    "last_name",
                    models.CharField(blank=True, max_length=150, verbose_name="last name"),
                ),
                (
                    "email",
                    models.EmailField(blank=True, max_length=254, verbose_name="email address"),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined"),
                ),
                (
                    "color_theme",
                    models.CharField(
                        choices=[
                            ("auto", "Auto"),
                            ("light", "Light"),
                            ("dark", "Dark"),
                        ],
                        db_index=True,
                        default="auto",
                        max_length=10,
                        verbose_name="Color theme",
                    ),
                ),
                (
                    "display_online",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        verbose_name="Display online status",
                    ),
                ),
                (
                    "email_notifications",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        verbose_name="Receive notifications by email",
                    ),
                ),
                (
                    "solvent",
                    models.CharField(
                        choices=[
                            ("pigments", "pigments"),
                            ("acrylic", "acrylique"),
                            ("enamel", "enamel"),
                            ("lacquer", "laque"),
                        ],
                        db_index=True,
                        max_length=12,
                        null=True,
                        verbose_name="type préféré",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "preferred_brands",
                    models.ManyToManyField(
                        blank=True,
                        to="paint_manager.brand",
                        verbose_name="marques préférées",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Paint",
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
                    "name",
                    models.CharField(db_index=True, max_length=200, verbose_name="nom"),
                ),
                (
                    "sort_name",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        default="",
                        max_length=200,
                        verbose_name="nom pour le tri",
                    ),
                ),
                (
                    "reference",
                    models.CharField(db_index=True, max_length=200, verbose_name="référence"),
                ),
                (
                    "finish",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("matt", "mat"),
                            ("fluo", "fluorescent"),
                            ("gloss", "brillant"),
                            ("transparent", "transparent"),
                            ("metallic", "métallique"),
                            ("satin", "satiné"),
                            ("varnish", "vernis"),
                            ("iridescent", "irisé"),
                        ],
                        db_index=True,
                        default="matt",
                        max_length=12,
                        null=True,
                        verbose_name="finition",
                    ),
                ),
                (
                    "solvent",
                    models.CharField(
                        choices=[
                            ("pigments", "pigments"),
                            ("acrylic", "acrylique"),
                            ("enamel", "enamel"),
                            ("lacquer", "laque"),
                        ],
                        db_index=True,
                        default="pigments",
                        max_length=12,
                        verbose_name="type",
                    ),
                ),
                (
                    "packaging",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("bottle", "pot"),
                            ("spray", "bombe"),
                            ("eye dropper", "compte-goutte"),
                        ],
                        db_index=True,
                        default="bottle",
                        max_length=12,
                        null=True,
                        verbose_name="format",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        blank=True,
                        db_index=True,
                        max_length=20,
                        null=True,
                        verbose_name="taille",
                    ),
                ),
                (
                    "color_r",
                    models.IntegerField(
                        db_index=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(255),
                        ],
                        verbose_name="composante R",
                    ),
                ),
                (
                    "color_g",
                    models.IntegerField(
                        db_index=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(255),
                        ],
                        verbose_name="composante V",
                    ),
                ),
                (
                    "color_b",
                    models.IntegerField(
                        db_index=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(255),
                        ],
                        verbose_name="composante B",
                    ),
                ),
                (
                    "brand",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="paint_manager.brand",
                        verbose_name="marque",
                    ),
                ),
            ],
            options={
                "verbose_name": "peinture",
                "verbose_name_plural": "peintures",
                "ordering": (
                    "sort_reference",
                    "size",
                ),
            },
        ),
        migrations.CreateModel(
            name="RegisteredSimilarPaint",
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
                    "paint_a",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="similar_a",
                        to="paint_manager.paint",
                    ),
                ),
                (
                    "paint_b",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="similar_b",
                        to="paint_manager.paint",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="paint_manager.reference",
                    ),
                ),
            ],
            options={
                "verbose_name": "peintures similaires",
                "verbose_name_plural": "peintures similaires",
            },
        ),
        migrations.CreateModel(
            name="UserPaint",
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
                    "remaining",
                    models.IntegerField(
                        blank=True,
                        db_index=True,
                        default=100,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name="niveau restant",
                    ),
                ),
                (
                    "comment",
                    models.TextField(blank=True, default="", verbose_name="commentaire"),
                ),
                (
                    "buying_date",
                    models.DateField(
                        blank=True,
                        db_index=True,
                        default=datetime.date.today,
                        null=True,
                        verbose_name="date d'achat",
                    ),
                ),
                (
                    "paint",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="paint_manager.paint",
                        verbose_name="peinture",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="utilisateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "peinture en stock",
                "verbose_name_plural": "peintures en stock",
                "ordering": ("paint__sort_name",),
            },
        ),
    ]