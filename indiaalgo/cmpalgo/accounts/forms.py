# # forms.py

# from django import forms
# from .models import GROUP, SYMBOL

# class GroupForm(forms.ModelForm):
#     symbols = forms.ModelMultipleChoiceField(
#         queryset=SYMBOL.objects.all(), 
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
#     )

#     class Meta:
#         model = GROUP
#         fields = ['GROUP', 'symbols']
        
        
        
# # forms.py

# from django import forms

# class OrderForm(forms.Form):
#     VARIETY_CHOICES = [
#         ('NORMAL', 'Normal Order (Regular)'),
#         ('STOPLOSS', 'Stop loss order'),
#         ('AMO', 'After Market Order'),
#         ('ROBO', 'ROBO (Bracket Order)'),
#     ]
#     TRANSACTION_TYPE_CHOICES = [
#         ('BUY', 'Buy'),
#         ('SELL', 'Sell'),
#     ]
#     ORDER_TYPE_CHOICES = [
#         ('MARKET', 'Market Order (MKT)'),
#         ('LIMIT', 'Limit Order (L)'),
#         ('STOPLOSS_LIMIT', 'Stop Loss Limit Order (SL)'),
#         ('STOPLOSS_MARKET', 'Stop Loss Market Order (SL-M)'),
#     ]
#     PRODUCT_TYPE_CHOICES = [
#         ('DELIVERY', 'Cash & Carry for equity (CNC)'),
#         ('CARRYFORWARD', 'Normal for futures and options (NRML)'),
#         ('MARGIN', 'Margin Delivery'),
#         ('INTRADAY', 'Margin Intraday Squareoff (MIS)'),
#         ('BO', 'Bracket Order (Only for ROBO)'),
#     ]
#     DURATION_CHOICES = [
#         ('DAY', 'Regular Order'),
#         ('IOC', 'Immediate or Cancel'),
#     ]
#     EXCHANGE_CHOICES = [
#         ('BSE', 'BSE Equity'),
#         ('NSE', 'NSE Equity'),
#         ('NFO', 'NSE Future and Options'),
#         ('MCX', 'MCX Commodity'),
#         ('BFO', 'BSE Futures and Options'),
#         ('CDS', 'Currency Derivate Segment'),
#     ]
    
#     variety = forms.ChoiceField(choices=VARIETY_CHOICES)
#     transactiontype = forms.ChoiceField(choices=TRANSACTION_TYPE_CHOICES)
#     ordertype = forms.ChoiceField(choices=ORDER_TYPE_CHOICES)
#     producttype = forms.ChoiceField(choices=PRODUCT_TYPE_CHOICES)
#     duration = forms.ChoiceField(choices=DURATION_CHOICES)
#     exchange = forms.ChoiceField(choices=EXCHANGE_CHOICES)
#     tradingsymbol = forms.CharField(max_length=100)
#     symboltoken = forms.CharField(max_length=100)
#     quantity = forms.IntegerField()
#     price = forms.DecimalField(decimal_places=2, required=False)
#     triggerprice = forms.DecimalField(decimal_places=2, required=False)
#     squareoff = forms.DecimalField(decimal_places=2, required=False)
#     stoploss = forms.DecimalField(decimal_places=2, required=False)
#     trailingStopLoss = forms.DecimalField(decimal_places=2, required=False)
#     disclosedquantity = forms.IntegerField(required=False)
#     ordertag = forms.CharField(max_length=100, required=False)
        

# forms.py

from django import forms
from .models import GROUP, SYMBOL,ind_clientDT

# class GroupForm(forms.ModelForm):
#     symbols = forms.ModelMultipleChoiceField(
#     #    queryset=SYMBOL.objects.all(), 
#         queryset=SYMBOL.objects.values('SYMBOL').distinct(), 
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
#     )

#     class Meta:
#         model = GROUP
#         fields = ['GROUP', 'min_quantity','max_quantity','symbols']
        

from django import forms
from django.forms import ModelForm
from django.db.models import Subquery, OuterRef, Min
from .models import SYMBOL, GROUP

