"""
URL configuration for indalgo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.client_login, name='client_login' ),
    path('client_registration/', views.client_registration, name='client_registration' ),
    
    path('home/', views.client_dashbord, name="client_home" ),
    path('client_signals/', views.client_signals, name="client_signals" ),
    path('client_status/', views.client_status, name="client_status" ),
    path('get-symbols/<int:group_id>/', views.get_s, name='get_symbols'),
    path('update-signals/', views.update_signals, name='update_signals'),
    # path('get_historic_data/', views.get_historic_data, name='get_historic_data'),

   
    # path('fetch_local_order_history/', views.fetch_local_order_history, name='fetch_local_order_history'),

    ###############################################################################################
    # path('cancel_order/', views.cancel_order, name='cancel_order'),
    # path('display_order/', views.display_order, name='display_order'),

    # path('trade_history_view/', views.trade_history_view, name='trade_history_view'),
    

    path('redirect-to-smartapi-login/', views.redirect_to_smartapi_login, name='redirect_to_smartapi_login'),
    path('handle-smartapi-redirect/', views.handle_smartapi_redirect, name='handle_smartapi_redirect'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('place-order/', views.place_order, name='place_order'),
    path('off/', views.off, name='off'),
    
    
    path('receive-trade/', views.receive_trade, name='receive_trade'),
    path('trades/', views.trade_list, name='trade_list'),
]
