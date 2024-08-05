from django.shortcuts import render , HttpResponse , redirect
from .models import *
from django.shortcuts import get_object_or_404


from django.views.decorators.csrf import csrf_protect
from django.utils import timezone    
import datetime
from django.contrib import messages
from cmpalgo import settings
from accounts.models import ind_clientDT
from accounts.forms import ind_clientDTForm
from django.core.mail import send_mail
# Create your views here.
# ===============================================      

from apscheduler.schedulers.background import BackgroundScheduler
from django.db import transaction
from django.utils import timezone
scheduler = BackgroundScheduler()




def admin_change_password(request):
    if request.method == 'POST':
        current_password = request.POST['currentpassword']
        new_password = request.POST['newpassword']
        confirm_password = request.POST['confirmpassword']
        
        user = authenticate(request, username=request.user.username, password=current_password)
        if user is not None:
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return render(request, 'change_password.html', {'msg': 'Password updated successfully', 'error': 'no'})
            else:
                return render(request, 'change_password.html', {'msg': 'New Password and Confirm Password fields do not match', 'error': 'yes'})
        else:
            return render(request, 'change_password.html', {'msg': 'Your current password is wrong', 'error': 'not'})
    else:
        return render(request, 'change_password.html', {})    







# ====================== ind_admin_login ==============================================
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout

def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                # login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html', locals())

def logoutAdmin(request):
    if 'cadmin_id' in request.session:
        del request.session['cadmin_id']
 #   logout(request)
    return redirect('admin_login')







# ====================== Admin admin_dashboard ==============================

def admin_dashboard(request):
    return render(request , 'admin_dashboard.html')


def Settings(request):
    return render(request,'settings.html')

from django.shortcuts import render, get_object_or_404, redirect
from .models import ind_clientDT
from .forms import ind_clientDTForm

def client_list(request):
    clientdetail = ind_clientDT.objects.all()
    return render(request, 'client_list.html', {'clientdetail': clientdetail})

def update_client(request, clint_id):
    clientdetail = get_object_or_404(ind_clientDT, clint_id=clint_id)

    if request.method == 'POST':
        form = ind_clientDTForm(request.POST, instance=clientdetail)
        if form.is_valid():
            form.save()
            return redirect('client_list')
    else:
        form = ind_clientDTForm(instance=clientdetail)
    
    return render(request, 'update_clientdetail.html', {'form': form, 'clientdetail': clientdetail})

def delete_client(request, clint_id):
    clientdetail = get_object_or_404(ind_clientDT, clint_id=clint_id)
    if request.method == 'POST':
        clientdetail.delete()
        return redirect('client_list')
    return render(request, 'delete_client.html', {'clientdetail': clientdetail})


# ====================== strategy_list ===========================================
from .forms import StrategyForm

def strategy_list(request):
    strategy = Strategy.objects.all()
    
    return render(request, 'strategy_list.html', {'strategy': strategy})

# ====================== create_strategy ===========================================

def create_strategy(request):
    if request.method == 'POST':
        form = StrategyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('strategy_list')
    else:
        form = StrategyForm()
    return render(request, 'create_strategy.html', {'form': form})


# ====================== update_strategy ===========================================

@csrf_protect
def update_strategy(request, strategy_id):
    # Retrieve the symbol object from the database
    strategy = get_object_or_404(Strategy, id=strategy_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = StrategyForm(request.POST, instance=strategy)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('strategy_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = StrategyForm(instance=strategy)
    
    return render(request, 'update_strategy.html', {'form': form, 'strategy': strategy})

# ====================== delete_strategy ===========================================

def delete_strategy(request, strategy_id):
    strategy = Strategy.objects.get(id=strategy_id)
    if request.method == 'POST':
        strategy.delete()
        return redirect('strategy_list')  # Redirect to the strategy list page after deletion
    return render(request, 'delete_strategy.html', {'strategy': strategy})



# ====================== group_list ===========================================
from .forms import GroupForm

def group_list(request):
    groups = GROUP.objects.all()
    
    return render(request, 'group_list.html', {'groups': groups})

# ====================== create_group ===========================================

def create_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'create_group.html', {'form': form})


# ====================== update_group ===========================================

@csrf_protect
def update_group(request, group_id):
    # Retrieve the symbol object from the database
    group = get_object_or_404(GROUP, id=group_id)

    if request.method == 'POST':
        # Populate the form with the data from the request and the existing object
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            # Save the updated object to the database
            form.save()
            return redirect('group_list')
    else:
        # If it's a GET request, create a form instance with the existing object
        form = GroupForm(instance=group)
    
    return render(request, 'update_group.html', {'form': form, 'group': group})

# ====================== delete_group ===========================================


def delete_group(request, group_id):
    group = GROUP.objects.get(id=group_id)
    if request.method == 'POST':
        group.delete()
        return redirect('group_list')  # Redirect to the group list page after deletion
    return render(request, 'delete_group.html', {'group': group})


# ====================== order ===========================================

def order(request):
    return render(request,'place_order.html')


# from decimal import Decimal
# from django.shortcuts import render, get_object_or_404
# from django.utils import timezone

# # ====================== admin_message ===========================================

# def admin_message(request):
#     entry = ClientSignal.objects.filter(ENTRY = "ENTRY")
#     error = ""
#     s=""
#     symbols = SYMBOL.objects.all()  # Fetch all SYMBOL objects
#     user = 'rr'
#     current_date = timezone.now().date()
#     d = request.session.get('message_id')
#     if request.method == "POST":
#         if request.user.is_authenticated:
          

#             user = 'rr'
#             symbol_name = request.POST['symbol']  # Get the symbol name from the form
#             sy = get_object_or_404(SYMBOL, SYMBOL=symbol_name)  # Fetch the corresponding SYMBOL instance
#             ty = request.POST['type']

#             qty_str = request.POST['quantity']
#             exit_id = request.POST.get('exit_id', '')

#             # if exit_id:
#             #     client_signals = ClientSignal.objects.filter(message_id=exit_id, ids='No')
#             # else:
#             #     client_signals = []
#             client_signals = ClientSignal.objects.filter(message_id=d, ids='No')
    
#             print('client_signals',client_signals , 'exit_id = ',d)
#             if ty == 'BUY_EXIT' or ty == 'SELL_EXIT':
#                 if client_signals:
#                     client_signal = client_signals.first()
#                     if qty_str.strip():  # Check if quantity string is not empty or only whitespace
#                         qty = float(qty_str)
#                     elif ty == 'BUY_EXIT':
#                         qty = client_signal.QUANTITY
#                         enp = client_signal.ENTRY_PRICE
#                         exp = float(request.POST['exit_price'])
#                     elif ty == 'SELL_EXIT':
#                         qty = client_signal.QUANTITY
#                         enp = client_signal.ENTRY_PRICE
#                         exp = float(request.POST['exit_price'])
#                     else:
#                         qty = 0  # Set qty to a default value or handle it according to your logic
#                         enp = float(request.POST['entry_price'])
#                         exp = None

#                     if ty == 'BUY_EXIT':
#                         if symbol_name in ['XAUUSD', 'USOIL', 'EURUSD', 'GBPUSD', 'AUDNZD', 'GBPNZD', 'USDCHF', 'GBPCAD', 'EURAUD', 'AUDNZD', 'EURGBP', 'NZDUSD', 'USDCAD', 'AUDUSD']:
#                             prloss = (float(exp) - float(enp)) * qty * 100
#                         elif symbol_name in ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY']:
#                             prloss = (exp - enp) * 100 * 6.39 * qty
#                         else:
#                             prloss =  (float(exp) - float(enp)) * qty * 100   

#                         t = ClientSignal.objects.filter(TYPE='BUY_EXIT', client_id=client_signal.client_id, created_at__date=current_date)
#                         total = sum(Decimal(p.profit_loss) for p in t)
#                         total_pl = total + Decimal(prloss)
#                         s = 'EXIT Successful'
#                     elif ty == 'SELL_EXIT':
#                         if symbol_name in ['XAUUSD', 'USOIL', 'EURUSD', 'GBPUSD', 'AUDNZD', 'GBPNZD', 'USDCHF', 'GBPCAD', 'EURAUD', 'AUDNZD', 'EURGBP', 'NZDUSD', 'USDCAD', 'AUDUSD']:
#                             prloss = (float(enp) - float(exp)) * qty * 100
#                         elif symbol_name in ['USDJPY', 'EURJPY', 'GBPJPY', 'AUDJPY']:
#                             prloss = (enp - exp) * 100 * 6.39 * qty
#                         else:
#                             prloss =  (float(exp) - float(enp)) * qty * 100   

#                         t = ClientSignal.objects.filter(TYPE='SELL_EXIT', client_id=client_signal.client_id, created_at__date=current_date)
#                         total = sum(Decimal(p.profit_loss) for p in t)
#                         total_pl = total + Decimal(prloss)
#                         s = 'EXIT Successful'

#                     ClientSignal.objects.create(
#                         user=user, SYMBOL=sy, TYPE=ty, QUANTITY=qty,
#                         ENTRY_PRICE=enp, EXIT_PRICE=exp, profit_loss=prloss,
#                         cumulative_pl=total_pl, created_at=timezone.now(),
#                         message_id=client_signal.message_id, client_id=client_signal.client_id
#                     )
#                     if exit_id:
#                         update_entry = ClientSignal.objects.get(id=exit_id)
#                         update_entry.ENTRY = "none"
#                         update_entry.save()
#                 else:
#                     # Handle the case where no client_signals are found
#                     error = "No client signals found for the given exit ID."
#             else:
#                 qty = 0  # Set qty to a default value or handle it according to your logic
#                 enp = float(request.POST['entry_price'])
#                 exp = None
#                 prloss = None
#                 total_pl = None
#                 if ty == 'BUY_ENTRY' or ty == 'SELL_ENTRY':
#                     creat = ClientSignal.objects.create(user=user, SYMBOL=sy, admin='admin', TYPE=ty, QUANTITY=qty,
#                                                         ENTRY_PRICE=enp, EXIT_PRICE=None, profit_loss=prloss,
#                                                         cumulative_pl=total_pl, created_at=timezone.now())
#                     creat.message_id = creat.id
#                     creat.ids = generate_unique_id()
#                     creat.save()
#                     request.session['message_id'] = creat.id
#                     global my_global_variable
#                     my_global_variable = creat.ids

#                     error = "no"
#                     result = add_singnal_qty(request)
#     return render(request, 'admin_messages.html', {'symbols': symbols, 'error': error , 'entry':entry , 's':s})




# ============================================================================================================================

import random
import string

# ====================== generate_unique_idt =========================================== 

def generate_unique_id():
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(10))
    return unique_id

# ====================== add_singnal_qty ===========================================

def add_singnal_qty(request):
    Client_symbol_qty = Client_SYMBOL_QTY.objects.all()
    value = my_global_variable
    try:
        client_signal = ClientSignal.objects.get(ids= value) 
        for q in Client_symbol_qty:
            print('for tes qq', q.SYMBOL)
            print('for tes cc',client_signal.SYMBOL)
            print('for')
            if q.trade == 'on':
                print('on')    
                if str(q.SYMBOL) == str(client_signal.SYMBOL):
                    print('symbol')
                    print(q.SYMBOL)
                    print(client_signal.SYMBOL)
                    print('creat singnal')
                    creat = ClientSignal.objects.create(
                        user=client_signal.user,
                        SYMBOL=client_signal.SYMBOL,
                        TYPE=client_signal.TYPE,
                        ENTRY_PRICE=client_signal.ENTRY_PRICE,
                        ids = 'No',
                        QUANTITY=q.QUANTITY,
                        message_id = client_signal.message_id,
                        client_id = q.client_id,
                        created_at = timezone.now()
                    )

                    
        return HttpResponse('pass function')    
    except Exception as e:
        error = str(e)
        print(error)   
        return HttpResponse(f'error = {e}') 


"""  ######################################################################################################################


################################################ Add update code ####################################################
# 
# 
# #############################################################################################################"""   


    
# ============================ Admin Live MSG ==========================================================
from django.http import JsonResponse


from django.http import JsonResponse




def get_symbols(request):
    segment_type = request.GET.get('segment_type')
    symbol = request.GET.get('symbol')
    request.session['segment_type'] = segment_type
    if segment_type == 'cash':
        symbols = SYMBOL.objects.filter(exch_seg='NSE', SYMBOL = symbol).values('SYMBOL', 'symbol_token','SYMBOL_order')
    elif segment_type == 'options' or segment_type == 'futures':
        symbols = SYMBOL.objects.filter(exch_seg='NFO',SYMBOL = symbol).values('SYMBOL', 'symbol_token','SYMBOL_order')
    else:
        symbols = []

    return JsonResponse(list(symbols), safe=False)

from django.views.decorators.http import require_GET
@require_GET
def get_symbol_price(request):
    segment_type = request.session.get('segment_type')
    symbol_token = request.GET.get('symbol_token')
    
    if not symbol_token:
        return JsonResponse({"error": "symbol_token is required"}, status=400)
    
    try:
        sy = SYMBOL.objects.get(symbol_token=symbol_token)
        obj, refreshToken = initialize_connection2()
        
        if not obj or not refreshToken:
            return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."}, status=500)
        
        # Determine exchange based on segment type
        if segment_type == 'cash':
            exchange = 'NSE'  # or 'BSE'
        elif segment_type in ['futures', 'options']:
            exchange = 'NFO'
        else:
            return JsonResponse({"error": "Invalid segment type"}, status=400)
        
        symboltoken = sy.symbol_token
        SYMBOL_order = sy.SYMBOL_order

        ltp = get_ltp2(obj, symboltoken, SYMBOL_order, exchange)
        
        if ltp is None:
            return JsonResponse({"error": "Failed to fetch the latest price. Please try again later."}, status=500)
        
        Open = ltp['open']
        high = ltp['high']
        low = ltp['low']
        close = ltp['close']
        ltp = ltp['ltp']
        symbol_price = f'Price: {ltp}, Open: {Open}, High: {high}, Low: {low}, Close: {close}'

        return JsonResponse({'price': symbol_price})
    
    except SYMBOL.DoesNotExist:
        return JsonResponse({"error": "Symbol not found"}, status=404)
    
    except Exception as e:
        # Log the error for debugging purposes
        print(f'Error: {e}')
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)



def initialize_connection2():
    # Your Angel One API credentials
    api_key = "z2nnckx5"
    client_id = "K436935"
    password = "3547"
    secret_key = "KRXJPF2JYG5NJBCI2IC46TIAZ4"  # Replace with your actual TOTP secret key

    # Generate the latest TOTP using pyotp
    totp = pyotp.TOTP(secret_key).now()

    # Initialize the SmartConnect object
    obj = SmartConnect(api_key=api_key)
    try:
        # Generate session with Angel One
        data = obj.generateSession(client_id, password, totp)
        return obj, data['data']['refreshToken']
    except Exception as e:
        print(f"Error initializing connection: {e}")
        return None, None

# ============================ Get Latest Price (LTP) ===================================
def get_ltp2(obj, symboltoken, SYMBOL_order, exchange):
    try:
        ltp_data = obj.ltpData(exchange, SYMBOL_order, symboltoken)
        print(ltp_data)
        return ltp_data ['data']
    #    return ltp_data['data']['ltp']
    except Exception as e:
        print(f"Error fetching LTP: {e}")
        return None


from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
import pyotp

# ============================ CSRF Protected View for Live Admin Message ===================================
from django.db.models import Subquery, OuterRef, Min


@csrf_protect
def Live_admin_message(request):
    symbols = SYMBOL.objects.filter(
        id__in=Subquery(
            SYMBOL.objects.values('SYMBOL').annotate(
                min_id=Min('id')
            ).values('min_id')
        ))
    
#    symbols = SYMBOL.objects.all()
    
    if request.method == 'POST': 
        print('run form post')
        symbol_token = request.POST.get('symbol')
        s_type = request.POST.get('s_type')
        order_type = request.POST.get('Order_type')
        segment_type = request.POST.get('segment_type')
        squareoff = request.POST.get('squareoff')
        stoploss = request.POST.get('stoploss')
        try:
            symbol = SYMBOL.objects.get(symbol_token = symbol_token)
        except:
            symbol = None

        if s_type in ['BUY', 'SELL']:
            clients = ind_clientDT.objects.all()
            for client in clients:
                if client.clint_plane == 'Live':
                    group = client.client_Group
                    for group_symbol in group.symbols.all():
                        if str(group_symbol) == str(symbol.SYMBOL):
                            symbol_q = Client_SYMBOL_QTY.objects.filter(client_id=client.clint_id, SYMBOL=group_symbol)
                            for symbol_qty in symbol_q:
                                if symbol_qty.trade == 'on':
                                    qty = symbol_qty.QUANTITY
                                   
                                    if order_type in ['LIMIT', 'MARKET']:
                                        if segment_type == 'options':
                                            order_id = place_options_order(client.clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss)
                                        elif segment_type == 'cash':    
                                            order_id = place_order(client.clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss)
                                    elif order_type in ['STOPLOSS_LIMIT', 'STOPLOSS_MARKET']:  
                                        order_id =  place_stop_loss_order(client.clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss)      
                                            
                                    print('order_id = ', order_id)
                                else:
                                    print('trade off')
    
    dt = {
        'symbols': symbols,
    }
    # return render(request, 'admin_place_order.html', dt)
    return render(request, 'admin_place_order.html', dt)


