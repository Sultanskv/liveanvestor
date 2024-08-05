


# ================================= client models====================================
from django.db import models
from django.core.validators import MinValueValidator
import uuid

from django.utils import timezone

     
class SYMBOL(models.Model): 
    SYMBOL = models.CharField(max_length=50)
    SYMBOL_order = models.CharField(max_length=50 ,blank=True, null=True)
    symbol_token = models.CharField(max_length=50 , blank=True, null=True)
    expiry = models.DateField(null=True, blank=True)
    strike = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    lotsize = models.IntegerField(null=True, blank=True)
    instrumenttype = models.CharField(max_length=20,null=True, blank=True)
    exch_seg = models.CharField(max_length=10,null=True, blank=True)
    tick_size = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
 

    def __str__(self):
        return self.SYMBOL
  #  " https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json " symbol list angel one 


# models.py
from django.db import models

class Instrument(models.Model):
    exchange_token = models.CharField(max_length=20)
    tradingsymbol = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    expiry = models.CharField(max_length=20, blank=True, null=True)
    strike = models.FloatField(blank=True, null=True)
    tick_size = models.FloatField()
    lot_size = models.IntegerField()
    instrument_type = models.CharField(max_length=10)
    
    def __str__(self):
        return self.tradingsymbol


from django.db import models

# class Symbol(models.Model):
#     token = models.CharField(max_length=50)
#     symbol = models.CharField(max_length=50)
#     name = models.CharField(max_length=50)
#     expiry = models.DateField()
#     strike = models.DecimalField(max_digits=10, decimal_places=2)
#     lotsize = models.IntegerField()
#     instrumenttype = models.CharField(max_length=20)
#     exch_seg = models.CharField(max_length=10)
#     tick_size = models.DecimalField(max_digits=5, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.symbol



class ClientSignal(models.Model):
    user = models.CharField(max_length=50, blank=True, null=True)
    admin = models.CharField(max_length=50, blank=True, null=True)
    client_id = models.CharField(max_length=50, blank=True, null=True)
    message_id = models.CharField(max_length=50, blank=True, null=True)
    ids = models.CharField(max_length=50, blank=True, null=True)
    ENTRY = models.CharField(max_length=50, blank=True, null=True)
    SYMBOL = models.ForeignKey('SYMBOL', on_delete=models.CASCADE, related_name='client_signals')
    TYPE_CHOICES = (
        ('BUY_ENTRY', 'BUY_ENTRY'),
        ('BUY_EXIT', 'BUY_EXIT'),
        ('SELL_ENTRY', 'SELL_ENTRY'),
        ('SELL_EXIT', 'SELL_EXIT'),
    )
    TYPE = models.CharField(max_length=10, choices=TYPE_CHOICES)
    QUANTITY = models.FloatField(null=True, blank=True)
    ENTRY_PRICE = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)
    EXIT_PRICE = models.DecimalField(max_digits=12, decimal_places=5, null=True, blank=True)
    profit_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cumulative_pl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    live_order_id = models.CharField(max_length=90, blank=True, null=True)
   
   
   
# class Client_SYMBOL_QTY(models.Model):
#     client_id = models.CharField(max_length=50, blank=True, null=True)    
#     SYMBOL = models.CharField(max_length=50, blank=True, null=True)
#     QUANTITY = models.FloatField(null=True, blank=True)
#     Order_Type = models.CharField(max_length=50, blank=True, null=True)   
#     Product_Type = models.CharField(max_length=50, blank=True, null=True)  
#     Strategy = models.CharField(max_length=50, blank=True, null=True)   
#     trade = models.CharField(max_length=50, blank=True, null=True)   
#     created_at = models.DateTimeField(auto_now_add=True)

class Client_SYMBOL_QTY(models.Model):
    client_id = models.CharField(max_length=50, blank=True, null=True)    
    SYMBOL = models.CharField(max_length=50, blank=True, null=True)
    QUANTITY = models.IntegerField(null=True, blank=True)
    Order_Type = models.CharField(max_length=50, blank=True, null=True)   
    Product_Type = models.CharField(max_length=50, blank=True, null=True)  
    Strategy = models.CharField(max_length=50, blank=True, null=True)   
    trade = models.CharField(max_length=50, blank=True, null=True)   
    created_at = models.DateTimeField(auto_now_add=True)    
 

# class GROUP(models.Model):
#     # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     GROUP = models.CharField(max_length=20)
#     symbols = models.ManyToManyField(SYMBOL, related_name='groups')
#     min_quantity = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
#     max_quantity = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.GROUP      
    

from django.contrib.auth.models import User
from django.db import models

class GROUP(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    GROUP = models.CharField(max_length=20)
    symbols = models.ManyToManyField(SYMBOL, related_name='groups')
    min_quantity = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    max_quantity = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.GROUP
    
    
class Strategy(models.Model):
    Strategy = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True) 
    def __str__(self):
        return self.Strategy    


class BROKERS(models.Model):
    broker_name = models.CharField(max_length=255, null=True)
    def __str__(self):
        return self.broker_name  


