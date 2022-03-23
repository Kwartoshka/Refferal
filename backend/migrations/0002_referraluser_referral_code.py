# Generated by Django 4.0.3 on 2022-03-23 15:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='referraluser',
            name='referral_code',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(100000), django.core.validators.MaxValueValidator(999999)]),
        ),
    ]