# ============================ Initialize Connection ===================================


def initialize_connection2(user_id):
    user = ind_clientDT.objects.get(clint_id=user_id)
    auth_token = user.auth_token
    feed_token = user.feed_token
    refresh_token = user.refresh_token
    
    if not auth_token or not feed_token or not refresh_token:
        return None, None
    
    obj = SmartConnect(api_key=user.api_key)  # Initialize with your API key
    obj.setAccessToken(auth_token)  # Set the auth token
    obj.feedToken = feed_token  # Set the feed token
    obj.refreshToken = refresh_token  # Set the refresh token
    return obj, refresh_token


# ============================ Get Latest Price (LTP) ===================================
def get_ltp(obj, symboltoken, SYMBOL_order, exchange):
    try:
        ltp_data = obj.ltpData(exchange, SYMBOL_order, symboltoken)
        print(ltp_data)
        return ltp_data['data']['ltp']
    except Exception as e:
        print(f"Error fetching LTP: {e}")
        return None
    

def place_order(clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss):
    print('run order plce function = ',clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss)
    try:
        sy = SYMBOL.objects.get(symbol_token=symbol_token)
        client = ind_clientDT.objects.get(clint_id=clint_id)
        obj, refreshToken = initialize_connection2(clint_id)
        if not obj or not refreshToken:
            return {"error": "Failed to initialize connection. Please check your credentials and TOTP."}
        
        # Determine exchange based on segment type
        if segment_type == 'cash':
            exchange = 'NSE'  # or 'BSE'
        elif segment_type in ['futures', 'options']:
            exchange = 'NFO'
        else:
            return {"error": "Invalid segment type"}
        
        symboltoken = sy.symbol_token
        SYMBOL_order = sy.SYMBOL_order
        ltp = get_ltp(obj, symboltoken, SYMBOL_order, exchange)
      
        if ltp is None:
            return {"error": "Failed to fetch the latest price. Please try again later."}
        
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": SYMBOL_order,
            "symboltoken": symboltoken,
            "transactiontype": s_type,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": ltp,
            "squareoff": squareoff,
            "stoploss": stoploss,
            "quantity": qty
        }
        print(orderparams)
        orderId = obj.placeOrder(orderparams)

         # Save the order details to the database
        if orderId is not None:
            order = OrderAngelOne(
                clint=client.clint_id,
                
                symbol=sy.SYMBOL,
                tradingsymbol= SYMBOL_order,
                symboltoken= symboltoken,

                transaction_type=s_type,
                order_type=order_type,
                quantity=qty,
                segment_type=segment_type,
                squareoff=squareoff,
                stoploss=stoploss,
                price=ltp,
                order_id=orderId
            )
            order.save()
            print('save order')

        print('order id order function =', orderId)
        return {"order_id": orderId, "price": ltp}
    
    except Exception as e:
        print(f"Error placing order: {e}")
        return {"error": str(e)}    
    



# ============================ Place Order option ===================================



def place_options_order(clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss):
    print('Running options order placement function with parameters:', clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss)
    try:
        # Fetch symbol details
        sy = SYMBOL.objects.get(symbol_token=symbol_token)
        client = ind_clientDT.objects.get(clint_id=clint_id)
        
        # Initialize connection
        obj, refreshToken = initialize_connection2(clint_id)
        if not obj or not refreshToken:
            return {"error": "Failed to initialize connection. Please check your credentials and TOTP."}
        
        # Determine exchange based on segment type
        if segment_type == 'options':
            exchange = 'NFO'
        else:
            return {"error": "Invalid segment type for options order"}
        
        # Fetch the latest price
        symboltoken = sy.symbol_token
        SYMBOL_order = sy.SYMBOL_order
        ltp = get_ltp(obj, symboltoken, SYMBOL_order, exchange)
        
        if ltp is None:
            return {"error": "Failed to fetch the latest price. Please try again later."}
        
        # Get the lot size from the SYMBOL model
        lot_size = sy.lotsize
        print('lot_size =', lot_size , qty % lot_size)
        if lot_size is None:
            return {"error": "Lot size is not defined for this symbol."}
        
        # Validate quantity
        if qty % lot_size != 0:
            return {"error": f"Quantity is invalid. It should be in multiples of lot size {lot_size}."}
        
        # Prepare order parameters
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": SYMBOL_order,
            "symboltoken": symboltoken,
            "transactiontype": s_type,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": ltp,
            "squareoff": squareoff,
            "stoploss": stoploss,
            "quantity": qty
        }
        print('Order parameters:', orderparams)
        orderId = obj.placeOrder(orderparams)

         # Save the order details to the database
        if orderId is not None:
            order = OrderAngelOne(
                clint=client.clint_id,
                
                symbol=sy.SYMBOL,
                tradingsymbol= SYMBOL_order,
                symboltoken= symboltoken,

                transaction_type=s_type,
                order_type=order_type,
                quantity=qty,
                segment_type=segment_type,
                squareoff=squareoff,
                stoploss=stoploss,
                price=ltp,
                order_id=orderId
            )
            order.save()
            print('save order')
        
    #    return {"order_id": orderId, "price": ltp}
    
        
        # Place the order
        orderId = obj.placeOrder(orderparams)
        print('Order ID:', orderId , )
        return {"order_id": orderId, "price": ltp}
    
    except Exception as e:
        print(f"Error placing options order: {e}")
        return {"error": str(e)}
    


# ============================ place_stop_loss_order ===================================



def place_stop_loss_order(clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss):
    try:
        # Fetch symbol details
        sy = SYMBOL.objects.get(symbol_token=symbol_token)
        client = ind_clientDT.objects.get(clint_id=clint_id)
        
        # Initialize connection
        obj, refreshToken = initialize_connection2(clint_id)
        if not obj or not refreshToken:
            return {"error": "Failed to initialize connection. Please check your credentials and TOTP."}
        
        # Determine exchange based on segment type
        if segment_type == 'cash':
            exchange = 'NSE'  # or 'BSE'
        elif segment_type in ['futures', 'options']:
            exchange = 'NFO'
        else:
            return {"error": "Invalid segment type for options order"}
        
        # Fetch the latest price
        symboltoken = sy.symbol_token
        SYMBOL_order = sy.SYMBOL_order
        ltp = get_ltp(obj, symboltoken, SYMBOL_order, exchange)
        
        if ltp is None:
            return {"error": "Failed to fetch the latest price. Please try again later."}
        
        # Get the lot size from the SYMBOL model
        lot_size = sy.lotsize
        print('lot_size =', lot_size , qty % lot_size)
        if lot_size is None:
            return {"error": "Lot size is not defined for this symbol."}
        
        # Validate quantity
        if qty % lot_size != 0:
            return {"error": f"Quantity is invalid. It should be in multiples of lot size {lot_size}."}
   
        orderparams = {
            "variety": "STOPLOSS",
            "tradingsymbol": SYMBOL_order,
            "symboltoken": symboltoken,
            "transactiontype": s_type,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": ltp,
            "triggerprice": stoploss,  # Trigger price for the Stop Loss
            "squareoff": squareoff,
            "stoploss": stoploss,
            "quantity": qty
        }

     
        orderId = obj.placeOrder(orderparams)

         # Save the order details to the database
        if orderId is not None:
            order = OrderAngelOne(
                clint=client.clint_id,
                
                symbol=sy.SYMBOL,
                tradingsymbol= SYMBOL_order,
                symboltoken= symboltoken,

                transaction_type=s_type,
                order_type=order_type,
                quantity=qty,
                segment_type=segment_type,
                squareoff=squareoff,
                stoploss=stoploss,
                price=ltp,
                order_id=orderId
            )
            order.save()
            print('save order')
        print('Order ID:', orderId , )
        return {"order_id": orderId, "price": ltp}
    
    except Exception as e:
        print(f"Error placing options order: {e}")
        return {"error": str(e)}    

##################################################################################################################

#################################################################################################################

def create_gtt_rule(request):
    obj, refreshToken = initialize_connection()
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        gttCreateParams = {
            "tradingsymbol": "SBIN-EQ",
            "symboltoken": "3045",
            "exchange": "NSE",
            "producttype": "MARGIN",
            "transactiontype": "BUY",
            "price": 100000,
            "qty": 10,
            "disclosedqty": 10,
            "triggerprice": 200000,
            "timeperiod": 365
        }
        rule_id = obj.gttCreateRule(gttCreateParams)
        return JsonResponse({"gtt_rule_id": rule_id})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def list_gtt_rules(request):
    obj, refreshToken = initialize_connection()
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        status = ["FORALL"]  # Should be a list
        page = 1
        count = 10
        gtt_list = obj.gttLists(status, page, count)
        return JsonResponse({"gtt_list": gtt_list})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def fetch_historic_data(request, symbol , clint_id):
    sy = SYMBOL.objects.get(SYMBOL = symbol)
    client_id = ind_clientDT.objects.get(clint_id = clint_id)
    obj, refreshToken = initialize_connection(client_id.client_id)
    symboltoken = sy.symbol_token
    SYMBOL_order = sy.SYMBOL_order
#    obj, refreshToken = initialize_connection()
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        historicParam = {
            "exchange": "NSE",
            "symboltoken": symboltoken,
            "interval": "ONE_MINUTE",
            "fromdate": "2024-06-14 11:00",
            "todate": "2024-06-14 12:22"
        }
        candle_data = obj.getCandleData(historicParam)
        return ({"candle_data": candle_data})
    except Exception as e:
        return ({"error": str(e)})
    #     return JsonResponse({"candle_data": candle_data})
    # except Exception as e:
    #     return JsonResponse({"error": str(e)})

def logout(request):
    obj, refreshToken = initialize_connection()
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        logout_response = obj.terminateSession('your_client_id')
        return JsonResponse({"message": "Logout Successful"})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    



def Creat_client_api(request):
    return render(request ,'api_create_informations.html')



from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


def fetch_all_symbol(request):
    query = request.GET.get('q', '')
    symbols = SYMBOL.objects.all()

    if query:
        symbols = symbols.filter(SYMBOL__icontains=query) | symbols.filter(SYMBOL_order__icontains=query)

    paginator = Paginator(symbols, 20)  # Show 10 symbols per page
    page = request.GET.get('page', 1)

    try:
        symbols = paginator.page(page)
    except PageNotAnInteger:
        symbols = paginator.page(1)
    except EmptyPage:
        symbols = paginator.page(paginator.num_pages)

    return render(request, 'symbol_list1.html', {'symbols': symbols, 'query': query})


def delete_symbol_to_database(request):
    SYMBOL.objects.all().delete()  # Optional: Clear existing data
    return HttpResponse('delet all sumbol')

# =============================================================================================================================

'''                                                LIVE SYMBOL DATA METHODS                                                   '''

# =================================     ================================================================================================
import requests
import json
from datetime import datetime
from django.shortcuts import render

# Function to fetch live data
def fetch_live_data(symbol):
    url = f'https://your-live-data-api.com/data/{symbol}'  # Replace with actual live data API URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching live data for {symbol}: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error for {symbol}: {e}")
    return None

# Separate functions to fetch specific field data from live data
def fetch_live_data_for_expiry(symbol):
    live_data = fetch_live_data(symbol)
    if live_data and 'expiry' in live_data:
        try:
            return datetime.strptime(live_data['expiry'], '%Y-%m-%d').date()
        except ValueError:
            return None
    return None

def fetch_live_data_for_strike(symbol):
    live_data = fetch_live_data(symbol)
    if live_data and 'strike' in live_data:
        return live_data['strike']
    return None

def fetch_live_data_for_lotsize(symbol):
    live_data = fetch_live_data(symbol)
    if live_data and 'lotsize' in live_data:
        return live_data['lotsize']
    return None

def fetch_live_data_for_tick_size(symbol):
    live_data = fetch_live_data(symbol)
    if live_data and 'tick_size' in live_data:
        return live_data['tick_size']
    return None


from django.core.exceptions import ValidationError
# Main view function to fetch and save data
# def fetch_instruments(client):
#     global instrument_dict
#     url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
#     print(url)
#     response = requests.get(url)
#     print(response)
    
#     if response.status_code == 200:
#         instruments = response.json()
#         instrument_dict = {instrument['symbol']: instrument['token'] for instrument in instruments}
#         logger.info(f"Instrument list fetched successfully: {list(instrument_dict.keys())}")

#         # Define the list of symbols to save
#         symbols_to_save = ["BANKNIFTY", "NIFTY", "FINNIFTY"]

#         # Process each instrument and update or create records in the database
#         for instrument in instruments:
#             name = instrument.get('name')
#             if name not in symbols_to_save:
#                 continue  # Skip symbols that are not in the list
#             symbol = instrument.get('symbol')
#             symbol_token = instrument.get('token')
#             expiry_str = instrument.get('expiry')
#             strike = instrument.get('strike')
#             lotsize = instrument.get('lotsize')
#             instrumenttype = instrument.get('instrumenttype')
#             exch_seg = instrument.get('exch_seg')
#             tick_size = instrument.get('tick_size')

#             # Validate and parse expiry date
#             expiry = None
#             if expiry_str:
#                 try:
#                     expiry = datetime.strptime(expiry_str, '%Y-%m-%d').date()
#                 except ValueError:
#                     logger.warning(f"Invalid date format for expiry: {expiry_str}")

#             # Update or create the SYMBOL record
#             try:
#                 obj, created = SYMBOL.objects.update_or_create(
#                     symbol_token=symbol_token,
#                     defaults={
#                         'SYMBOL': name,
#                         'SYMBOL_order': symbol,  # Update SYMBOL_order with the symbol value
#                         'expiry': expiry,
#                         'strike': strike,
#                         'lotsize': lotsize,
#                         'instrumenttype': instrumenttype,
#                         'exch_seg': exch_seg,
#                         'tick_size': tick_size
#                     }
#                 )
#                 if created:
#                     logger.info(f"Created new SYMBOL record: {obj}")
#                 else:
#                     logger.info(f"Updated SYMBOL record: {obj}")
#             except ValidationError as e:
#                 logger.error(f"Validation error while saving SYMBOL record: {e}")
#             except Exception as e:
#                 logger.error(f"Error while saving SYMBOL record: {e}")

#     else:
#         logger.error("Failed to fetch instrument list")

def fetch_instruments(request):
    global instrument_dict
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    print(url)
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        instruments = response.json()
        instrument_dict = {instrument['symbol']: instrument['token'] for instrument in instruments}
        logger.info(f"Instrument list fetched successfully: {instrument_dict.keys()}")
        return JsonResponse({"message": "Instrument list fetched successfully", "instruments": list(instrument_dict.keys())})
    else:
        logger.error("Failed to fetch instrument list")
        return JsonResponse({"error": "Failed to fetch instrument list"}, status=500)
    

def fetch_and_save_data(request):
    url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
    response = requests.get(url)
    
    if response.status_code == 200:
        instruments = response.json()

        # Define the list of symbols to save
        symbols_to_save = ["BANKNIFTY", "NIFTY", "FINNIFTY"]

        # Initialize response data
        response_data = {
            'status': 'success',
            'message': 'Data fetched and saved successfully.',
            'created': 0,
            'updated': 0,
            'errors': []
        }

        # Process each instrument and update or create records in the database
        for instrument in instruments:
            name = instrument.get('name')
            if name not in symbols_to_save:
                continue  # Skip symbols that are not in the list
            
            symbol = instrument.get('symbol')
            symbol_token = instrument.get('token')
            expiry_str = instrument.get('expiry')
            strike = instrument.get('strike')
            lotsize = instrument.get('lotsize')
            instrumenttype = instrument.get('instrumenttype')
            exch_seg = instrument.get('exch_seg')
            tick_size = instrument.get('tick_size')

            # Validate and parse expiry date
            expiry = None
            if expiry_str:
                for date_format in ['%d%b%Y', '%Y-%m-%d']:
                    try:
                        expiry = datetime.strptime(expiry_str, date_format).date()
                        break
                    except ValueError:
                        continue
                if expiry is None:
                    response_data['errors'].append(f"Invalid date format for expiry: {expiry_str}")
                    continue  # Skip this record if date parsing fails

            # Validate and parse numeric fields
            try:
                strike = float(strike) if strike else None
                lotsize = int(lotsize) if lotsize else None
                tick_size = float(tick_size) if tick_size else None
            except ValueError as e:
                response_data['errors'].append(f"Invalid numeric value: {e}")
                continue  # Skip this record if numeric conversion fails

            # Update or create the SYMBOL record
            try:
                obj, created = SYMBOL.objects.update_or_create(
                    symbol_token=symbol_token,
                    defaults={
                        'SYMBOL': name,
                        'SYMBOL_order': symbol,  # Update SYMBOL_order with the symbol value
                        'expiry': expiry,
                        'strike': strike,
                        'lotsize': lotsize,
                        'instrumenttype': instrumenttype,
                        'exch_seg': exch_seg,
                        'tick_size': tick_size
                    }
                )
                if created:
                    print(f"Created new SYMBOL record: {obj}")
                    response_data['created'] += 1
                else:
                    print(f"Updated SYMBOL record: {obj}")
                    response_data['updated'] += 1
            except ValidationError as e:
                response_data['errors'].append(f"Validation error while saving SYMBOL record: {e}")
            except Exception as e:
                response_data['errors'].append(f"Error while saving SYMBOL record: {e}")

        return JsonResponse(response_data)

    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to fetch instrument list.'
        }, status=500)   
                 
    
