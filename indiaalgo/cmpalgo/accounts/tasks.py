from celery import shared_task
from .models import BrokerAccount, Trade
from .views import initialize_connection

@shared_task
def check_trades():
    accounts = BrokerAccount.objects.all()
    for account in accounts:
        obj, refreshToken = initialize_connection(account)
        if obj:
            # Add your trading logic here
            pass

# Schedule the task periodically
