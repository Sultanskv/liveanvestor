import os
from datetime import datetime


def validate(data, expected_values):
    l = [x for x in expected_values if x not in data]
    return l


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    client_ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
    return client_ip

def Logs(filename, message, desc, id, status = 0):
    log_folder = 'media/logs/'+filename
    os.makedirs(log_folder, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d')
    timestamp2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log_file_path = os.path.join(log_folder, filename+'-'+timestamp+'.txt')

    if status == 0:
        text = f"\n\n\n-------------------- {timestamp2} --------------------\n\n\nRequest - {desc} - {id}\n\n{message}\n\n----------------------------------------"
    else:
        text = f"\n\n\n-------------------- {timestamp2} --------------------\n\n\nResponse - {desc} - {id}\n\n{message}\n\n----------------------------------------"

    with open(log_file_path, 'a') as log_file:
        log_file.write(text)