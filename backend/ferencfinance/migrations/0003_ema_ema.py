# Generated by Django 4.1.3 on 2023-12-21 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferencfinance', '0002_stock_startdate_alter_ema_xirr'),
    ]

    operations = [
        migrations.AddField(
            model_name='ema',
            name='ema',
            field=models.JSONField(default=None),
            preserve_default=False,
        ),
    ]