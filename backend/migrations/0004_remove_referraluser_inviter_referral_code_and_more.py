# Generated by Django 4.0.3 on 2022-03-23 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_referraluser_inviter_referral_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='referraluser',
            name='inviter_referral_code',
        ),
        migrations.AddField(
            model_name='referraluser',
            name='inviter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.referraluser'),
        ),
    ]
