"""
URL configuration for cmpalgo project.

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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
# from sub_admin import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    ###################  other file urls ##################################   
    path('accounts/',include('accounts.urls')), 
    path('subadmin/',include('sub_admin.urls')),
  
    ##################  myapi views url ####################################
    
    
    
    
    ##################### Admin Api url ##########################    
    path('admin_login/', views.admin_login,name='admin_login'),
    path('logoutAdmin/', views.logoutAdmin,name='logoutAdmin'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    path('group_list/', views.group_list, name='group_list' ),
    path('create_group/', views.create_group, name='create_group' ),
    path('update_group/<int:group_id>/', views.update_group, name='update_group'),
    path('delete_group/<int:group_id>/', views.delete_group, name='delete_group'),
    
    path('strategy_list/', views.strategy_list, name='strategy_list' ),
    path('create_strategy/', views.create_strategy, name='create_strategy' ),
    path('update_strategy/<int:strategy_id>/', views.update_strategy, name='update_strategy'),
    path('delete_strategy/<int:strategy_id>/', views.delete_strategy, name='delete_strategy'),

  
    path('order/', views.order, name='order'),
    # path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    # path('admin_message/', views.admin_message, name='admin_message'),
    path('admin_help_center/', views.admin_help_center, name="admin_help_center"),
    # path('admin_signals/',views.admin_signals, name='admin_signals'),
    path('Creat_client_api/', views.Creat_client_api, name='Creat_client_api'),
    path('place_order/', views.place_order, name='place_order'),
  #  path('symbol_price/', views.symbol_price_view, name='symbol_price'),
    path('Live_admin_message/', views.Live_admin_message, name='Live_admin_message'),
    
    
    path('fetch_and_save_data/', views.fetch_and_save_data, name='fetch_and_save_data'),
    path('client_thistory/',views.client_thistory,name='client_thistory'),
    # path('place-order-view/', views.place_order_view, name='place_order_view'), 
    # path('fetch-symbol-token/<str:symbol>/', views.fetch_symbol_token, name='fetch_symbol_token'),
    path('fetch_and_update_symbols/', views.fetch_and_update_symbols, name='fetch_and_update_symbols'),    
    

   

 
#####################################################################################################
    path('edit/<str:clint_id>/', views.edit_client, name='edit_client'),
    path('client/', views.client_detail, name='client_detail'), 
    
    path('get-symbols/', views.get_symbols, name='get_symbols'),
    path('get-symbol-price/', views.get_symbol_price, name='get_symbol_price'),
    path('Settings/', views.Settings, name='Settings'),
    # path('fetch-instrument-list/', views.fetch_instrument_list, name='fetch_instrument_list'),
    # path('instrument-list/', views.show_instrument_list, name='instrument_list'),
    path('fetch-option-chain/', views.fetch_option_chain, name='fetch_option_chain'),

    
    path('fetch_all_symbol/', views.fetch_all_symbol, name='fetch_all_symbol'),
    path('delete_symbol_to_database/', views.delete_symbol_to_database, name='delete_symbol_to_database'),
    
    # ------------------------------ client url-------------------------------------------
    
    path('', views.client_login, name='client_login' ),
    path('client_logout/', views.client_logout, name='client_logout' ),
    path('client_registration/', views.client_registration, name='admin_client_registration' ),
    
    path('dashbord/', views.client_dashbord, name="client_dashbord" ),
    path('signals/', views.client_signals, name="client_signals" ),
    path('tradingstatus/', views.client_status, name="client_status" ),
    # path('get-symbols/<int:group_id>/', views.get_s, name='get_symbols'),
    path('update-signals/', views.update_signals, name='update_signals'),
    path('order_place/', views.order_place, name='order_place'),
    ###################  other file urls ##################################

    
    path('redirect-to-smartapi-login/', views.redirect_to_smartapi_login, name='redirect_to_smartapi_login'),
    path('handle-smartapi-redirect/', views.handle_smartapi_redirect, name='handle_smartapi_redirect'),  # http://127.0.0.1:8000/handle-smartapi-redirect/
  
    path('off/', views.off, name='off'),
    
    path('place-order/', views.place_order, name='place-order'),
    path('order-success/', views.order_success, name='order-success'),
    path('order-failed/', views.order_failed, name='order-failed'),
    
    path('demo_Live_admin_message/', views.demo_Live_admin_message, name='demo_Live_admin_message'),
    path('place_sl_market_order/', views.place_sl_market_order, name='place_sl_market_order'),
    path('place_sl_limit_order/', views.place_sl_limit_order, name='place_sl_limit_order'),
    path('receive-trade/', views.receive_trade, name='receive_trade'),
    path('trades/', views.trade_list, name='trade_list'),
    path('get_symbol_token/', views.get_symbol_token, name='get_symbol_token'),
    
    path('trade-history/', views.trade_history, name='trade_history'),
    path('home/', views.homes, name='homes'),
    path('send-notification/', views.send_notification, name='send_notification'),
    path('get-notifications/', views.get_notifications, name='get_notifications'),
    
    path('reset/password/', views.Reset_Password, name='reset_password'),
    path('accept_terms/', views.Accept_Terms, name='accept_terms'),
    # path('receive-trade/', views.receive_trade, name='receive_trade'),
    # path('trades/', views.trade_list, name='trade_list'),
    # path('fetch_live_data/', views.fetch_live_data, name='fetch_live_data'),
    # path('live_chart/', views.live_chart, name='live_chart'),
    
    # path('place_ordermt4/', views.place_ordermt4, name='place_ordermt4'),
    # path('dash/', views.dash, name='dash'),
    path('test_order/', views.test_order, name='test_order'),  
    path('client_trade_history/', views.client_trade_history, name='client_trade_history'),  
    # path('send-message/', views.send_message_form, name='send_message_form'),
    # path('send-message-action/', views.send_message_to_all_clients, name='send_message_to_all_clients'),
    # path('telegram-webhook/', views.telegram_webhook, name='telegram_webhook'),
    path('client_help_center/', views.client_help_center, name='client_help_center'),
    
    
    # path('demo/', views.all_trades_history, name='all_trades_history'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