class GroupForm(ModelForm):
    # Get distinct SYMBOL instances based on the SYMBOL field
    distinct_symbols = SYMBOL.objects.filter(
        id__in=Subquery(
            SYMBOL.objects.values('SYMBOL').annotate(
                min_id=Min('id')
            ).values('min_id')
        )
    )

    symbols = forms.ModelMultipleChoiceField(
        queryset=distinct_symbols,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
    )

    class Meta:
        model = GROUP
        fields = ['GROUP', 'min_quantity', 'max_quantity', 'symbols']        
        
# forms.py

from django import forms

class OrderForm(forms.Form):
    VARIETY_CHOICES = [
        ('NORMAL', 'Normal Order (Regular)'),
        ('STOPLOSS', 'Stop loss order'),
        ('AMO', 'After Market Order'),
        ('ROBO', 'ROBO (Bracket Order)'),
    ]
    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    ]
    ORDER_TYPE_CHOICES = [
        ('MARKET', 'Market Order (MKT)'),
        ('LIMIT', 'Limit Order (L)'),
        ('STOPLOSS_LIMIT', 'Stop Loss Limit Order (SL)'),
        ('STOPLOSS_MARKET', 'Stop Loss Market Order (SL-M)'),
    ]
    PRODUCT_TYPE_CHOICES = [
        ('DELIVERY', 'Cash & Carry for equity (CNC)'),
        ('CARRYFORWARD', 'Normal for futures and options (NRML)'),
        ('MARGIN', 'Margin Delivery'),
        ('INTRADAY', 'Margin Intraday Squareoff (MIS)'),
        ('BO', 'Bracket Order (Only for ROBO)'),
    ]
    DURATION_CHOICES = [
        ('DAY', 'Regular Order'),
        ('IOC', 'Immediate or Cancel'),
    ]
    EXCHANGE_CHOICES = [
        ('BSE', 'BSE Equity'),
        ('NSE', 'NSE Equity'),
        ('NFO', 'NSE Future and Options'),
        ('MCX', 'MCX Commodity'),
        ('BFO', 'BSE Futures and Options'),
        ('CDS', 'Currency Derivate Segment'),
    ]
    
    variety = forms.ChoiceField(choices=VARIETY_CHOICES)
    transactiontype = forms.ChoiceField(choices=TRANSACTION_TYPE_CHOICES)
    ordertype = forms.ChoiceField(choices=ORDER_TYPE_CHOICES)
    producttype = forms.ChoiceField(choices=PRODUCT_TYPE_CHOICES)
    duration = forms.ChoiceField(choices=DURATION_CHOICES)
    exchange = forms.ChoiceField(choices=EXCHANGE_CHOICES)
    tradingsymbol = forms.CharField(max_length=100)
    symboltoken = forms.CharField(max_length=100)
    quantity = forms.IntegerField()
    price = forms.DecimalField(decimal_places=2, required=False)
    triggerprice = forms.DecimalField(decimal_places=2, required=False)
    squareoff = forms.DecimalField(decimal_places=2, required=False)
    stoploss = forms.DecimalField(decimal_places=2, required=False)
    trailingStopLoss = forms.DecimalField(decimal_places=2, required=False)
    disclosedquantity = forms.IntegerField(required=False)
    ordertag = forms.CharField(max_length=100, required=False)
    
    
    
from .models import HelpMessage

class HelpMessageForm(forms.ModelForm):
    class Meta:
        model = HelpMessage
        fields = ['client_name', 'message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'cols': 40,
                'placeholder': 'Enter your message here...',
                'class': 'form-control',
            }),
        }
            
    
# class ind_clientDTForm(forms.ModelForm):
#     class Meta:
#         model = ind_clientDT
#         fields = ['id','clint_id','clint_name_first','clint_name_last','clint_email','clint_password','clint_phone_number','clint_verify_code','clint_date_joined','clint_last_login','clint_is_staff','clint_status','clint_plane','client_Group','broker','api_key','client_id','password','secret_key','created_at','updated_at']
class ind_clientDTForm(forms.ModelForm):
    class Meta:
        model = ind_clientDT
        exclude = ['created_at', 'updated_at']
        
        

from django import forms
from .models import Strategy

class StrategyForm(forms.ModelForm):
    class Meta:
        model = Strategy
        fields = ['Strategy']  # Specify which fields from the Strategy model should be included in the form

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation logic if needed
        return cleaned_data


from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message']



 


 
 
        

        
        