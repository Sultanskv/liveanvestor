from django.shortcuts import render , HttpResponse ,redirect
from django.contrib import messages
from .models import sub_adminDT 
from django.views.decorators.csrf import csrf_protect
from accounts.models import ind_clientDT , BROKERS , GROUP , Strategy

# Create your views here.
@csrf_protect
def subadmin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            subadmin = sub_adminDT.objects.get(subadmin_email=email)
            if subadmin.subadmin_password == password:
                
                # Store session data
                request.session['subadmin_id'] = subadmin.subadmin_id

                return redirect('subadmin_dashboard')  # Change 'home' to your desired redirect URL
              #  return HttpResponse('login')
            else:
                messages.error(request, 'Invalid password')
        except sub_adminDT.DoesNotExist:
            messages.error(request, 'Invalid email')
    return render(request, 'subadmin/login.html')

def subadmin_logout(request):
    subadmin_id = request.session.get('subadmin_id')
    del request.session['subadmin_id']
    return redirect('subadmin_login')

def subadmin_dashboard(request):
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
        print(subadmin_id)
        return render(request,'subadmin/subadmin_dashboard.html')
    else:
        messages.error(request, 'Pls Login')
        return redirect('subadmin_login')  # Change 'home' to your desired redirect URL
    

def subadmin_clients(request):
    
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
        client = ind_clientDT.objects.filter(sub_admin_id = subadmin_id)

        return render(request, 'subadmin/subadmin_clients.html', {'client': client}) 
    else:
        messages.error(request, 'Pls Login')
        return redirect('subadmin_login')    
    
def subbase(request):
   
    return HttpResponse('no session')
       
    
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
import logging


logger = logging.getLogger(__name__)

@csrf_protect
def subadmin_client_registration(request):
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
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
                    return render(request, 'subadmin/subadmin_register.html', {'msg':'Email already registered'}) 
                
                except ind_clientDT.DoesNotExist:    
                    Group = None
                    if group_id:
                        try:
                            Group = GROUP.objects.get(id=group_id)
                        except GROUP.DoesNotExist:
                            return render(request, 'subadmin/subadmin_register.html', {'msg': 'Selected group does not exist', 'groups': groups, 'brokers': brokers})
                    
                    Broker = None
                    if broker_id:
                        try:
                            Broker = BROKERS.objects.get(broker_name=broker_id)
                        except BROKERS.DoesNotExist:
                            return render(request, 'subadmin/subadmin_register.html', {'msg': 'Selected broker does not exist', 'groups': groups, 'brokers': brokers})

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
                            sub_admin_id = subadmin_id
                        )
                    #   client.strategies.set(selected_strategies)
                        
                        return redirect('subadmin_clients')
                    except Exception as e:
                        logger.error(f"Email sending failed: {e}")
                        return render(request, 'subadmin/subadmin_register.html', {'msg': f'Error sending email: {e}', 'groups': groups, 'brokers': brokers, 'strategies': strategies}) 
                    
            except Exception as e:
                logger.error(f"Client registration failed: {e}")
                return render(request, 'subadmin/subadmin_register.html', {'msg': f'Error: {e}', 'groups': groups, 'brokers': brokers, 'strategies': strategies}) 
        
        return render(request, 'subadmin/subadmin_register.html', {'groups': groups, 'brokers': brokers, 'strategies': strategies})
    else:
        messages.error(request, 'Pls Login')
        return redirect('subadmin_login')     
    

# ====================== edit_client =========================
from django.shortcuts import render, get_object_or_404, redirect
from accounts.forms import ind_clientDTForm

@csrf_protect
def subadmin_edit_client(request, clint_id):
    client = ind_clientDT.objects.get(clint_id=clint_id)
    if request.method == 'POST':
        form = ind_clientDTForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('subadmin_clients')
    else:
        form = ind_clientDTForm(instance=client)
    return render(request, 'edit_client.html', {'form': form})    

def create_api(request):
    return render(request,'api_create_informations.html')


def sub_admin(request):
    return render(request,'sub_admin.html')


# def create_api(request):
#     return render(request,'api_create_informations.html')
  
  

def subadmin_client_status(request):
    subadmin_id = request.session.get('subadmin_id')
    if subadmin_id:
        client = ind_clientDT.objects.filter(sub_admin_id = subadmin_id)
        return render(request, 'subadmin/subadmin_client_status.html',{'client':client})
    else:
        messages.error(request, 'Pls Login')
        return redirect('subadmin_login')