class ind_clientDT(models.Model):
    clint_id = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
 #   user_id = models.IntegerField(verbose_name="user_id",  unique=True, primary_key=True)
    clint_name_first = models.CharField(max_length=50, blank=True, null=True)
    clint_name_last = models.CharField(max_length=50, blank=True, null=True)
    clint_email = models.EmailField(blank=True, null=True)
    clint_password = models.CharField(max_length=50,blank=True, null=True)
    clint_phone_number = models.CharField(max_length=15,blank=True, null=True)
    clint_verify_code = models.CharField(max_length=15,blank=True, null=True)
    clint_date_joined	= models.DateTimeField(verbose_name='date joined', default=None)
    clint_last_login= models.DateTimeField(verbose_name='last login',default=None)
    clint_is_staff= models.BooleanField(default=False)    
    clint_status = models.CharField(max_length=15,blank=True, null=True) 

    clint_plane = models.CharField(max_length=15,blank=True, null=True)   

    # client_Group = models.CharField(GROUP , max_length=15,blank=True, null=True)   
    # broker = models.CharField(BROKERS , max_length=255, null=True)

    client_Group = models.ForeignKey(GROUP, on_delete=models.SET_NULL, blank=True, null=True)
    broker = models.ForeignKey(BROKERS, on_delete=models.SET_NULL, blank=True, null=True)
    
    
    api_key = models.CharField(max_length=100, blank=True, null=True)
    client_id = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    secret_key = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    auth_token = models.CharField(max_length=1355, blank=True, null=True)  # Add this field
    feed_token = models.CharField(max_length=1355, blank=True, null=True)  # Add this field
    refresh_token = models.CharField(max_length=1355, blank=True, null=True)  # Add this field

    sub_admin_id = models.CharField(max_length=50, blank=True, null=True)
    
    
     # New fields
    service_name = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    login_date_time = models.DateTimeField(blank=True, null=True)
    strategies = models.CharField(max_length=100, blank=True, null=True)
    Term_condition = models.BooleanField(default=False) 
    telegram_number = models.CharField(max_length=15, blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=15, blank=True, null=True)

'''from django.db import models

class Client(models.Model):
    username = models.CharField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    mobile = models.CharField(max_length=15)
    status = models.BooleanField(default=True)
    is_term = models.BooleanField(default=False)
    new_password = models.CharField(max_length=255)
    login_status = models.BooleanField(default=False)
    user_login = models.BooleanField(default=False)
    expiry_status = models.BooleanField(default=False) 
    end_date = models.DateTimeField(null=True)
    broker = models.CharField(max_length=255, null=True)
    api_key = models.CharField(max_length=255, null=True)
    api_secret = models.CharField(max_length=255, null=True)
    app_id = models.CharField(max_length=255, null=True)
    demat_userid = models.CharField(max_length=255, null=True)
    client_code = models.CharField(max_length=255, null=True)
    api_type = models.CharField(max_length=255, null=True)
    web_url = models.CharField(max_length=255, null=True)
    client_key = models.CharField(max_length=255, null=True)
    signal_execution = models.IntegerField(null=True)
    qty_type = models.IntegerField(null=True)
    overall_fund = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    overall_fund_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    fund_used = models.IntegerField(null=True)

    def __str__(self):
        return self.username     
'''


class HelpMessage(models.Model):
    clint_id = models.ForeignKey('ind_clientDT', to_field='clint_id', on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.clint_id} {self.client_name} at {self.timestamp}'


class OrderAngelOne(models.Model):
    clint = models.CharField(max_length=100)  # Adjust max_length as needed
    symbol = models.CharField(max_length=50)
    tradingsymbol = models.CharField(max_length=50)
    symboltoken = models.CharField(max_length=50)
    transaction_type = models.CharField(max_length=20)
    order_type = models.CharField(max_length=20)
    quantity = models.IntegerField()
    segment_type = models.CharField(max_length=20)
    squareoff = models.DecimalField(max_digits=10, decimal_places=2)
    stoploss = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.order_id} for {self.clint}"
    
    
    
# -------------------------------------------------------------------------------

from django.db import models
class Trade(models.Model):
    TRADE_TYPES = (
        ('Long_Entry', 'Long Entry'),
        ('Long_Exit', 'Long Exit'),
        ('Short_Entry', 'Short Entry'),
        ('Short_Exit', 'Short Exit'),
    )
    TRADE_MODE_CHOICES = [
        ('demo', 'Demo'),
        ('live', 'Live'),
    ]
    
    trade_type = models.CharField(max_length=20, choices=TRADE_TYPES)
    symbol = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    lot_size = models.IntegerField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30,null=True, blank=True)
    clint_id = models.CharField(max_length=30,null=True, blank=True)
    order_id = models.CharField(max_length=30,null=True, blank=True)
    mode = models.CharField(max_length=10, choices=TRADE_MODE_CHOICES, default='demo')
    # Add other necessary fields

    def _str_(self):
        return f"{self.trade_type} {self.symbol} at {self.price}"
     
     
from django.db import models

class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
    
    
class ClientStatus(models.Model):
    sub_admin_id = models.CharField(max_length=50,null=True, blank=True)
    clint_id = models.CharField(max_length=50,null=True, blank=True)
    name = models.CharField(max_length=255,null=True, blank=True)  # 'Name' field as a string
    time = models.DateTimeField(auto_now_add=True)  # 'Time' field as a DateTime field
    service_name = models.CharField(max_length=255,null=True, blank=True)  # 'Service Name' field as a string
    quantity = models.IntegerField(null=True, blank=True)  # 'Quantity' field as an integer
    strategy = models.CharField(max_length=255,null=True, blank=True)  # 'Strategy' field as a string
    trading = models.CharField(max_length=255,null=True, blank=True)  # 'Trading' field as a string
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # 'IP Address' field as an IP address
    updated_by = models.CharField(max_length=255,null=True, blank=True)  # 'UPDATED BY' field as a string

    def _str_(self):
        return f"{self.name} - {self.service_name} ({self.clint_id})"
    
    
    