# ============================ Admin Live MSG ==========================================================

# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import SYMBOL, ind_clientDT, Client_SYMBOL_QTY

# def Live_admin_message(request):
#     symbols = SYMBOL.objects.all()

#     if request.method == 'POST':
#         symbol_token = request.POST.get('symbol')
#         s_type = request.POST.get('s_type')
#         Order_type = request.POST.get('Order_type')

#         try:
#             symbol = SYMBOL.objects.get(symbol_token=symbol_token).SYMBOL
#         except SYMBOL.DoesNotExist:
#             return JsonResponse({"error": "Symbol not found."})

#         if s_type == 'BUY':
#             clients = ind_clientDT.objects.filter(clint_plane='Live')
#             for client in clients:
#                 group = client.client_Group
#                 group_symbols = group.symbols.all()
#                 for group_symbol in group_symbols:
#                     if str(group_symbol) == str(symbol):
#                         symbol_q = Client_SYMBOL_QTY.objects.filter(client_id=client.clint_id, SYMBOL=group_symbol)
#                         for symbol_qty in symbol_q:
#                             if symbol_qty.trade == 'on':
#                                 order_id = place_order(client.clint_id, symbol, s_type, Order_type, symbol_qty.QUANTITY)
#                                 print('order_id = ', order_id)
#                             else:
#                                 print('trade off')
#         elif s_type == 'SELL':
#             clients = ind_clientDT.objects.filter(clint_plane='Live')
#             for client in clients:
#                 group = client.client_Group
#                 group_symbols = group.symbols.all()
#                 for group_symbol in group_symbols:
#                     if str(group_symbol) == str(symbol):
#                         symbol_q = Client_SYMBOL_QTY.objects.filter(client_id=client.clint_id, SYMBOL=group_symbol)
#                         for symbol_qty in symbol_q:
#                             if symbol_qty.trade == 'on':
#                                 order_id = place_order(client.clint_id, symbol, s_type, Order_type, symbol_qty.QUANTITY)
#                                 print('order_id = ', order_id)
#                             else:
#                                 print('trade off')

#     context = {
#         'symbols': symbols,
#     }
#     return render(request, 'admin_place_order.html', context)



# def fetch_symbols(request):
#     stock = request.GET.get('stock')
#     symbols = SYMBOL.objects.filter(SYMBOL__icontains=stock)
#     symbol_list = list(symbols.values('symbol_token', 'SYMBOL'))
#     return JsonResponse({'symbols': symbol_list})

# def get_symbols(request):
#     symbols = SYMBOL.objects.all()
#     symbol_list = list(symbols.values('symbol_token', 'SYMBOL', 'expiry', 'strike', 'lotsize', 'instrumenttype', 'exch_seg', 'tick_size'))
#     return JsonResponse({'symbols': symbol_list})

# import requests
# from datetime import datetime
# from .models import SYMBOL
# from django.http import JsonResponse

# def fetch_and_save_option_data():
#     url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data: {e}")
#         return f"Error fetching data: {e}"
#     except json.JSONDecodeError as e:
#         print(f"JSON decode error: {e}")
#         return f"JSON decode error: {e}"

#     relevant_symbols = ["NIFTY BANK", "NIFTY 50", "NIFTY FIN SERVICE"]
#     for item in data:
#         expiry_date_str = item.get('expiry')
#         expiry_date = None
#         if expiry_date_str:
#             try:
#                 expiry_date = datetime.strptime(expiry_date_str, '%d%b%Y').date()
#             except ValueError:
#                 print(f"Invalid date format for expiry_date: {expiry_date_str}")
#                 expiry_date = None

#         symbol_name = item.get('name', '').upper()
#         if any(relevant in symbol_name for relevant in relevant_symbols):
#             try:
#                 SYMBOL.objects.update_or_create(
#                     symbol_token=item.get('token'),
#                     defaults={
#                         'SYMBOL': item.get('symbol'),
#                         'SYMBOL_order': item.get('symbol'),
#                         'symbol_token': item.get('token'),
#                         'expiry': expiry_date,
#                         'strike': item.get('strike'),
#                         'lotsize': item.get('lotsize'),
#                         'instrumenttype': item.get('instrumenttype'),
#                         'exch_seg': item.get('exch_seg'),
#                         'tick_size': item.get('tick_size'),
#                     }
#                 )
#                 print(f"Saved symbol: {symbol_name}")
#             except Exception as e:
#                 print(f"Error saving symbol {symbol_name}: {e}")

#     return "Successfully updated symbol-token mappings"

# # Ensure the function is called correctly
# fetch_and_save_option_data()


# def fetch_options(request):
#     symbol = request.GET.get('symbol')
#     if symbol:
#         options = SYMBOL.objects.filter(SYMBOL__icontains=symbol)
#         options_list = list(options.values('symbol_token', 'SYMBOL', 'expiry', 'strike', 'lotsize', 'instrumenttype', 'exch_seg', 'tick_size'))
#         return JsonResponse({'options': options_list})
#     else:
#         return JsonResponse({'error': 'No symbol provided'}, status=400)
    
# ============================ Creat Api client ===================================

# def Creat_client_api(request):
#     return render(request ,'api_create_informations.html')


# from SmartApi import SmartConnect
# from django.shortcuts import render
# from django.http import JsonResponse
# import json
# import pyotp

# def initialize_connection(client_id):
    
#     try:
#         # Fetch the client's credentials from the database
#         client = ind_clientDT.objects.get(client_id=client_id)
#     except ind_clientDT.DoesNotExist:
#         return None, None
    
#     api_key = client.api_key
#     client_id = client.client_id
#     password = client.password
#     secret_key = client.secret_key

#     # Your Angel One API credentials
#     # api_key = "z2nnckx5"
#     # client_id = "K436935"
#     # password = "3547"
#     # secret_key = "KRXJPF2JYG5NJBCI2IC46TIAZ4"  # Replace with your actual TOTP secret key

#     # Generate the latest TOTP using pyotp
#     totp = pyotp.TOTP(secret_key).now()

#     # Initialize the SmartConnect object
#     obj = SmartConnect(api_key=api_key)
#     try:
#         # Generate session with Angel One
#         data = obj.generateSession(client_id, password, totp)
#         return obj, data['data']['refreshToken']
#     except Exception as e:
#         print(f"Error initializing connection: {e}")
#         return None, None

# def get_ltp(obj, symboltoken , SYMBOL_order):
#     try:
#         # Fetch the latest market data
#         ltp_data = obj.ltpData("NFO", SYMBOL_order, symboltoken)
#         print(ltp_data)
#         return ltp_data['data']['ltp']
#     except Exception as e:
#         print(f"Error fetching LTP: {e}")
#         return None


# import pyotp
# #def place_order(request,client_id,):
# def place_order(clint_id,symbol,s_type,Order_type,qty):
#     print('run palce order')
#     sy = SYMBOL.objects.get(SYMBOL = symbol)
#     client_id = ind_clientDT.objects.get(clint_id = clint_id)
#     obj, refreshToken = initialize_connection(client_id.client_id)
# def place_order(clint_id, symbol, s_type, Order_type, qty):
#     try:
#         sy = SYMBOL.objects.get(SYMBOL=symbol)
#         client = ind_clientDT.objects.get(clint_id=clint_id)
#     except (SYMBOL.DoesNotExist, ind_clientDT.DoesNotExist):
#         return {"error": "Invalid symbol or client ID"}

#     obj, refreshToken = initialize_connection(client.client_id)
#     if not obj or not refreshToken:
#         return {"error": "Failed to initialize connection. Please check your credentials and TOTP."}
    
#     symboltoken = sy.symbol_token
#     SYMBOL_order = sy.SYMBOL_order
#     ltp = get_ltp(obj, symboltoken, SYMBOL_order)
#     if ltp is None:
#         return {"error": "Failed to fetch the latest price. Please try again later."}
    
#     try:
#         orderparams = {
#             "variety": "NORMAL",
#             "tradingsymbol": SYMBOL_order,
#             "symboltoken": symboltoken,
#             "transactiontype": s_type,  # SELL, BUY
#             "exchange": sy.exch_seg,
#             "ordertype": Order_type,  # LIMIT, MARKET
#             "producttype": "INTRADAY",
#             "duration": "DAY",
#             "price": ltp,  # Use the fetched price
#             "squareoff": '0',
#             "stoploss": '0',
#             "quantity": qty ,##"1"  # Order quantity
#             "squareoff": "0",
#             "stoploss": "0",
#             "quantity": qty  # Order quantity
#         }
#         orderId = obj.placeOrder(orderparams)
#         return {"order_id": orderId, "price": ltp}
#     except Exception as e:
#         return {"error": str(e)}

# def create_gtt_rule(request):
#     obj, refreshToken = initialize_connection()
#     if not obj or not refreshToken:
#         return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
#     try:
#         gttCreateParams = {
#             "tradingsymbol": "SBIN-EQ",
#             "symboltoken": "3045",
#             "exchange": "NFO",
#             "producttype": "MARGIN",
#             "transactiontype": "BUY",
#             "price": 100000,
#             "qty": 10,
#             "disclosedqty": 10,
#             "triggerprice": 200000,
#             "timeperiod": 365
#         }
#         rule_id = obj.gttCreateRule(gttCreateParams)
#         return JsonResponse({"gtt_rule_id": rule_id})
#     except Exception as e:
#         return JsonResponse({"error": str(e)})

# def list_gtt_rules(request):
#     obj, refreshToken = initialize_connection()
#     if not obj or not refreshToken:
#         return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
#     try:
#         status = ["FORALL"]  # Should be a list
#         page = 1
#         count = 10
#         gtt_list = obj.gttLists(status, page, count)
#         return JsonResponse({"gtt_list": gtt_list})
#     except Exception as e:
#         return JsonResponse({"error": str(e)})

# def fetch_historic_data(request, symbol , clint_id):
#     sy = SYMBOL.objects.get(SYMBOL = symbol)
#     client_id = ind_clientDT.objects.get(clint_id = clint_id)
#     obj, refreshToken = initialize_connection(client_id.client_id)
#     symboltoken = sy.symbol_token
#     SYMBOL_order = sy.SYMBOL_order
# #    obj, refreshToken = initialize_connection()
#     if not obj or not refreshToken:
#         return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
#     try:
#         historicParam = {
#             "exchange": "NFO",
#             "symboltoken": symboltoken,
#             "interval": "ONE_MINUTE",
#             "fromdate": "2024-06-14 11:00",
#             "todate": "2024-06-14 12:22"
#         }
#         candle_data = obj.getCandleData(historicParam)
#         return ({"candle_data": candle_data})
#     except Exception as e:
#         return ({"error": str(e)})
#     #     return JsonResponse({"candle_data": candle_data})
#     # except Exception as e:
#     #     return JsonResponse({"error": str(e)})

# def logout(request):
#     obj, refreshToken = initialize_connection()
#     if not obj or not refreshToken:
#         return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
#     try:
#         logout_response = obj.terminateSession('your_client_id')
#         return JsonResponse({"message": "Logout Successful"})
#     except Exception as e:
#         return JsonResponse({"error": str(e)})
    
    
    

# ======================================  Complite code ==================================================

"""



from SmartApi import SmartConnect
from django.shortcuts import render
from django.http import JsonResponse
import json
import pyotp

def initialize_connection(client_id):
    
    try:
        # Fetch the client's credentials from the database
        client = ind_clientDT.objects.get(client_id=client_id)
    except ind_clientDT.DoesNotExist:
        return None, None
    
    api_key = client.api_key
    client_id = client.client_id
    password = client.password
    secret_key = client.secret_key

    # Your Angel One API credentials
    # api_key = "z2nnckx5"
    # client_id = "K436935"
    # password = "3547"
    # secret_key = "KRXJPF2JYG5NJBCI2IC46TIAZ4"  # Replace with your actual TOTP secret key

    # Generate the latest TOTP using pyotp
    totp = pyotp.TOTP(secret_key).now()

    # Initialize the SmartConnect object
    obj = SmartConnect(api_key=api_key)
    try:
        # Generate session with Angel One
        data = obj.generateSession(client_id, password, totp)
        return obj, data['data']['refreshToken']
    except Exception as e:
        print(f"Error initializing connection: {e}")
        return None, None

def get_ltp(obj, symboltoken):
    try:
        # Fetch the latest market data
        ltp_data = obj.ltpData("NSE", "SBIN-EQ", symboltoken)
        print(ltp_data)
        return ltp_data['data']['ltp']
    except Exception as e:
        print(f"Error fetching LTP: {e}")
        return None

#def place_order(request,client_id,):
def place_order(clint_id,symbol,s_type,Order_type):
    print('run palce order')
    sy = SYMBOL.objects.get(SYMBOL = symbol)
    client_id = ind_clientDT.objects.get(clint_id = clint_id)
    obj, refreshToken = initialize_connection(client_id.client_id)
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    
    # Fetch the latest price
    symboltoken = sy.symbol_token
    ltp = get_ltp(obj, symboltoken)
    if ltp is None:
        return JsonResponse({"error": "Failed to fetch the latest price. Please try again later."})
     
    try:
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": sy.SYMBOL,
            "symboltoken": symboltoken,
            "transactiontype": s_type, # SELL , BUY
            "exchange": "NSE",
            "ordertype": Order_type,  # LIMIT , MARKET
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": ltp,  # Use the fetched price
            "squareoff": "0",
            "stoploss": "0",
            "quantity": "1"  # Order quantity
        }
        orderId = obj.placeOrder(orderparams)
        return JsonResponse({"order_id": orderId, "price": ltp})
    except Exception as e:
        return JsonResponse({"error": str(e)})


def create_gtt_rule(request):
    obj, refreshToken = initialize_connection()
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        gttCreateParams = {
            "tradingsymbol": "SBIN-EQ",
            "symboltoken": "3045",
            "exchange": "NSE",
            "producttype": "MARGIN",
            "transactiontype": "BUY",
            "price": 100000,
            "qty": 10,
            "disclosedqty": 10,
            "triggerprice": 200000,
            "timeperiod": 365
        }
        rule_id = obj.gttCreateRule(gttCreateParams)
        return JsonResponse({"gtt_rule_id": rule_id})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def list_gtt_rules(request):
    obj, refreshToken = initialize_connection()
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        status = ["FORALL"]  # Should be a list
        page = 1
        count = 10
        gtt_list = obj.gttLists(status, page, count)
        return JsonResponse({"gtt_list": gtt_list})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def fetch_historic_data(request):
    obj, refreshToken = initialize_connection()
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        historicParam = {
            "exchange": "NSE",
            "symboltoken": "3045",
            "interval": "ONE_MINUTE",
            "fromdate": "2024-05-01 09:00",
            "todate": "2024-05-31 03:08"
        }
        candle_data = obj.getCandleData(historicParam)
        return JsonResponse({"candle_data": candle_data})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def logout(request):
    obj, refreshToken = initialize_connection()
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        logout_response = obj.terminateSession('your_client_id')
        return JsonResponse({"message": "Logout Successful"})
    except Exception as e:
        return JsonResponse({"error": str(e)})



"""
# # ============================ symboltech ===========================================
# import requests
# from datetime import datetime
# from django.core.management.base import BaseCommand
# from accounts.models import SYMBOL

# def fetch_and_save_symbols():
#     url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
#     response = requests.get(url)
    
#     if response.status_code == 200:
#         data = response.json()
#         save_to_database(data)
#     else:
#         print("Failed to fetch data from the URL.")

# def save_to_database(data):
#     SYMBOL.objects.all().delete()  # Optional: Clear existing data
#     for item in data:
#         expiry_date = datetime.strptime(item['expiry'], '%d%b%Y').date() if item['expiry'] else None
#         symbol_instance = SYMBOL(
#             token=item.get('token'),
#             symbol=item.get('symbol'),
#             name=item.get('name'),
#             expiry=expiry_date,
#             strike=float(item.get('strike')),
#             lotsize=int(item.get('lotsize')),
#             instrumenttype=item.get('instrumenttype'),
#             exch_seg=item.get('exch_seg'),
#             tick_size=float(item.get('tick_size')),
#         )
#         symbol_instance.save()
#     print('Successfully saved symbol-token mappings to the database.')

