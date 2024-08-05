


# ======================================================================
#                     client admin.py
# ======================================================================
from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(ind_clientDT)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in ind_clientDT._meta.fields]      


@admin.register(SYMBOL)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in SYMBOL._meta.fields]   


@admin.register(ClientSignal)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in ClientSignal._meta.fields]   

@admin.register(Client_SYMBOL_QTY)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Client_SYMBOL_QTY._meta.fields]         



@admin.register(BROKERS)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in BROKERS._meta.fields]  


# @admin.register(GROUP)
# class ProductAdmin(admin.ModelAdmin):
   
#     list_display = [field.name for field in GROUP._meta.fields]           

from django.contrib import admin
from .models import GROUP, SYMBOL

class GroupAdmin(admin.ModelAdmin):
    list_display = ('GROUP', 'min_quantity', 'max_quantity', 'created_at')  # Add all fields here
    search_fields = ('GROUP',)
    filter_horizontal = ('symbols',)
    
admin.site.register(GROUP, GroupAdmin)
# class SymbolAdmin(admin.ModelAdmin):
#     list_display = ('SYMBOL', 'created_at')
#     search_fields = ('SYMBOL',)


# admin.site.register(SYMBOL, SymbolAdmin)

@admin.register(OrderAngelOne)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in OrderAngelOne._meta.fields]     



# ==============================================================================

from .models import Trade,ClientStatus

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('trade_type', 'symbol', 'price','lot_size', 'timestamp','status','clint_id','order_id')
    
   
    
    
@admin.register(ClientStatus)
class ClientStatusAdmin(admin.ModelAdmin):
    list_display = ('sub_admin_id', 'clint_id', 'name','time', 'service_name','quantity','strategy','trading','ip_address','updated_by')
    
