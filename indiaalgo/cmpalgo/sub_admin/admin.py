from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(sub_adminDT)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in sub_adminDT._meta.fields] 