# class Command(BaseCommand):
#     help = 'Fetch and save symbol-token mappings to the database'

#     def handle(self, *args, **kwargs):
#         fetch_and_save_symbols()

# from django.shortcuts import render
# from .models import SYMBOL

# import requests
# from django.shortcuts import render

# # def fetch_and_display_data(request):
# #     return render(request, 'symbol_list1.html')
# import requests
# from django.shortcuts import render
# from .models import SYMBOL
# from datetime import datetime
# import json

# # Function to fetch live data for a given symbol
# def fetch_live_data(symbol):
#     url = f'https://your-live-data-api.com/data/{symbol}'  # Replace with actual live data API URL
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching live data for {symbol}: {e}")
#     except json.JSONDecodeError as e:
#         print(f"JSON decode error for {symbol}: {e}")
#     return None

# # Separate functions to fetch specific field data from live data
# def fetch_live_data_for_expiry(symbol):
#     live_data = fetch_live_data(symbol)
#     if live_data and 'expiry' in live_data:
#         try:
#             return datetime.strptime(live_data['expiry'], '%Y-%m-%d').date()
#         except ValueError:
#             return None
#     return None

# def fetch_live_data_for_strike(symbol):
#     live_data = fetch_live_data(symbol)
#     if live_data and 'strike' in live_data:
#         return live_data['strike']
#     return None

# def fetch_live_data_for_lotsize(symbol):
#     live_data = fetch_live_data(symbol)
#     if live_data and 'lotsize' in live_data:
#         return live_data['lotsize']
#     return None

# def fetch_live_data_for_tick_size(symbol):
#     live_data = fetch_live_data(symbol)
#     if live_data and 'tick_size' in live_data:
#         return live_data['tick_size']
#     return None

# # Main view function to fetch and save data
# def fetch_and_save_data(request):
#     url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an exception for HTTP errors
#         data = response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"Error fetching data from URL: {e}")
#         data = []
#     except json.JSONDecodeError as e:
#         print(f"JSON decode error: {e}")
#         data = []

#     for item in data:
#         expiry_date = item.get('expiry')
#         if expiry_date:
#             try:
#                 expiry_date = datetime.strptime(expiry_date, '%d-%b-%Y').date()
#             except ValueError:
#                 expiry_date = fetch_live_data_for_expiry(item.get('symbol'))
#         else:
#             expiry_date = fetch_live_data_for_expiry(item.get('symbol'))

#         if not expiry_date:
#             expiry_date = datetime.now().date()  # Assign a default value if expiry date is not available

#         SYMBOL.objects.update_or_create(
#             token=item.get('token'),
#             defaults={
#                 'symbol': item.get('symbol'),
#                 'name': item.get('name'),
#                 'expiry': expiry_date,
#                 'strike': item.get('strike') if item.get('strike') else fetch_live_data_for_strike(item.get('symbol')),
#                 'lotsize': item.get('lotsize') if item.get('lotsize') else fetch_live_data_for_lotsize(item.get('symbol')),
#                 'instrumenttype': item.get('instrumenttype'),
#                 'exch_seg': item.get('exch_seg'),
#                 'tick_size': item.get('tick_size') if item.get('tick_size') else fetch_live_data_for_tick_size(item.get('symbol')),
#             }
#         )

#     symbols = SYMBOL.objects.all()
#     return render(request, 'symbol_list1.html', {'symbols': symbols})




# =========================================================================
#                           client views
# =========================================================================


from django.shortcuts import render ,HttpResponse , redirect
from .models import ind_clientDT , ClientSignal , Client_SYMBOL_QTY , SYMBOL
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone

from .models import ind_clientDT , GROUP , BROKERS


from django.utils import timezone    
import datetime
from django.contrib import messages
from cmpalgo import settings
from django.core.mail import send_mail

# ###########################  clint login method start ####################################
# my_global_variable = None

# @csrf_protect
# def client_login(request):
#     if 'msg' in request.GET:
#         msg = request.GET['msg']
#     else:
#         msg = None 
    
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         print(email ,password)
#         try:
#             user = ind_clientDT.objects.get(clint_email=email)
#             if password == user.clint_password:
#                 user_id = ind_clientDT.objects.get(clint_email=user.clint_email)
#                 # Check if last login date is today or later
#                 if user.clint_last_login.date() >= timezone.now().date():
#                     request.session['clint_id'] = user_id.clint_id

#                     # alls = SYMBOL.objects.all()
#                     group = user_id.client_Group
#                     alls = group.symbols.all()
#                     for s in alls:
#                         print(s)
#                         try:
#                             signals = Client_SYMBOL_QTY.objects.get(client_id = user_id.clint_id , SYMBOL = s)
#                             q = signals.QUANTITY
#                             d = signals.client_id
#                         except:    
#                             q = 0
#                             d = "my"
#                         if user_id.clint_id != d:
#                             creat = Client_SYMBOL_QTY.objects.create(
#                                 client_id = user_id.clint_id,
#                                 SYMBOL = s.SYMBOL,
#                                 QUANTITY = q
#                             )
                            
#                     # return HttpResponse('logi')
#                     return redirect('/dashbord/')
#                 else:
#                     return redirect('/?msg=your plane is expire')  
                
#             else:
#                 return redirect('/?msg=wrong password') 
#         except Exception as e:
#             print(e)
#             return redirect(f'/?msg=Email no register {e}') 
     
#     return render(request,'client_login.html', {'msg':msg})
my_global_variable = None

@csrf_protect
def client_login(request):
    if 'msg' in request.GET:
        msg = request.GET['msg']
    else:
        msg = None 

   # if 'clint_id' in request.session:
    #    return redirect('client_home')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email ,password)
        try:
            user = ind_clientDT.objects.get(clint_email=email)
            if password == user.clint_password:
                user_id = ind_clientDT.objects.get(clint_email=user.clint_email)
                # 'term_condition': client_user.term_condition,
                # Check if last login date is today or later
                if user.clint_last_login.date() >= timezone.now().date():
                    request.session['clint_id'] = user_id.clint_id

                #    alls = SYMBOL.objects.all()
                    group = user_id.client_Group
                    alls = group.symbols.all()
                    
                    for s in alls:
                        try:
                            signals = Client_SYMBOL_QTY.objects.get(client_id = user_id.clint_id , SYMBOL = s)
                            q = signals.QUANTITY
                            d = signals.client_id
                        except:    
                            q = 0
                            d = "my"
                        if user_id.clint_id != d:
                            creat = Client_SYMBOL_QTY.objects.create(
                                client_id = user_id.clint_id,
                                SYMBOL = s,
                                QUANTITY = q
                            )
                            
                 #   return HttpResponse('logi')
                    return redirect('homes')
                else:
                    return redirect('/?msg=your plane is expire')  
                
            else:
                return redirect('/?msg=wrong password') 
        except Exception as e:
            print(e)
            return redirect(f'/?msg=Email no register {e}') 
     
    return render(request,'client_login.html', {'msg':msg})

def client_logout(request):
    if 'clint_id' in request.session:
        del request.session['clint_id']
   # logout(request)
    return redirect('/')
 #   return HttpResponse('test')
# def client_logout(request):
#     return HttpResponse('test')
    # clint_id = request.session.get('clint_id')
    # del request.session['clint_id']
    # return redirect('')

###########################  clint login method start ####################################

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from .models import GROUP, ind_clientDT, BROKERS
import logging

logger = logging.getLogger(__name__)

@csrf_protect
def client_registration(request):
    error = ""
    groups = GROUP.objects.all()
    strategies = Strategy.objects.all()  # Fetch all strategies
    brokers = BROKERS.objects.all()
    
    if request.method == "POST":
        c_fname = request.POST['fname']
        c_lname = request.POST['lname']
        c_mno = request.POST['mobile']
        c_email = request.POST['email']
        c_from_date = request.POST['fromdate']
        c_last_date = request.POST['todate']
        password = request.POST['pwd']
        group_id = request.POST['group']
        account_type = request.POST['Acount_type']
        broker_id = request.POST['Broker']
        api_key = request.POST['api_key']
        selected_strategies = request.POST.getlist('strategies')  # Get selected strategies

        try:
            try:
                u = ind_clientDT.objects.get(clint_email=c_email)
                return render(request, 'register.html', {'msg':'Email already registered'}) 
            
            except ind_clientDT.DoesNotExist:    
                Group = None
                if group_id:
                    try:
                        Group = GROUP.objects.get(id=group_id)
                    except GROUP.DoesNotExist:
                        return render(request, 'register.html', {'msg': 'Selected group does not exist', 'groups': groups, 'brokers': brokers})
                
                Broker = None
                if broker_id:
                    try:
                        Broker = BROKERS.objects.get(broker_name=broker_id)
                    except BROKERS.DoesNotExist:
                        return render(request, 'register.html', {'msg': 'Selected broker does not exist', 'groups': groups, 'brokers': brokers})

                try:
                
                    
                    subject = f'Dear {c_fname} {c_lname}'
                    message = f""" {c_fname} {c_lname}
                    Thank you for choosing ANVESTORS for Algo Platform. We are pleased to inform you that the password of your
                    Algo Platform has been reset as per details mentioned below:

                    Login Details:

                    Email ID / User ID: {c_email}
                    Login Password: {password}

                    Note: Please change your login password as per your choice.

                    Login URL: http://software.anvestors.com
                    """
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [c_email]
                    send_mail(subject, message, email_from, recipient_list)
                    
                    ind_clientDT.objects.create(
                        clint_name_first=c_fname,
                        clint_name_last=c_lname,
                        clint_email=c_email,
                        clint_password=password,
                        clint_phone_number=c_mno,
                        clint_date_joined=c_from_date,
                        clint_last_login=c_last_date,
                        client_Group=Group,
                        clint_plane=account_type,
                        broker=Broker,
                        api_key=api_key,
                    )
                 #   client.strategies.set(selected_strategies)
                    
                    return redirect('client_detail')
                except Exception as e:
                    logger.error(f"Email sending failed: {e}")
                    return render(request, 'register.html', {'msg': f'Error sending email: {e}', 'groups': groups, 'brokers': brokers, 'strategies': strategies}) 
                
        except Exception as e:
            logger.error(f"Client registration failed: {e}")
            return render(request, 'register.html', {'msg': f'Error: {e}', 'groups': groups, 'brokers': brokers, 'strategies': strategies}) 
    
    return render(request, 'register.html', {'groups': groups, 'brokers': brokers, 'strategies': strategies})

# ===================================== Get singnal ================================================

from django.http import JsonResponse

# views.py
from django.http import JsonResponse
from .models import GROUP  # Import your GROUP model

def get_s(request, group_id):
    print('call function')
    try:
        group = GROUP.objects.get(id=group_id)
        symbols = group.symbols.all()
        symbols_list = [{'id': symbol.id, 'name': symbol.SYMBOL} for symbol in symbols]  # Replace 'SYMBOL' with the correct attribute
        return JsonResponse({'symbols': symbols_list})
    except GROUP.DoesNotExist:
        return JsonResponse({'symbols': []})


################# clint dashbord method start #######################



# def client_dashbord(request):
#     # try:
#         user_id = request.session.get('clint_id')
#         client_user = ind_clientDT.objects.get(clint_id=user_id)
#         try:
#             group = GROUP.objects.get(GROUP = client_user.client_Group)
     
#             # Retrieve all symbols from the group and iterate over them
#             symbols = group.symbols.all()
            
#         except:
#             symbols = []
#         current_date = timezone.now().date()
#         filtered_signals = Client_SYMBOL_QTY.objects.filter(client_id = user_id)
        
#         if request.method == "POST":
         
#         #    user_id = request.user.id  # Assuming user is logged in and has an ID
#             filtered_signals = Client_SYMBOL_QTY.objects.filter(client_id=user_id)
#             # n = 0
#             # for filtereds in filtered_signals:
#             #     print(filtereds) 
#             #     n = n+1
#             #     print(n)
#             for i in range(1, len(filtered_signals) + 1):
#                 print(i)
#                 symbol = request.POST.get(f'symbol_{i}')
#                 quantity = request.POST.get(f'quantity_{i}')
#                 strategy = request.POST.get(f'strategy_{i}')
#                 order_type = request.POST.get(f'order_type_{i}')
#                 product_type = request.POST.get(f'product_type_{i}')
#                 trading = 'on' if request.POST.get(f'trading_{i}') else 'off'
#                 print(f"symbol: {symbol}, quantity: {quantity}, strategy: {strategy}, order_type: {order_type}, product_type: {product_type}, trading: {trading}")

#                 try:
#                     signal = filtered_signals.get(SYMBOL=symbol)
#                     signal.QUANTITY = quantity
#                     signal.Strategy = strategy
#                     signal.Order_Type = order_type
#                     signal.Product_Type = product_type
#                     signal.trade = trading
#                     signal.save()
#                     print('try save')
#                 #    return redirect('client_home')
#                 except Client_SYMBOL_QTY.DoesNotExist:
#                     print(f"Signal with symbol {symbol} does not exist.")
#             #         messages.error(request, f"Signal with symbol {symbol} does not exist.")
#             return redirect('client_dashbord')
#             # messages.success(request, "Signals updated successfully.")

#         dt = {
#             'symbols':symbols,
#             'signals':filtered_signals,
#             'client_user': client_user,
        
#         }
#         return render(request,'client_dashboard.html',dt)


@csrf_protect
def client_dashbord(request):
    try:
        if 'msg' in request.GET:
            msg = request.GET['msg']
        else:
            msg = None
        
        user_id = request.session.get('clint_id')
        client_user = ind_clientDT.objects.get(clint_id=user_id)
        
        try:
            client_user = ind_clientDT.objects.get(clint_id=user_id)
            group = GROUP.objects.get(GROUP=client_user.client_Group)
                # Retrieve all symbols from the group
            symbols = group.symbols.all()
                # Define the symbols to exclude
            symbols_to_exclude = ['BANKNIFTY', 'NIFTY', 'FINNIFTY']
            for symbol in symbols:
                for s in symbols_to_exclude:
                    if str(symbol) ==  str(s):
                        symbols_to_exclude.remove(str(symbol))
                    

        except GROUP.DoesNotExist:
            symbols_to_exclude = []
            symbols = []
            count = symbols.count()
            print(count)
            print(symbols_to_exclude)


        current_date = timezone.now().date()
        filtered_signals = Client_SYMBOL_QTY.objects.filter(client_id=user_id)

        if request.method == "POST":
            for i in range(1, len(filtered_signals) + 1):
                symbol = request.POST.get(f'symbol_{i}')
                quantity = request.POST.get(f'quantity_{i}')
                strategy = request.POST.get(f'strategy_{i}')
                order_type = request.POST.get(f'order_type_{i}')
                product_type = request.POST.get(f'product_type_{i}')
                trading = 'on' if request.POST.get(f'trading_{i}') else 'off'
                
                # Debug print statements
                print(f"symbol: {symbol}, quantity: {quantity}, strategy: {strategy}, order_type: {order_type}, product_type: {product_type}, trading: {trading}")

                if quantity and symbol:
                    try:
                        quantity = int(quantity)
                    except ValueError:
                        error = f"Invalid quantity value: {quantity}"
                        return redirect(f'/home/?msg={error}')
                    
                    g = GROUP.objects.get(GROUP=client_user.client_Group)
                    if quantity <= g.max_quantity:
                        try:
                            signal = filtered_signals.get(SYMBOL=symbol)
                            signal.QUANTITY = quantity
                            signal.Strategy = strategy
                            signal.Order_Type = order_type
                            signal.Product_Type = product_type
                            signal.trade = trading
                            signal.save()
                            print('Record updated successfully')
                        except Client_SYMBOL_QTY.DoesNotExist:
                            error = f"Signal with symbol {symbol} does not exist."
                            print(error)
                            return redirect(f'/home/?msg={error}')
                    else:
                        error = f'symbol {symbol} group max_quantity {g.max_quantity} any thing {quantity}'
                        return redirect(f'/home/?msg={error}')
            
            return redirect('client_dashbord')

        context = {
            'msg': msg,
            'symbols': symbols,
            'signals': filtered_signals,
            'client_user': client_user,
            'term_condition': client_user.Term_condition,
            'symbols_to_exclude': symbols_to_exclude,
            'count': len(symbols),
        }
        return render(request, 'client_dashboard.html', context)
    except:
        return redirect('/')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client_SYMBOL_QTY

