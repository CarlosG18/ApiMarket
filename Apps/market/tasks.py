# Create your tasks here
from celery import shared_task
from .models import Alerts

@shared_task
def alarm_stock(stock, type_alarm):
    """
        verifica se o estoque esta no limite e cria um alerta
    """
    if type_alarm == "sup":
        alerta_max = Alerts(stock=stock, alert_type='2', message=f"O estoque[{stock.id}] já esta com o limite maximo para este produto!")
        alerta_max.save()
    
    if type_alarm == "inf":
        alerta_min = Alerts(stock=stock, alert_type='1', message=f"O estoque[{stock.id}] possui menos de 10 unidades!")
        alerta_min.save()