import json
import requests
from django.core.management.base import BaseCommand
from accounts.models import SYMBOL
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch symbols from Angel Broking API and populate the SYMBOL model'

    def handle(self, *args, **kwargs):
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        response = requests.get(url)
        data = response.json()
        
        for item in data:
            if item['name'] in ['BANKNIFTY', 'NIFTY', 'FINNIFTY']:
                # Parse the expiry date if it exists
                expiry_date = None
                if item.get('expiry'):
                    try:
                        expiry_date = datetime.strptime(item['expiry'], '%d%b%Y').date()
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(f"Error parsing date: {item['expiry']} - {str(e)}"))
                
                SYMBOL.objects.update_or_create(
                    SYMBOL=item['symbol'],
                    defaults={
                        'SYMBOL_order': item.get('symbol'),
                        'symbol_token': item.get('token'),
                        'expiry': expiry_date,
                        'strike': item.get('strike'),
                        'lotsize': item.get('lotsize'),
                        'instrumenttype': item.get('instrumenttype'),
                        'exch_seg': item.get('exch_seg'),
                        'tick_size': item.get('tick_size')
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved symbols'))