def update_signals(request):
    if request.method == "POST":
        user_id = request.session.get('clint_id')
    #    user_id = request.user.id  # Assuming user is logged in and has an ID
        filtered_signals = Client_SYMBOL_QTY.objects.filter(client_id=user_id)
        
        for i in range(1, len(filtered_signals) + 1):
            print(i)
            symbol = request.POST.get(f'symbol_{i}')
            quantity = request.POST.get(f'quantity_{i}')
            strategy = request.POST.get(f'strategy_{i}')
            order_type = request.POST.get(f'order_type_{i}')
            product_type = request.POST.get(f'product_type_{i}')
            trading = 'on' if request.POST.get(f'trading_{i}') else 'off'


            try:
                signal = filtered_signals.get(SYMBOL=symbol)
                signal.QUANTITY = quantity
                signal.Strategy = strategy
                signal.Order_Type = order_type
                signal.Product_Type = product_type
                signal.trade = trading
                signal.save()
                print('try save')
            except Client_SYMBOL_QTY.DoesNotExist:
                print(f"Signal with symbol {symbol} does not exist.")
                messages.error(request, f"Signal with symbol {symbol} does not exist.")
        
        messages.success(request, "Signals updated successfully.")
        return HttpResponse('save')  # Redirect to an appropriate view after saving
    

    return render(request, 'your_template.html')  # Render the appropriate template if not POST

def client_signals(request):
    return render(request,'client_signals.html')


def order_place(request):
    return render(request,'place_order.html')

def client_thistory(request):
    return render(request,'client_thistory.html')


# =================================================  Api order plce ===========================================================

from django.shortcuts import render
from django.http import JsonResponse
from .models import ind_clientDT
import pyotp
from SmartApi import SmartConnect

def initialize_connection(client_id):
    try:
        # Fetch the client's credentials from the database
        client = ind_clientDT.objects.get(client_id=client_id)
    except ind_clientDT.DoesNotExist:
        return None, None
    
    api_key = client.api_key
    client_id = client.client_id
    password = client.password
    secret_key = client.secret_key

    # Generate the latest TOTP using pyotp
    totp = pyotp.TOTP(secret_key).now()

    # Initialize the SmartConnect object
    obj = SmartConnect(api_key=api_key)
    try:
        # Generate session with Angel One
        data = obj.generateSession(client_id, password, totp)
        return obj, data['data']['refreshToken']
    except Exception as e:
        print(f"Error initializing connection: {e}")
        return None, None

def fetch_current_price(obj, symboltoken):
    try:
        ltp_data = obj.ltpData('NFO', symboltoken)
        return ltp_data['data']['ltp']
    except Exception as e:
        print(f"Error fetching current price: {e}")
        return None

def place_order11(request):
    client_id = request.GET.get('client_id')  # Get client_id from the request
    obj, refreshToken = initialize_connection(client_id)
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})

    symboltoken = "3045"  # Symbol token for SBIN-EQ
    current_price = fetch_current_price(obj, symboltoken)
    if not current_price:
        return JsonResponse({"error": "Failed to fetch current market price."})

    try:
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": "SBIN-EQ",
            "symboltoken": symboltoken,
            "transactiontype": "BUY",
            "exchange": "NFO",
            "ordertype": "LIMIT",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": str(current_price),  # Use current market price
            "squareoff": "0",
            "stoploss": "0",
            "quantity": "125"
        }
        orderId = obj.placeOrder(orderparams)
        return JsonResponse({"order_id": orderId})
    except Exception as e:
        return JsonResponse({"error": str(e)})



def create_gtt_rule(request):
    client_id = request.GET.get('client_id')
    obj, refreshToken = initialize_connection(client_id)
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        gttCreateParams = {
            "tradingsymbol": "SBIN-EQ",
            "symboltoken": "3045",
            "exchange": "NFO",
            "producttype": "MARGIN",
            "transactiontype": "BUY",
            "price": 100000,
            "qty": 10,
            "disclosedqty": 10,
            "triggerprice": 200000,
            "timeperiod": 365
        }
        rule_id = obj.gttCreateRule(gttCreateParams)
        return JsonResponse({"gtt_rule_id": rule_id})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def list_gtt_rules(request):
    client_id = request.GET.get('client_id')
    obj, refreshToken = initialize_connection(client_id)
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        status = ["FORALL"]  # Should be a list
        page = 1
        count = 10
        gtt_list = obj.gttLists(status, page, count)
        return JsonResponse({"gtt_list": gtt_list})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def fetch_historic_data(request):
    client_id = request.GET.get('client_id')
    obj, refreshToken = initialize_connection(client_id)
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        historicParam = {
            "exchange": "NFO",
            "symboltoken": "3045",
            "interval": "ONE_MINUTE",
            "fromdate": "2024-05-01 09:00",
            "todate": "2024-05-31 03:08"
        }
        candle_data = obj.getCandleData(historicParam)
        return JsonResponse({"candle_data": candle_data})
    except Exception as e:
        return JsonResponse({"error": str(e)})

def logout(request):
    client_id = request.GET.get('client_id')
    obj, refreshToken = initialize_connection(client_id)
    if not obj or not refreshToken:
        return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})
    try:
        logout_response = obj.terminateSession(client_id)
        return JsonResponse({"message": "Logout Successful"})
    except Exception as e:
        return JsonResponse({"error": str(e)})
    
    
    
    
    
# _________________________________Instrument __________________________________________    
# views.py
import json
import logging
from django.http import JsonResponse
from SmartApi import SmartConnect
import os
from .models import ind_clientDT


# -----------------------------------------------------------------------------
# =============================================================================
# myapp/tasks.py

from celery import shared_task
import requests
from datetime import datetime
from .models import SYMBOL

@shared_task
def fetch_and_update_symbols():
    url = 'https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"
    except json.JSONDecodeError as e:
        return f"JSON decode error: {e}"

    for item in data:
        expiry_date = item.get('expiry')
        if expiry_date:
            try:
                expiry_date = datetime.strptime(expiry_date, '%d%b%Y').date()
            except ValueError:
                expiry_date = None

        SYMBOL.objects.update_or_create(
            token=item.get('token'),
            defaults={
                'symbol': item.get('symbol'),
                'name': item.get('name'),
                'expiry': expiry_date,
                'strike': item.get('strike'),
                'lotsize': item.get('lotsize'),
                'instrumenttype': item.get('instrumenttype'),
                'exch_seg': item.get('exch_seg'),
                'tick_size': item.get('tick_size'),
            }
        )
    return "Successfully updated symbol-token mappings"


# ====================== Admin admin_dashboard ==============================
from accounts.forms import HelpMessageForm

def admin_help_center(request):
    # Get the clint_id from the session
    clint_id = request.session.get('clint_id')
    
    # If clint_id is not found in the session, redirect to the admin login page
    if not clint_id:
        return redirect('admin_login')
    
    # Check if the user is an admin (you might have a way to distinguish admins from clients)
    # For example, if admins have a specific role in your system:
    if not request.user.is_superuser:
        return redirect('admin_login')

    # If the request method is POST, process the form submission
    if request.method == 'POST':
        form = HelpMessageForm(request.POST)
        if form.is_valid():
            # If form is valid, save the form data without associating it with any client
            help_message = form.save(commit=False)
            help_message.save()
            return redirect('admin_help_center')  # Redirect to the same page after form submission
    else:
        # If the request method is not POST, instantiate a new form
        form = HelpMessageForm()

    # Retrieve all HelpMessage objects (for admins, not associated with any client) in descending order by timestamp
    messages = HelpMessage.objects.all().order_by('-timestamp')

    # Render the admin_help_center.html template with the form and messages
    return render(request, 'admin_help_center.html', {'form': form, 'messages': messages})

from django.shortcuts import render, redirect
from .models import HelpMessage
from .forms import HelpMessageForm


def client_help_center(request):
    clint_id = request.session.get('clint_id')
    client_user = ind_clientDT.objects.get(clint_id=clint_id)
    if not clint_id:
        return redirect('client_login')  # Redirect to login if user_id is not in session

    try:
        client_detail = ind_clientDT.objects.get(clint_id=clint_id)
    except ind_clientDT.DoesNotExist:
        return redirect('client_login')  # Redirect to login if the client does not exist

    if request.method == 'POST':
        form = HelpMessageForm(request.POST)
        if form.is_valid():
            help_message = form.save(commit=False)
            help_message.user_id = client_detail  # Set the user_id field to the client_detail instance
            help_message.save()
            return redirect('client_help_center')  # Redirect to the same page or a thank you page
    else:
        form = HelpMessageForm()

    messages = HelpMessage.objects.filter(clint_id=client_detail)

    return render(request, 'help_center.html', {'form': form, 'messages': messages,'client_user':client_user})


# ---------------------------fetch option chainn data-------------------------------------

logger = logging.getLogger(__name__)

def fetch_option_chain(request):
    client_id = request.GET.get('client_id')

    if not client_id:
        return JsonResponse({'error': 'Client ID is required'}, status=400)

    try:
        client = ind_clientDT.objects.get(client_id=client_id)
    except ind_clientDT.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)
    
    api_key = client.api_key
    password = client.password
    secret_key = client.secret_key

    symbol = request.GET.get('symbol')

    if not symbol:
        return JsonResponse({'error': 'Symbol is required'}, status=400)

    # Initialize the Smart API client
    obj = SmartConnect(api_key=api_key)
    try:
        data = obj.generateSession(client.client_id, password, secret_key)
        logger.debug(f"Session Data: {data}")

        if 'status' in data and data['status'] == 'success':
            token = data['data']['refreshToken']
            obj.setSessionToken(token)

            exchange = 'NFO'
            option_chain = obj.ltpData(exchange, symbol)

            logger.debug(f"Option Chain Data: {option_chain}")

            if 'status' in option_chain and option_chain['status'] == 'success':
                return JsonResponse({'option_chain': option_chain['data']})
            else:
                logger.error(f"Error fetching option chain: {option_chain}")
                return JsonResponse({'error': 'Failed to fetch option chain data'}, status=500)

        else:
            logger.error(f"Error generating session: {data}")
            return JsonResponse({'error': 'Failed to generate session'}, status=500)

    except Exception as e:
        logger.error(f"Error in fetch_option_chain: {str(e)}")
        return JsonResponse({'error': 'Internal server error'}, status=500)

