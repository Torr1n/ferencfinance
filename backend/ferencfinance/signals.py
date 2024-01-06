from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from ferencfinance.helpers import (
    calculate_ema,
    generate_signals_and_xirr,
    calculate_profits,
    get_stock_data,
)
import pandas as pd
import json

from ferencfinance.models import EMA, Stock


@receiver(post_save, sender=User, weak=False)
def report_uploaded(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Stock)
def update_stock_data_on_create(sender, instance, created, **kwargs):
    if created:
        for period in range(3, 101):
            data = pd.DataFrame(
                json.loads(instance.data),
                columns=["Date", "Open", "High", "Low", "Close"],
            )
            ema = calculate_ema(data, period)
            data["EMA"] = ema
            emalist = data[["Date", "EMA"]].values.tolist()
            result = generate_signals_and_xirr(data)
            signals, xirr, cash_flows = result
            print(signals)
            if not xirr:
                xirr = 0

            profit = calculate_profits(signals)
            EMA.objects.create(
                stock=instance,
                period=period,
                profit=profit,
                ema=json.dumps(emalist),
                xirr=xirr,
                signals=json.dumps(signals),
            )


@receiver(pre_save, sender=Stock)
def validate_ticker(sender, instance, **kwargs):
    try:
        if instance.startDate:
            instance.data = json.dumps(
                get_stock_data(instance.ticker, instance.startDate)
            )
        else:
            instance.data = json.dumps(get_stock_data(instance.ticker))

    except Exception as e:
        raise ValidationError(f"Invalid ticker: {instance.ticker}, Error: {str(e)}")