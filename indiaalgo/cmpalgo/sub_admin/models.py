from django.db import models

# Create your models here.

import uuid

from django.utils import timezone
class sub_adminDT(models.Model):
   subadmin_id = models.CharField(max_length=8, unique=True, default=uuid.uuid4().hex[:8])
 #   user_id = models.IntegerField(verbose_name="user_id",  unique=True, primary_key=True)
   subadmin_name_first = models.CharField(max_length=50, blank=True, null=True)
   subadmin_name_last = models.CharField(max_length=50, blank=True, null=True)
   subadmin_email = models.EmailField(blank=True, null=True)
   subadmin_password = models.CharField(max_length=50,blank=True, null=True)
   subadmin_phone_number = models.CharField(max_length=15,blank=True, null=True)
   subadmin_verify_code = models.CharField(max_length=15,blank=True, null=True)
 #  subadmin__status = models.CharField(max_length=15,blank=True, null=True)  
    # subadmin_date_joined	= models.DateTimeField(verbose_name='date joined', default=None)
    # subadmin__last_login= models.DateTimeField(verbose_name='last login',default=None)
    # subadmin__is_staff= models.BooleanField(default=False)    
    
    
    
    
    