def place_option_order(request):
    client_id = request.POST.get('client_id')

    if not client_id:
        return JsonResponse({'error': 'Client ID is required'}, status=400)

    try:
        client = ind_clientDT.objects.get(client_id=client_id)
    except ind_clientDT.DoesNotExist:
        return JsonResponse({'error': 'Client not found'}, status=404)
    
    api_key = client.api_key
    password = client.password
    secret_key = client.secret_key

    if request.method == 'POST':
        symbol = request.POST.get('symbol')
        strike_price = request.POST.get('strike_price')
        option_type = request.POST.get('option_type')
        transaction_type = request.POST.get('transaction_type')
        quantity = int(request.POST.get('quantity'))
        order_type = request.POST.get('order_type')
        price = float(request.POST.get('price'))

        # Initialize the Smart API client
        obj = SmartConnect(api_key=api_key)
        try:
            data = obj.generateSession(client.client_id, password, secret_key)
            logger.debug(f"Session Data: {data}")

            if 'status' in data and data['status'] == 'success':
                token = data['data']['refreshToken']
                obj.setSessionToken(token)

                # Fetch the correct symbol token
                symbol_token = get_symbol_token(obj, symbol, strike_price, option_type)
                if not symbol_token:
                    return JsonResponse({'error': 'Symbol token not found'}, status=500)

                order_params = {
                    "variety": "NORMAL",
                    "tradingsymbol": f"{symbol}{strike_price}{option_type}",
                    "symboltoken": symbol_token,
                    "transactiontype": transaction_type,
                    "exchange": "NFO",
                    "ordertype": order_type,
                    "producttype": "INTRADAY",
                    "duration": "DAY",
                    "price": price,
                    "quantity": quantity,
                }

                order_id = obj.placeOrder(order_params)
                logger.debug(f"Order ID: {order_id}")

                return JsonResponse({'status': 'success', 'order_id': order_id})

        except Exception as e:
            logger.error(f"Error in place_option_order: {str(e)}")
            return JsonResponse({'error': 'Failed to place order'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_symbol_token(api_client, symbol, strike_price, option_type):
    try:
        # Fetch the instrument list
        instruments = api_client.getInstruments("NFO")
        for instrument in instruments:
            if (instrument['symbol'] == symbol and
                instrument['strike'] == strike_price and
                instrument['instrumenttype'] == option_type):
                return instrument['token']
    except Exception as e:
        logger.error(f"Error in get_symbol_token: {str(e)}")
    return None





# ------------------------------------------------------------------------
# import requests
# import pyotp
# from django.http import JsonResponse
# from .models import SYMBOL, ind_clientDT, Client_SYMBOL_QTY
# from SmartApi import SmartConnect

# def initialize_connection(client_id):
#     try:
#         # Fetch the client's credentials from the database
#         client = ind_clientDT.objects.get(client_id=client_id)
#         print(f"Fetched client: {client}")  # Debugging
#     except ind_clientDT.DoesNotExist:
#         print("Client does not exist")
#         return None, None
    
#     api_key = client.api_key
#     client_code = client.client_id
#     password = client.password
#     secret_key = client.secret_key

#     print(f"API Key: {api_key}, Client Code: {client_code}, Password: {password}, Secret Key: {secret_key}")  # Debugging

#     # Generate the latest TOTP using pyotp
#     totp = pyotp.TOTP(secret_key).now()
#     print(f"Generated TOTP: {totp}")  # Debugging

#     # Initialize the SmartConnect object
#     obj = SmartConnect(api_key=api_key)
#     try:
#         # Generate session with Angel One
#         data = obj.generateSession(client_code, password, totp)
#         print(f"Session Data: {data}")  # Debugging
#         return obj, data['data']['refreshToken']
#     except Exception as e:
#         print(f"Error initializing connection: {e}")
#         return None, None

# def fetch_live_history(request):
#     # client_id = request.GET.get('client_id')
#     client_id = 1  # Example client_id, replace with dynamic value as needed
#     if not client_id:
#         return JsonResponse({"error": "Client ID is required"}, status=400)

#     obj, refreshToken = initialize_connection(client_id)
#     if not obj or not refreshToken:
#         return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."})

#     # Your Angel One API credentials and endpoint
#     api_url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/details/"
#     headers = {
#         "Content-Type": "application/json",
#         "X-API-KEY": obj.api_key,
#         "Authorization": f"Bearer {refreshToken}"
#     }
    
#     # Example: fetch data for a specific order
#     # Replace 'unique_order_id' with actual order ID
#     unique_order_id = "240620101316475"
#     response = requests.get(f"{api_url}{unique_order_id}", headers=headers)
    
#     if response.status_code == 200:
#         try:
#             data = response.json().get('data', {})
#             # Parse the response data and transform it to match your table's structure
#             live_data = [
#                 {
#                     "signal": data.get("signal", "-"),
#                     "signalTime": data.get("updatetime", "-"),
#                     "symbol": data.get("tradingsymbol", "-"),
#                     "strat": "NEUTRON1",  # Example static value, replace as necessary
#                     "type": data.get("transactiontype", "-"),
#                     "quantity": data.get("quantity", "-"),
#                     "entryPrice": data.get("price", "-"),
#                     "exitPrice": data.get("averageprice", "-"),
#                     "pnl": None,  # Placeholder, calculate P&L if possible
#                     "cumulativePnL": None  # Placeholder, calculate cumulative P&L if possible
#                 }
#             ]
#             return JsonResponse(live_data, safe=False)
#         except ValueError:
#             return JsonResponse({"error": "Failed to parse JSON response from Angel One API"}, status=500)
#     else:
#         return JsonResponse({"error": "Failed to fetch data from Angel One API", "status_code": response.status_code}, status=response.status_code)

# trading/utils.py
# trading/utils.py
# accounts/utils.py





# ====================== client_detail =========================

def client_detail(request):
    client = ind_clientDT.objects.all()

    return render(request, 'client_detail.html', {'client': client})


# ====================== edit_client =========================
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ind_clientDTForm

@csrf_protect
def edit_client(request, clint_id):
    client = ind_clientDT.objects.get(clint_id=clint_id)
    if request.method == 'POST':
        form = ind_clientDTForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_detail')
    else:
        form = ind_clientDTForm(instance=client)
    return render(request, 'edit_client.html', {'form': form})







'''
=====================================================================================================================================


=====================================================================================================================================
'''

from django.shortcuts import render, redirect
from django.http import HttpResponse
from urllib.parse import urlparse, parse_qs
from SmartApi import SmartConnect
from django.shortcuts import redirect, HttpResponse
from urllib.parse import urlparse, parse_qs


# Initial redirect to SmartAPI login
def redirect_to_smartapi_login(request):
    user_id = request.session.get('clint_id')
    client_user = ind_clientDT.objects.get(clint_id=user_id)
    api_key = client_user.api_key # Replace with your actual API key
    redirect_url = f"https://smartapi.angelbroking.com/publisher-login?api_key={api_key}"
    return redirect(redirect_url)

from django.shortcuts import get_object_or_404
def handle_smartapi_redirect(request):
    if 'clint_id' in request.session:
        user_id = request.session.get('clint_id')
        client_user = ind_clientDT.objects.get(clint_id=user_id)
        full_url = request.build_absolute_uri()
        # Parse the URL and extract query parameters
        parsed_url = urlparse(full_url)
        query_params = parse_qs(parsed_url.query)
         
        auth_token = query_params.get('auth_token', [None])[0]
        feed_token = query_params.get('feed_token', [None])[0]
        refresh_token = query_params.get('refresh_token', [None])[0]
        
        if client_user.Term_condition == True:
            if auth_token and feed_token and refresh_token:
                # Get the client record
                client = client_user #get_object_or_404(ind_clientDT, clint_id=client_id)

                # Save the tokens in the client record
                client.clint_plane = 'Live'
                client.auth_token = auth_token
                client.feed_token = feed_token
                client.refresh_token = refresh_token
                client.save()
                update_login_info(request,user_id)
            # return HttpResponse('done')
                # Redirect to dashboard or any other desired page
                return redirect('/home/')  # Replace 'dashboard' with your actual dashboard URL name
            else:
                update_login_info(request,user_id)
                return HttpResponse("Login failed", status=401)
        else:
            messages.error(request, "Please accept term and condition")
            return redirect('/home/')      
    else:
        messages.error(request, 'Pls Login')
        return redirect('/') 
 
import logging
logger = logging.getLogger(__name__)

def update_login_info(request,user_id):
   
    try:
        client = ind_clientDT.objects.get(clint_id = user_id)
        client.ip_address = get_client_ip(request)
        client.login_date_time = timezone.now()
        client.save()
    except ind_clientDT.DoesNotExist:
        logger.error(f"Client with email {user_id} does not exist.")


def get_client_ip(request):
    # Check for IP address from different headers
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('HTTP_X_REAL_IP')
        if ip:
            ip = ip.strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
    return ip

    
    
    
    

def off(request):
    print('run off')
    user_id = request.session.get('clint_id')
    client_user = ind_clientDT.objects.get(clint_id=user_id)
    client_user.clint_plane = 'Demo'
    client_user.save()
    return redirect('client_dashbord')
  #  return HttpResponse('run')
  
def smartapi_callback(request):
    auth_token = request.GET.get('auth_token')
    feed_token = request.GET.get('feed_token')
    refresh_token = request.GET.get('refresh_token')
    return redirect('/dashbord')
  
  
  
  
  
# ----------------------------------------------------------------------------  
# utils.py

# views.py

from django.shortcuts import render, redirect
from .models import ClientSignal, SYMBOL, OrderAngelOne
from pyotp import TOTP
import os
from SmartApi import SmartConnect  # Assuming this is your API integration module

def place_order(request):
    if request.method == 'POST':
        signal_id = request.POST.get('signal_id')  # Assuming you pass signal ID in the form
        signal = ClientSignal.objects.get(pk=signal_id)
        
        try:
            # Replace with your Angel One API integration logic
            api_key = "z2nnckx5"
            client_id = "K436935"
            password = "3547"
            secret_key = "KRXJPF2JYG5NJBCI2IC46TIAZ4"

            # Initialize SmartConnect with API credentials
            obj = SmartConnect(api_key=api_key)
            data = obj.generateSession(client_id=client_id, password=password, api_secret=secret_key)
            feed_token = obj.getfeedToken()

            # Prepare order parameters based on signal
            order_params = {
                "tradingsymbol": signal.SYMBOL.SYMBOL,
                "symboltoken": signal.SYMBOL.symbol_token,
                "transactiontype": "BUY" if signal.TYPE == "BUY_ENTRY" else "SELL",
                "exchange": "NSE",  # Example exchange (modify as per your requirement)
                "ordertype": "LIMIT",  # Example order type
                "producttype": "INTRADAY",  # Example product type
                "duration": "DAY",  # Example duration
                "price": signal.ENTRY_PRICE + 0.05,  # Example price calculation
                "triggerprice": signal.ENTRY_PRICE,  # Example trigger price
                "quantity": signal.QUANTITY
            }

            # Place order
            response = obj.placeOrder(order_params)
            order_id = response['data']['orderid']  # Adjust as per API response structure

            # Save order details in database
            OrderAngelOne.objects.create(
                clint=request.user.username,  # Adjust as per your user model
                symbol=signal.SYMBOL.SYMBOL,
                tradingsymbol=order_params['tradingsymbol'],
                symboltoken=order_params['symboltoken'],
                transaction_type=order_params['transactiontype'],
                order_type=order_params['ordertype'],
                quantity=order_params['quantity'],
                segment_type=order_params['exchange'],  # Example segment type
                squareoff=0.0,  # Example square off
                stoploss=0.0,  # Example stop loss
                price=order_params['price'],
                order_id=order_id
            )

            # Update signal with live_order_id
            signal.live_order_id = order_id
            signal.save()

            return redirect('order-success')  # Redirect to success page after order placement
        except Exception as e:
            # Handle exceptions or errors
            print(f"Error placing order: {str(e)}")
            return redirect('order-failed')  # Redirect to failure page
    else:
        return redirect('home')  # Redirect to home if not POST request


from django.shortcuts import render

def order_success(request):
    return render(request, 'order_success.html')

def order_failed(request):
    return render(request, 'order_failed.html')







# ----------------------------------------------------------------------
# stop_loss_script.py
  # Import the initialization function
import pyotp
from SmartApi import SmartConnect

def initialize_connection2(clint_id=None):
    if clint_id:
        # Fetch client credentials from the database
        client = ind_clientDT.objects.get(clint_id=clint_id)
        api_key = client.api_key
        client_id = client.client_id
        password = client.password
        secret_key = client.totp  # Time-based One Time Password if required
    else:
        # Your Angel One API credentials
        api_key = "z2nnckx5"
        client_id = "K436935"
        password = "3547"
        secret_key = "KRXJPF2JYG5NJBCI2IC46TIAZ4"  # Replace with your actual TOTP secret key

    # Generate the latest TOTP using pyotp
    totp = pyotp.TOTP(secret_key).now()

    # Initialize the SmartConnect object
    obj = SmartConnect(api_key=api_key)
    try:
        # Generate session with Angel One
        data = obj.generateSession(client_id, password, totp)
        return obj, data['data']['refreshToken']
    except Exception as e:
        print(f"Error initializing connection: {e}")
        return None, None




from .models import SYMBOL

def token_lookup(ticker, exchange="NFO"):
    try:
        instrument = SYMBOL.objects.get(SYMBOL=ticker, exch_seg=exchange)
        return instrument.symbol_token
    except SYMBOL.DoesNotExist:
        return None


def get_ltp(obj, symboltoken, tradingsymbol, exchange):
    try:
        ltp_data = obj.ltpData(exchange, tradingsymbol, symboltoken)
        ltp = ltp_data['data']['ltp']
        return ltp
    except Exception as e:
        print(f"Error fetching LTP: {e}")
        return None


# def get_valid_symbol_token(tradingsymbol, exchange='NFO'):
#     try:
#         # Assuming 'obj' is your SmartConnect object initialized with valid credentials
#         symbol_data = obj.searchSymbol(exchange, tradingsymbol)
#         for symbol in symbol_data:
#             if symbol['tradingsymbol'] == tradingsymbol:
#                 return symbol['symboltoken']
#         return None
#     except Exception as e:
#         print(f"Error fetching symbol token: {e}")
#         return None



from .models import SYMBOL, ind_clientDT, OrderAngelOne

# Updated order placement function
def place_sl_limit_order(obj, ticker, transaction_type, price, quantity, exchange="NFO"):
    symbol_token = token_lookup(ticker, exchange)
    if not symbol_token:
        print("Invalid symbol token. Order cannot be placed.")
        return None

    order_params = {
        "variety": "STOPLOSS",
        "tradingsymbol": ticker,
        "transactiontype": transaction_type,
        "exchange": exchange,
        "ordertype": "STOPLOSS_LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": price + 0.05,  # Adjust as needed
        "triggerprice": price,
        "quantity": quantity,
        "symboltoken": symbol_token
    }

    try:
        response = obj.placeOrder(order_params)
        return response
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from pyotp import TOTP

from django.http import JsonResponse


from django.http import JsonResponse
from django.views.decorators.http import require_GET
def place_order_function(ticker, transaction_type, price, quantity, exchange):
    # Your order placement logic here
    # This function should return the order ID or None if order placement fails
    try:
        # Example logic to place order (replace with your actual implementation)
        # place_sl_limit_order(instrument_list, ticker, transaction_type, price, quantity, exchange)
        order_id = f"ORD-{ticker}-{transaction_type}-{quantity}"  # Example order ID
        return order_id
    except Exception as e:
        print(f"Error placing order: {e}")
        return None


@require_GET
def place_sl_limit_order(request):
    ticker = request.GET.get('ticker')
    transaction_type = request.GET.get('transaction_type')
    price = request.GET.get('price')
    quantity = request.GET.get('quantity')
    exchange = request.GET.get('exchange', 'NFO')  # Default to 'NFO' if not provided

    if not all([ticker, transaction_type, price, quantity]):
        return JsonResponse({'status': 'error', 'message': 'Missing parameters'}, status=400)

    # Call your order placement function here
    order_id = place_order_function(ticker, transaction_type, price, quantity, exchange)

    if order_id:
        return JsonResponse({'status': 'success', 'order_id': order_id})
    else:
        return JsonResponse({'status': 'error', 'message': 'Failed to place order'}, status=500)


def place_sl_market_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ticker = data.get('ticker')
        transaction_type = data.get('transaction_type')
        price = data.get('price')
        quantity = data.get('quantity')
        exchange = data.get('exchange', 'NFO')
        response = place_sl_market_order(ticker, transaction_type, price, quantity, exchange)
        return JsonResponse(response)


@csrf_exempt
def place_sl_market_order_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ticker = data.get('ticker')
        transaction_type = data.get('transaction_type')
        price = data.get('price')
        quantity = data.get('quantity')
        exchange = data.get('exchange', 'NFO')

        key_secret = open("key.txt","r").read().split()
        obj = SmartConnect(api_key=key_secret[0])
        obj.generateSession(key_secret[2], key_secret[3], TOTP(key_secret[4]).now())

        result = place_sl_market_order(obj, ticker, transaction_type, price, quantity, exchange)
        return JsonResponse({'result': result})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def place_options_order(clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss):
    print('Running options order placement function with parameters:', clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss)
    try:
        # Fetch symbol details
        sy = SYMBOL.objects.get(symbol_token=symbol_token)
        client = ind_clientDT.objects.get(clint_id=clint_id)
        
        # Initialize connection
        obj, refreshToken = initialize_connection2(clint_id)
        if not obj or not refreshToken:
            return {"error": "Failed to initialize connection. Please check your credentials and TOTP."}
        
        # Determine exchange based on segment type
        if segment_type == 'options':
            exchange = 'NFO'
        else:
            return {"error": "Invalid segment type for options order"}
        
        # Fetch the latest price
        symboltoken = sy.symbol_token
        SYMBOL_order = sy.SYMBOL_order
        ltp = get_ltp(obj, symboltoken, SYMBOL_order, exchange)
        
        if ltp is None:
            return {"error": "Failed to fetch the latest price. Please try again later."}
        
        # Get the lot size from the SYMBOL model
        lot_size = sy.lotsize
        print('lot_size =', lot_size, qty % lot_size)
        if lot_size is None:
            return {"error": "Lot size is not defined for this symbol."}
        
        # Validate quantity
        if qty % lot_size != 0:
            return {"error": f"Quantity is invalid. It should be in multiples of lot size {lot_size}."}
        
        # Prepare order parameters
        orderparams = {
            "variety": "NORMAL",
            "tradingsymbol": SYMBOL_order,
            "symboltoken": symboltoken,
            "transactiontype": s_type,
            "exchange": exchange,
            "ordertype": order_type,
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": ltp,
            "squareoff": squareoff,
            "stoploss": stoploss,
            "quantity": qty
        }
        print('Order parameters:', orderparams)
        
        # Place the order
        orderId = obj.placeOrder(orderparams)
        print('Order ID:', orderId)
        
        # Save the order details to the database
        if orderId is not None:
            order = OrderAngelOne(
                clint=client.clint_id,
                symbol=sy.SYMBOL,
                tradingsymbol=SYMBOL_order,
                symboltoken=symboltoken,
                transaction_type=s_type,
                order_type=order_type,
                quantity=qty,
                segment_type=segment_type,
                squareoff=squareoff,
                stoploss=stoploss,
                price=ltp,
                order_id=orderId
            )
            order.save()
            print('Order saved')
        
        return {"order_id": orderId, "price": ltp}
    
    except Exception as e:
        print(f"Error placing options order: {e}")
        return {"error": str(e)}



from django.shortcuts import render
from django.db.models import Subquery, Min
from django.http import JsonResponse
from .models import SYMBOL, ind_clientDT, Client_SYMBOL_QTY, OrderAngelOne

# Example constant definition (replace with your actual data)
instrument_list = [
    {"tradingsymbol": "RELIANCE-EQ", "symboltoken": "2885"},
    {"tradingsymbol": "TCS-EQ", "symboltoken": "2955"},
    # Add more instruments as needed
]

# Usage in your main function
def demo_Live_admin_message(request):
    symbols = SYMBOL.objects.filter(
        id__in=Subquery(
            SYMBOL.objects.values('SYMBOL').annotate(
                min_id=Min('id')
            ).values('min_id')
        ))
    
    if request.method == 'POST':
        print('run form post')
        symbol_token = request.POST.get('symbol')
        s_type = request.POST.get('s_type')
        order_type = request.POST.get('Order_type')
        segment_type = request.POST.get('segment_type')
        squareoff = request.POST.get('squareoff')
        stoploss = request.POST.get('stoploss')
        
        try:
            symbol = SYMBOL.objects.get(symbol_token=symbol_token)
        except SYMBOL.DoesNotExist:
            symbol = None

        if s_type in ['BUY', 'SELL'] and symbol:
            clients = ind_clientDT.objects.all()
            for client in clients:
                if client.clint_plane == 'Live':
                    group = client.client_Group
                    for group_symbol in group.symbols.all():
                        if str(group_symbol) == str(symbol.SYMBOL):
                            symbol_q = Client_SYMBOL_QTY.objects.filter(client_id=client.clint_id, SYMBOL=group_symbol)
                            for symbol_qty in symbol_q:
                                if symbol_qty.trade == 'on':
                                    qty = symbol_qty.QUANTITY
                                    order_id = None
                                    obj, _ = initialize_connection2(client.clint_id)  # Ensure client ID is passed
                                    if order_type in ['LIMIT', 'MARKET']:
                                        if segment_type == 'options':
                                            order_id = place_options_order(client.clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss)
                                        elif segment_type == 'cash':    
                                            order_id = place_order(client.clint_id, symbol_token, s_type, order_type, qty, segment_type, squareoff, stoploss)
                                    elif order_type in ['STOPLOSS_LIMIT', 'STOPLOSS_MARKET']:  
                                        if order_type == 'STOPLOSS_LIMIT':
                                            order_id = place_sl_limit_order(obj, symbol.SYMBOL, s_type, float(stoploss), qty)
                                        elif order_type == 'STOPLOSS_MARKET':
                                            order_id = place_sl_market_order(obj, symbol.SYMBOL, s_type, float(stoploss), qty)
                                            
                                    print('order_id = ', order_id)
                                else:
                                    print('trade off')
    
    dt = {
        'symbols': symbols,
    }
    return render(request, 'admin_place_order.html', dt)


def get_symbols(request):
    segment_type = request.GET.get('segment_type')
    symbol = request.GET.get('symbol')
    request.session['segment_type'] = segment_type
    if segment_type == 'cash':
        symbols = SYMBOL.objects.filter(exch_seg='NSE', SYMBOL=symbol).values('SYMBOL', 'symbol_token', 'SYMBOL_order')
    elif segment_type == 'options' or segment_type == 'futures':
        symbols = SYMBOL.objects.filter(exch_seg='NFO', SYMBOL=symbol).values('SYMBOL', 'symbol_token', 'SYMBOL_order')
    else:
        symbols = []

    return JsonResponse(list(symbols), safe=False)


from django.views.decorators.http import require_GET

@require_GET
def get_symbol_price(request):
    segment_type = request.session.get('segment_type')
    symbol_token = request.GET.get('symbol_token')
    
    if not symbol_token:
        return JsonResponse({"error": "symbol_token is required"}, status=400)
    
    try:
        sy = SYMBOL.objects.get(symbol_token=symbol_token)
        obj, refreshToken = initialize_connection2()
        
        if not obj or not refreshToken:
            return JsonResponse({"error": "Failed to initialize connection. Please check your credentials and TOTP."}, status=500)
        
        # Determine exchange based on segment type
        if segment_type == 'cash':
            exchange = 'NSE'  # or 'BSE'
        elif segment_type in ['futures', 'options']:
            exchange = 'NFO'
        else:
            return JsonResponse({"error": "Invalid segment type"}, status=400)
        
        symboltoken = sy.symbol_token
        SYMBOL_order = sy.SYMBOL_order

        ltp = get_ltp2(obj, symboltoken, SYMBOL_order, exchange)
        
        if ltp is None:
            return JsonResponse({"error": "Failed to fetch the latest price. Please try again later."}, status=500)
        
        Open = ltp['open']
        high = ltp['high']
        low = ltp['low']
        close = ltp['close']
        ltp = ltp['ltp']
        symbol_price = f'Price: {ltp}, Open: {Open}, High: {high}, Low: {low}, Close: {close}'

        return JsonResponse({'price': symbol_price})
    
    except SYMBOL.DoesNotExist:
        return JsonResponse({"error": "Symbol not found"}, status=404)
    
    except Exception as e:
        # Log the error for debugging purposes
        print(f'Error: {e}')
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)


def initialize_connection2():
    # Your Angel One API credentials
    api_key = "z2nnckx5"
    client_id = "K436935"
    password = "3547"
    secret_key = "KRXJPF2JYG5NJBCI2IC46TIAZ4"  # Replace with your actual TOTP secret key

    # Generate the latest TOTP using pyotp
    totp = pyotp.TOTP(secret_key).now()

    # Initialize the SmartConnect object
    obj = SmartConnect(api_key=api_key)
    try:
        # Generate session with Angel One
        data = obj.generateSession(client_id, password, totp)
        return obj, data['data']['refreshToken']
    except Exception as e:
        print(f"Error initializing connection: {e}")
        return None, None


# ============================ Get Latest Price (LTP) ===================================
def get_ltp2(obj, symboltoken, SYMBOL_order, exchange):
    try:
        ltp_data = obj.ltpData(exchange, SYMBOL_order, symboltoken)
        print(ltp_data)
        return ltp_data['data']
    except Exception as e:
        print(f"Error fetching LTP: {e}")
        return None
    
    
    
        
    
    
    
    
    
# import schedule
# import time
# import requests
# import logging

# logging.basicConfig(level=logging.INFO)

# def job():
#     try:
#         # Example: Place an SL limit order for Nifty options
#         order_data = {
#             'ticker': 'NIFTY23JUL17600CE',
#             'transaction_type': 'BUY',
#             'price': 150,
#             'quantity': 75,
#             'exchange': 'NFO'
#         }
#         response = requests.post('http://127.0.0.1:8000/place_sl_limit_order/', json=order_data)
#         logging.info(f"SL Limit Order Response: {response.json()}")

#         # Example: Place an SL market order for Bank Nifty options
#         order_data = {
#             'ticker': 'BANKNIFTY23JUL40000PE',
#             'transaction_type': 'BUY',
#             'price': 200,
#             'quantity': 25,
#             'exchange': 'NFO'
#         }
#         response = requests.post('http://127.0.0.1:8000/place_sl_market_order/', json=order_data)
#         logging.info(f"SL Market Order Response: {response.json()}")

#     except requests.exceptions.RequestException as e:
#         logging.error(f"Error placing order: {e}")

# schedule.every().day.at("09:15").do(job)  # Adjust the time as per your requirement

# while True:
#     schedule.run_pending()
#     time.sleep(1)

    




# ====================================================================================
# ==================================  MT4 panel =======================================
# ========================================================================================
import requests
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# from .models import Trade, SYMBOL, ind_clientDT, Client_SYMBOL_QTY
from SmartApi import SmartConnect  # Make sure to import SmartConnect

logger = logging.getLogger(__name__)

# Global variable to store instrument tokens
instrument_dict = {}

# Function to fetch instruments
# def fetch_instruments(client):
#     global instrument_dict
#     url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
#     print(url)
#     response = requests.get(url)
#     print(response)
#     if response.status_code == 200:
#         instruments = response.json()
#         instrument_dict = {instrument['symbol']: instrument['token'] for instrument in instruments}
#         logger.info(f"Instrument list fetched successfully: {instrument_dict.keys()}")
#     else:
#         logger.error("Failed to fetch instrument list")

# # Fetch instruments at the start
# client_user = ind_clientDT.objects.values('api_key').first()
# if client_user:
#     api_key = client_user['api_key']
#     client = SmartConnect(api_key=api_key)
#     fetch_instruments(client)
#     print(fetch_instruments)

from django.http import HttpRequest

# client_user = ind_clientDT.objects.values('api_key').first()
# if client_user:
#     api_key = client_user['api_key']
#     client = SmartConnect(api_key=api_key)
#     fetch_instruments(client)
#     request = HttpRequest()
#     fetch_and_save_data(request)
    

@csrf_exempt
def receive_trade(request):
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Request headers: {request.headers}")
    logger.debug(f"Request body (raw): {request.body}")
    
    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8').rstrip('\x00')
            logger.debug(f"Request body (decoded): {body_unicode}")
            
            data = json.loads(body_unicode)
            logger.debug(f"Parsed data: {data}")

            trade_type = data.get('trade_type')
            symbol = data.get('symbol')
            price = data.get('price')
            lot_size = data.get('lot_size')

            if not trade_type or not symbol or price is None or lot_size is None:
                logger.error("Missing required fields")
                return JsonResponse({'status': 'fail', 'message': 'Missing required fields'}, status=400)

            # Save the trade to the database
            trade = Trade(trade_type=trade_type, symbol=symbol, price=price)
            trade.save()
            
            # Fetch the api_key and auth_token for all clients
            client_users = ind_clientDT.objects.values('api_key', 'auth_token')

            if not client_users:
                logger.error("No client users found")
                return JsonResponse({'status': 'fail', 'message': 'No client users found'}, status=400)

            # Iterate over each client and transfer the trade
            for client_user in client_users:
                api_key = client_user['api_key']
                auth_token = client_user['auth_token']
                
            #    transfer_trade_to_angel(trade, api_key, auth_token)

            response = {
                'status': 'success',
                'data': {
                    'trade_type': trade_type,
                    'symbol': symbol,
                    'price': price,
                    'lot_size': lot_size
                }
            }


            print('Trade data saved and transferred successfull and run place order all')
            place_order_all(request, trade, trade_type, symbol, price)
            logger.info("Trade data saved and transferred successfully")
            return JsonResponse(response)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            return JsonResponse({'status': 'fail', 'message': 'Invalid JSON'}, status=400)
    else:
        logger.error("Invalid request method")
        return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)

