# Generated by Django 4.1.3 on 2024-01-10 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferencfinance', '0003_ema_ema'),
    ]

    operations = [
        migrations.AddField(
            model_name='ema',
            name='cashflows',
            field=models.JSONField(null=True),
        ),
    ]