def get_symbol_token(symbol):
    symbol_token = SYMBOL.objects.get(SYMBOL_order = symbol)
    token = symbol_token.symbol_token
    print(symbol_token.symbol_token)
    if not token:
        logger.error(f"Symbol {token} does not exist in instrument_dict")
    return token

def transfer_trade_to_angel(trade, api_key, auth_token):
    try:
        # Initialize SmartAPI
        client = SmartConnect(api_key=api_key)
        
        # Set the access token directly
        client.setAccessToken(auth_token)

        # Determine order type
        trade_type = trade.trade_type
        symbol = trade.symbol
        price = trade.price
        lot_size = trade.lot_size

        if trade_type in ['Long_Entry', 'Short_Entry']:
            order_type = 'BUY'
        elif trade_type in ['Long_Exit', 'Short_Exit']:
            order_type = 'SELL'
        else:
            order_type = 'SELL'

        # Fetch the correct symbol token
        symbol_token = get_symbol_token(symbol)
        if not symbol_token:
            logger.error(f"Invalid symbol token for symbol: {symbol}")
            return

        # Place order on Angel Broking
        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": symbol_token,
            "transactiontype": order_type,
            "exchange": "NFO",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": price,
            "quantity": lot_size
        }

        response = client.placeOrder(order_params)
        print(response)
        logger.debug(f"Order response: {response}")

        # Ensure the response is parsed as JSON if it's a string
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse response JSON: {response}")
                return

        # Handle the response, checking if it's a dictionary
        if isinstance(response, dict) and 'status' in response:
            if response['status']:
                trade.status = 'executed'
                trade.save()
                logger.info(f"Trade executed successfully: {trade_type} {symbol} at {price}")
            else:
                error_message = response.get('message', 'Unknown error')
                logger.error(f"Failed to execute trade: {error_message}")
        else:
            logger.error(f"Unexpected response format: {response}")
    except Exception as e:
        logger.error(f"Error in transferring trade to Angel Broking: {str(e)}")

from django.shortcuts import render

def trade_list(request):
    if 'clint_id' in request.session:
        user_id = request.session.get('clint_id')
        today = datetime.now().date()  # Gets today's date
        trades = Trade.objects.filter(clint_id=user_id, timestamp__date=today)
        client_user = ind_clientDT.objects.get(clint_id=user_id)
        client = ind_clientDT.objects.filter(clint_id=user_id)
        dt = {
            'trades': trades,
            'client_user': client_user,
            'client': client,
        }
        return render(request, 'trade_list.html', dt)
    else:
        messages.error(request, 'Please log in.')
        return redirect('/')


from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import Trade, ind_clientDT

# def trade_list(request):
#     if 'clint_id' in request.session:
#         user_id = request.session.get('clint_id')
#         today = datetime.now().date()  # Gets today's date
#         trades = Trade.objects.filter(clint_id=user_id, timestamp__date=today)
#         client_user = ind_clientDT.objects.get(clint_id=user_id)
#         client = ind_clientDT.objects.filter(clint_id=user_id)
#         dt = {
#             'trades': trades,
#             'client_user': client_user,
#             'client': client,
#         }
#         return render(request, 'trade_list.html', dt)
#     else:
#         messages.error(request, 'Please log in.')
#         return redirect('/')




def trade_history(request):
    trades = Trade.objects.all().order_by('timestamp')
    trade_history = []
    cumulative_pnl = 0

    entry_trades = {}

    for trade in trades:
        if trade.trade_type in ['Long_Entry', 'Short_Entry']:
            # Store entry trades by symbol
            entry_trades[trade.symbol] = trade
        elif trade.trade_type in ['Long_Exit', 'Short_Exit']:
            entry_trade = entry_trades.pop(trade.symbol, None)
            if entry_trade:
                pnl = (trade.price - entry_trade.price) * trade.lot_size
                cumulative_pnl += pnl

                trade_history.append({
                    'signal': entry_trade.id,
                    'signal_time': entry_trade.timestamp,
                    'symbol': entry_trade.symbol,
                    'type': entry_trade.trade_type,
                    'quantity': entry_trade.lot_size,
                    'entry_price': entry_trade.price,
                    'exit_price': '-',
                    'pnl': '-',
                    'cumulative_pnl': cumulative_pnl
                })

                trade_history.append({
                    'signal': trade.id,
                    'signal_time': trade.timestamp,
                    'symbol': trade.symbol,
                    'type': trade.trade_type,
                    'quantity': trade.lot_size,
                    'entry_price': '-',
                    'exit_price': trade.price,
                    'pnl': pnl,
                    'cumulative_pnl': cumulative_pnl
                })

    return render(request, 'trade_history.html', {'trade_history': trade_history, 'total_cumulative_pnl': cumulative_pnl})

@csrf_exempt
def place_order_all(request, trade, trade_type, symbol, price):
    print('run all ')
    try:
        symbol_obj = SYMBOL.objects.get(SYMBOL_order=symbol)
    except SYMBOL.DoesNotExist:
        logger.error(f"Symbol {symbol} does not exist")
        return JsonResponse({'status': 'fail', 'message': 'Invalid symbol'}, status=400)

    clients = ind_clientDT.objects.filter(clint_plane='Live')
    for client in clients:
        print(client.clint_name_first)
        group = client.client_Group
        for group_symbol in group.symbols.all():
            print(group_symbol)
            if str(group_symbol) == str(symbol_obj.SYMBOL):
                print(group_symbol ,'==',symbol_obj.SYMBOL)
                symbol_qty = Client_SYMBOL_QTY.objects.filter(client_id=client.clint_id, SYMBOL=group_symbol).first()
                if symbol_qty and symbol_qty.trade == 'on':
                    qty = symbol_qty.QUANTITY
                    print('run next send_trade_to_angel_broking')
                    send_trade_to_angel_broking(trade, trade_type, symbol, price, client.auth_token, qty, client.clint_id, client.api_key , symbol_obj.SYMBOL )
                else:
                    logger.info(f"Trade is off for symbol: {symbol}")
    return JsonResponse({'status': 'success', 'message': 'Orders placed for all clients'}, status=200)

def send_trade_to_angel_broking(trade, trade_type, symbol, price, auth_token, qty, client_id, api_key, SYMBOL_m):
    try:
        client = SmartConnect(api_key=api_key)
        client.setAccessToken(auth_token)

        if trade_type in ['Long_Entry', 'Short_Entry']:
            order_type = 'BUY'
        elif trade_type in ['Long_Exit', 'Short_Exit']:
            order_type = 'SELL'
        else:
            order_type = 'SELL'

        symbol_token = get_symbol_token(symbol)
        if not symbol_token:
            logger.error(f"Invalid symbol token for symbol: {symbol}")
            return

        order_params = {
            "variety": "NORMAL",
            "tradingsymbol": symbol,
            "symboltoken": symbol_token,
            "transactiontype": order_type,
            "exchange": "NFO",
            "ordertype": "MARKET",
            "producttype": "INTRADAY",
            "duration": "DAY",
            "price": price,
            "quantity": qty
        }

        response = client.placeOrder(order_params)
        logger.debug(f"Order response: {response}")
        print(f'response == {response}')
        # Check if response is a string and log it for debugging
        # if isinstance(response, str):
        #     logger.error(f"Response is a string: {response}")
        #     return

        if response is not None:
            # Assuming 'orderid' is a key in the successful response
           

            # Save trade data to Trade model
            trade_record = Trade(
                trade_type=trade_type,
                symbol=symbol,
                price=price,
                lot_size=qty,
                status="Executed",
                clint_id=client_id,
                order_id=response
            )
            trade_record.save()

            # Save order details to OrderAngelOne model
            order_angel = OrderAngelOne(
                clint=client_id,
                symbol=SYMBOL_m,
                tradingsymbol=symbol,
                symboltoken=symbol_token,
                transaction_type=order_type,
                order_type="MARKET",
                quantity=qty,
                segment_type="NFO",
                squareoff=0,  # Set this appropriately if you have this data
                stoploss=0,   # Set this appropriately if you have this data
                price=price,
                order_id=response
            )
            order_angel.save()

            logger.info(f"Trade and order details saved successfully. Order ID: {response}")
        else:
            error_message = response.get('message', 'Unknown error')
            logger.error(f"Failed to execute trade: {error_message}")

    except Exception as e:
        logger.error(f"Error in transferring trade to Angel Broking: {str(e)}")
        print(e, '-------------------------send_trade_to_angel_broking--------------------------------')



# @csrf_exempt
# def place_order_all(request, trade, trade_type, symbol, price):
#     # try:
#     #     symbol_obj = SYMBOL.objects.get(SYMBOL_order=symbol)
#     # except SYMBOL.DoesNotExist:
#     #     logger.error(f"Symbol {symbol} does not exist")
#     #     return JsonResponse({'status': 'fail', 'message': 'Invalid symbol'}, status=400)

#     clients = ind_clientDT.objects.filter(clint_plane='Live')
#     for client in clients:
#         group = client.client_Group
#         for group_symbol in group.symbols.all():
#             # if str(group_symbol) == str(symbol_obj.SYMBOL):
#                 symbol_qty = Client_SYMBOL_QTY.objects.filter(client_id=client.clint_id, SYMBOL=group_symbol).first()
#                 if symbol_qty and symbol_qty.trade == 'on':
#                     qty = symbol_qty.QUANTITY
#                     send_trade_to_angel_broking(trade, trade_type, symbol, price, client.auth_token, qty, client.clint_id, client.api_key)
#                 else:
#                     logger.info(f"Trade is off for symbol: {symbol}")
#     return JsonResponse({'status': 'success', 'message': 'Orders placed for all clients'}, status=200)

# def send_trade_to_angel_broking(trade, trade_type, symbol, price, auth_token, qty, client_id, api_key):
#     try:
#         client = SmartConnect(api_key=api_key)
#         client.setAccessToken(auth_token)

#         if trade_type in ['Long_Entry', 'Short_Entry']:
#             order_type = 'BUY'
#         elif trade_type in ['Long_Exit', 'Short_Exit']:
#             order_type = 'SELL'
#         else:
#             order_type = 'SELL'

#         symbol_token = get_symbol_token(symbol)
#         # if not symbol_token:
#         #     logger.error(f"Invalid symbol token for symbol: {symbol}")
#         #     return

#         order_params = {
#             "variety": "NORMAL",
#             "tradingsymbol": symbol,
#             "symboltoken": symbol_token,
#             "transactiontype": order_type,
#             "exchange": "NFO",
#             "ordertype": "MARKET",
#             "producttype": "INTRADAY",
#             "duration": "DAY",
#             "price": price,
#             "quantity": qty
#         }

#         response = client.placeOrder(order_params)
#         print(response)
#         logger.debug(f"Order response: {response}")

#         if isinstance(response, str):
#             try:
#                 response = json.loads(response)
#             except json.JSONDecodeError:
#                 logger.error(f"Failed to parse response JSON: {response}")
#                 return

#         if isinstance(response, dict) and 'status' in response:
#             if response['status']:
#                 trade.status = 'executed'
#                 trade.save()
#                 logger.info(f"Trade executed successfully: {trade_type} {symbol} at {price}")
#             else:
#                 error_message = response.get('message', 'Unknown error')
#                 logger.error(f"Failed to execute trade: {error_message}")
#         else:
#             logger.error(f"Unexpected response format: {response}")
#     except Exception as e:
#         print(e,'-------------------------send_trade_to_angel_broking--------------------------------')
#         logger.error(f"Error in transferring trade to Angel Broking: {str(e)}")

    
    


def test_order(request):
    trade = None  # Replace with your trade object
    trade_type = 'Long_Entry'
    symbol = 'BANKNIFTY24JUL2451600CE'
    price = 259.95
    auth_token = 'your_auth_token'
    qty = 45
    # Place the order and capture the response
    order_response = place_order_all(request, trade, trade_type, symbol, price)

    # Return the response as a JSON response
    return order_response




# def client_status_admin(request):
#     if 'admin_id' in request.session:
#         admin_id = request.session.get('admin_id')
#         client = ind_clientDT.objects.all()
#     #  return render(request,'client_status.html',{'client':client})
#         return render(request,'admin/client_status_admin.html',{'client':client})
#     else:
#         return redirect('/ind_admin/?msg=Login')


# def subadmin_list(request):
#     if 'admin_id' in request.session:
#         subadmins = ind_subadminDT.objects.all()
#         return render(request, 'admin/subadmin_list.html', {'subadmins': subadmins})    
#     else:
#         return redirect('/ind_admin/?msg=Login')


# def subadmin_create(request):
#     if 'admin_id' in request.session:
#         if request.method == 'POST':
#             form = SubadminForm(request.POST)
#             if form.is_valid():
#                 form.save()
#                 return redirect('subadmin_list')
#         else:
#             form = SubadminForm()

#         return render(request, 'admin/subadmin_form.html', {'form': form}) 
#     else:
#         return redirect('/ind_admin/?msg=Login')    
from django.db.models import Sum, Count, Q
from django.utils import timezone
  
    
def homes(request):
    if 'clint_id' in request.session:
        user_id = request.session.get('clint_id')
        client_user = ind_clientDT.objects.get(clint_id=user_id)
        client = ind_clientDT.objects.filter(clint_id=user_id)
        api_key = client_user.api_key
        auth_token = client_user.auth_token
        refresh_token = client_user.refresh_token

        # if not auth_token or not api_key or not refresh_token:
        #     return redirect('redirect_to_smartapi_login')

        obj = SmartConnect(api_key=api_key)
        obj.setAccessToken(auth_token)

        try:
            fund_response = obj.rmsLimit()
            print(fund_response)  # Debug: Print the fund response
            if fund_response['status'] == True:
                funds = fund_response['data']['net']
            else:
                funds = f"Unable to fetch funds: {fund_response.get('message', 'Unknown error')}"
        except Exception as e:
            funds = f"Exception: {str(e)}"

    #    trades = Trade.objects.filter(clint_id=user_id).order_by('timestamp')
        today = date.today()
        # Filter trades for the current date
        trades = Trade.objects.filter(clint_id=user_id, timestamp__date=today).order_by('timestamp')

        long_entries = [trade for trade in trades if trade.trade_type == 'Long_Entry']
        short_entries = [trade for trade in trades if trade.trade_type == 'Short_Entry']
        long_exits = [trade for trade in trades if trade.trade_type == 'Long_Exit']
        short_exits = [trade for trade in trades if trade.trade_type == 'Short_Exit']
        
        profitable_trades = 0
        loss_trades = 0
        total_cumulative_pnl = 0
        total_trades = 0
        
        while long_entries and long_exits:
            entry_trade = long_entries.pop(0)
            exit_trade = long_exits.pop(0)
            pnl = (exit_trade.price - entry_trade.price) * entry_trade.lot_size
            total_cumulative_pnl += pnl
            total_trades += 1
            if pnl > 0:
                profitable_trades += 1
            else:
                loss_trades += 1
        
        while short_entries and short_exits:
            entry_trade = short_entries.pop(0)
            exit_trade = short_exits.pop(0)
            pnl = (entry_trade.price - exit_trade.price) * entry_trade.lot_size
            total_cumulative_pnl += pnl
            total_trades += 1
            if pnl > 0:
                profitable_trades += 1
            else:
                loss_trades += 1
        
        trade_accuracy = (profitable_trades / total_trades) * 100 if total_trades > 0 else 0
        

        # Debug: Print calculated values
        # print("Profitable Trades:", profitable_trades)
        # print("Loss Trades:", loss_trades)
        # print("Total Cumulative PnL:", total_cumulative_pnl)
        # print("Trade Accuracy:", trade_accuracy)
        dt = {
            'profitable_trades': profitable_trades,
            'loss_trades': loss_trades,
            'total_cumulative_pnl': total_cumulative_pnl,
            'trade_accuracy': trade_accuracy,
            'funds': funds,
            'client_user': client_user,
            'term_condition': client_user.Term_condition,
        }

        return render(request, 'homes.html', dt)
    else:
        messages.error(request, 'Please Login')
        return redirect('/')
    


# def HOME(request):
#     if 'clint_id' in request.session:
#         user_id = request.session.get('clint_id')
#         client_user = ind_clientDT.objects.get(clint_id=user_id)
#         client = ind_clientDT.objects.filter(clint_id = user_id)
#         api_key = client_user.api_key
#         auth_token = client_user.auth_token
#         refresh_token = client_user.refresh_token

#         if not auth_token or not api_key or not refresh_token:
#             return redirect('redirect_to_smartapi_login')

#         obj = SmartConnect(api_key=api_key)
#         obj.setAccessToken(auth_token)
        
#         try:
#             # Use the getRMS method to fetch fund data
#             fund_response = obj.rmsLimit()
#             print(fund_response)  # Debug: Print the fund response
#             if fund_response['status'] == True:
#                 funds = fund_response['data']['net']
#             else:
#                 funds = f"Unable to fetch funds: {fund_response.get('message', 'Unknown error')}"
#         except Exception as e:
#             funds = f"Exception: {str(e)}"

#         trades = Trade.objects.all().order_by('timestamp')
#         profitable_trades = 0
#         loss_trades = 0
#         total_cumulative_pnl = 0
#         total_trades = 0

#         entry_trades = {}

#         for trade in trades:
#             if trade.trade_type in ['Long_Entry', 'Short_Entry']:
#                 entry_trades[trade.symbol] = trade
#             elif trade.trade_type in ['Long_Exit', 'Short_Exit']:
#                 entry_trade = entry_trades.pop(trade.symbol, None)
#                 if entry_trade:
#                     if trade.price is not None and entry_trade.price is not None and trade.lot_size is not None:
#                         if trade.trade_type == 'Long_Exit':
#                             pnl = (trade.price - entry_trade.price) * trade.lot_size
#                         else:
#                             pnl = (entry_trade.price - trade.price) * trade.lot_size
#                         total_cumulative_pnl += pnl

#                         if pnl > 0:
#                             profitable_trades += 1
#                         elif pnl < 0:
#                             loss_trades += 1

#                         total_trades += 1

#         trade_accuracy = (profitable_trades / total_trades) * 100 if total_trades > 0 else 0

#         dt = {
#             'profitable_trades': profitable_trades,
#             'loss_trades': loss_trades,
#             'total_cumulative_pnl': total_cumulative_pnl,
#             'trade_accuracy': trade_accuracy,
#             'funds': funds,
#             'client_user':client_user
#         }

#         return render(request, 'HOME.html', dt)
#     else:
#         messages.error(request, 'Pls Login')
#         return redirect('/') 
    


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Notification
from .forms import NotificationForm

def send_notification(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('send_notification')
    else:
        form = NotificationForm()
    return render(request, 'send_notification.html', {'form': form})

def get_notifications(request):
    notifications = Notification.objects.all().order_by('-created_at')[:5]  # Limit to latest 5 notifications
    data = [{'message': n.message, 'created_at': n.created_at} for n in notifications]
    return JsonResponse(data, safe=False)



    
    
    
# -------------------------------------client side --------------------------------------------    

    
from datetime import date
from django.shortcuts import render, redirect
from .models import Trade, ind_clientDT

def client_trade_history(request):
    if 'clint_id' in request.session:
        if 'msg' in request.GET:
            msg = request.GET['msg']
        else:
            msg = None 
        user_id = request.session.get('clint_id')
        client_user = ind_clientDT.objects.get(clint_id=user_id)

      
        api_key = client_user.api_key
        auth_token = client_user.auth_token
        refresh_token = client_user.refresh_token

        # if not auth_token or not api_key or not refresh_token:
        #     return redirect('redirect_to_smartapi_login')

        obj = SmartConnect(api_key=api_key)
        obj.setAccessToken(auth_token)

        try:
            fund_response = obj.rmsLimit()
            print(fund_response)  # Debug: Print the fund response
            if fund_response['status'] == True:
                funds = fund_response['data']['net']
            else:
                funds = f"Unable to fetch funds: {fund_response.get('message', 'Unknown error')}"
        except Exception as e:
            funds = f"Exception: {str(e)}"


      
        today = date.today()
        # Filter trades for the current date
     
        tr = Trade.objects.filter(clint_id=user_id, timestamp__date=today).order_by('timestamp')
      
        trade_history = []
        cumulative_pnl = 0

        entry_trades = {}

        for trade in tr:
            if trade.trade_type in ['Long_Entry', 'Short_Entry']:
                # Store entry trades by symbol
                entry_trades[trade.symbol] = trade
            elif trade.trade_type in ['Long_Exit', 'Short_Exit']:
                entry_trade = entry_trades.pop(trade.symbol, None)
                if entry_trade:
                    pnl = (trade.price - entry_trade.price) * trade.lot_size
                    cumulative_pnl += pnl

                    trade_history.append({
                        'signal': entry_trade.id,
                        'signal_time': entry_trade.timestamp,
                        'symbol': entry_trade.symbol,
                        'type': entry_trade.trade_type,
                        'quantity': entry_trade.lot_size,
                        'entry_price': entry_trade.price,
                        'exit_price': '-',
                        'pnl': '-',
                        'cumulative_pnl': cumulative_pnl
                    })

                    trade_history.append({
                        'signal': trade.id,
                        'signal_time': trade.timestamp,
                        'symbol': trade.symbol,
                        'type': trade.trade_type,
                        'quantity': trade.lot_size,
                        'entry_price': '-',
                        'exit_price': trade.price,
                        'pnl': pnl,
                        'cumulative_pnl': cumulative_pnl
                    })


        dt = {
            'trade_history': trade_history, 
            'cumulative_pnl': cumulative_pnl,
            'client_user': client_user,

            'funds': funds,
            'client_user': client_user,
            'term_condition': client_user.Term_condition,
        }
 
        return render(request, 'trade_history_client.html', dt)
    else:
        return redirect('/')
       
    

def client_status(request):
    if 'clint_id' in request.session:
        user_id = request.session.get('clint_id')
        try:
            client_user = ind_clientDT.objects.get(clint_id=user_id)
            clients = ind_clientDT.objects.filter(clint_id=user_id)
            
            client_symbol_qty = Client_SYMBOL_QTY.objects.filter(client_id=user_id).first()

            st = ClientStatus.objects.filter(clint_id = user_id).order_by('-id')
           

            dt = {
                'client': clients,
                'client_user': client_user,
                'client_symbol_qty':client_symbol_qty,
                'st':st
               
            }
            return render(request, 'client_status.html', dt)
        except ind_clientDT.DoesNotExist:
            messages.error(request, 'Client does not exist.')
            return redirect('/')
    else:
        messages.error(request, 'Please log in.')
        return redirect('/')   

def update_by_client(request):
    if 'clint_id' in request.session:
        user_id = request.session.get('clint_id')
        client_user = ind_clientDT.objects.get(clint_id=user_id)
        client_user.updated_by = 'update by client' 
        client_user.save()

        ClientStatus.objects.create(
            sub_admin_id = client_user.sub_admin_id,
            clint_id = user_id,
            name = f"{client_user.clint_name_first} {client_user.clint_name_last}" ,
            service_name =client_user.service_name,
            quantity = None,
            strategy = client_user.strategies,
            trading =client_user.clint_plane,
            ip_address = client_user.ip_address,
            updated_by = 'update by client',
        )
    
def client_status_admin(request):
   
    client = ind_clientDT.objects.all()
    #  return render(request,'client_status.html',{'client':client})
    return render(request,'client_status_admin.html',{'client':client})    


# views.py
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ind_clientDT


@login_required
def fetch_live_data(request):
    try:
        client = get_object_or_404(ind_clientDT, clint_email=request.user.email)
        
        api_key = client.api_key
        auth_token = client.auth_token
        refresh_token = client.refresh_token
        feed_token = client.feed_token
        
        obj = SmartConnect(api_key=api_key)
        obj.setAccessToken(auth_token)
        obj.setRefreshToken(refresh_token)
        obj.setFeedToken(feed_token)
        
        token = '26009'  # Nifty 50 token, example
        live_data = obj.ltpData('NSE', token)
        
        print("Live Data: ", live_data)  # Debug statement
        
        return JsonResponse(live_data)
    except Exception as e:
        print("Error: ", e)  # Debug statement
        return JsonResponse({'error': str(e)})

def live_chart(request):
    return render(request , 'live_chart.html')


import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from datetime import datetime
from .models import Trade, ind_clientDT

@csrf_exempt
def fetch_order_status(request):
    if request.method == 'POST':
        # unique_order_id = request.POST.get('05ebf91b-bea4-4a1d-b0f2-4259606570e3')
        unique_order_id = "05ebf91b-bea4-4a1d-b0f2-4259606570e3"
        if not unique_order_id:
            return JsonResponse({'error': 'uniqueOrderId is required'}, status=400)

        if 'clint_id' in request.session:
            user_id = request.session.get('clint_id')
            today = datetime.now().date()  # Gets today's date
            trades = Trade.objects.filter(clint_id=user_id, timestamp__date=today)
            client_user = ind_clientDT.objects.get(clint_id=user_id)
            client = ind_clientDT.objects.filter(clint_id=user_id)

            # Your Angel One API credentials
            api_key = "your_api_key"
            client_code = "your_client_code"
            session_token = "your_session_token"

            api_url = f"https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/details"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {session_token}",
                'X-ClientCode': client_code,
                'X-APIKey': api_key,
            }
            payload = {
                "clientcode": client_code,
                "orderno": unique_order_id
            }

            # Make the API request
            response = requests.post(api_url, headers=headers, json=payload)
            dt = {
                'trades': trades,
                'client_user': client_user,
                'client': client,
            }

            if response.status_code == 200:
                data = response.json()
                if data['status']:
                    return JsonResponse(data['data'])
                else:
                    return JsonResponse({'error': 'Failed to fetch order status', 'message': data.get('message', '')}, status=400)
            else:
                return render(request, 'client_broker_response.html', dt)
        else:
            messages.error(request, 'Please log in.')
            return redirect('/')
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


from django.views.decorators.http import require_POST


@require_POST
def Reset_Password(request):
    print('Reset_Password')
    if 'clint_id' in request.session:
        user_id = request.session.get('clint_id')
        try:
            client_user = ind_clientDT.objects.get(clint_id=user_id)
        except ind_clientDT.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})

        new_password = request.POST.get('new_password')
        if not new_password:
            return JsonResponse({'success': False, 'message': 'Password cannot be empty.'})

        client_user.clint_password = new_password
        client_user.save()
        return JsonResponse({'success': True})
        
    return JsonResponse({'success': False, 'message': 'User not logged in.'})


@require_POST
def Accept_Terms(request):
    if 'clint_id' in request.session:
        user_id = request.session.get('clint_id')
        try:
            client_user = ind_clientDT.objects.get(clint_id=user_id)
        except ind_clientDT.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})

        if not client_user.Term_condition:
            client_user.Term_condition = True
            client_user.save()
            # try:
            #     subject = f'Dear {client_user.clint_name_first} {client_user.clint_name_last}'
            #     message = "Thanks for Accepting the terms and conditions"
            #     email_from = settings.EMAIL_HOST_USER
            #     recipient_list = [client_user.clint_email]
            #     send_mail(subject, message, email_from, recipient_list)
            # except Exception as e:
            #     logger.error(f"Error sending email: {str(e)}")
            #     return JsonResponse({'success': False, 'message': 'Email not sent.'})

            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'message': 'Terms already accepted.'})

    return JsonResponse({'success': False, 'message': 'User not logged in.'})



