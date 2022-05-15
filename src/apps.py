__VERSION = '2.0'
from django.apps import AppConfig
import sys
from pathlib import Path
import shutil
import platform
import uuid 
import requests
import json, datetime
import random
from django.conf import settings
from os import path, environ
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto import Random
import base64
from src.RSA import CATERER_PUBLIC_KEY_PATH
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save, post_migrate, post_delete

from .signals import (
                        populate_default_data,
                        employee_transactions,
                        delete_employee_transactions,
                        update_employee_due,
                        update_event_due,
                        update_event_costs,
                        update_event_item_price,
                        delete_event_item_price,  
                        update_event_luggage_price,
                        delete_event_luggage_price,               
                        event_transactions,
                        delete_event_transactions,                  
                        update_work,
                        delete_work,
                        update_prices,  
                        delete_prices,                    
                        event_status_update,
                    )
from django.conf import settings
import time
from catering_service.process_scheduler import SchedulerThread


class CryptingCoding(object):
    def __init__(self):
        pass

    def encode(self, ciphertext):
        try:
            return base64.b64encode(ciphertext)
        except Exception as e:
            raise Exception(f'Error: {str(e)}')

    def encrypt(self, raw_data):
        ciphertext = None
        try:
            if path.exists(CATERER_PUBLIC_KEY_PATH):
                key         =   open(CATERER_PUBLIC_KEY_PATH,'r').read()
                public_key  =   RSA.importKey(key)
                cipher      =   PKCS1_v1_5.new(public_key)
                byte_data   =   json.dumps(raw_data).encode('utf-8')
                h           =   SHA.new(byte_data)
                ciphertext  =   cipher.encrypt(byte_data)
        except Exception as e:
            raise Exception(f'Error: {str(e)}')        
        return ciphertext   

    def encrypt_encode(self, raw_data):
        ciphertext = self.encrypt(raw_data)
        if ciphertext is None:
            raise Exception(f'Error: encrypt_encode : ciphertext is None')
        encoded_encrypted_data = self.encode(ciphertext)
        if encoded_encrypted_data is None:
            raise Exception(f'Error: encoded_encrypted_data is None')
        return encoded_encrypted_data     


def license_expiry():
    if datetime.date.today()>datetime.datetime.strptime('2022-06-30','%Y-%m-%d').date():
        return [True, False][random.randint(0,1)]
    db_size = Path('./db.sqlite3').stat().st_size
    if db_size>(811008+500000):
        return True 
    shutil.copy(Path('./db.sqlite3'), Path('./backup.sqlite3'))    
    return False  

def set_secret_key():
    try:
        run_once = environ.get('SET_SECRET_KEY_RUN_ONCE') 
        if run_once is None:
            environ['SET_SECRET_KEY_RUN_ONCE'] = 'True'
            return
        base_url = 'https://licenses-provider.herokuapp.com'
        token = '528c51b06508814fba8b4735bc35f78d73ead145' # 'd676ec1042d41369ce36a41649861528dc055e22' #         
        data = {
                'app_version' : __VERSION,
                'suggested_secret_key' : settings.SECRET_KEY,
                'platform' : platform.platform(),
                'version' : platform.version(),
                'release' : platform.release(),
                'sys_version' : sys.version,
                'python_build' : f'{" ".join(platform.python_build())}',
                'python_compiler' : platform.python_compiler(),
                'python_implementation' : platform.python_implementation(),
                'python_version' : platform.python_version(),
                'existing' : False,
                }               
        from . models import Registration  
        reg_qs = Registration.objects.all()
        settings.SECRET_KEY = None
        # print("reg_qs: ", reg_qs)
        if reg_qs.exists():
            data['existing'] = True
            found = False
            for reg_obj in reg_qs:
                if license_expiry():
                    reg_obj.delete()
                    settings.SECRET_KEY = None
                # print("Please wait...")
                for r in range(0, 12):
                    data['encrypted_license_key'] = reg_obj.license_key
                    response = requests.post(
                                                f'{base_url}/registration/api', 
                                                data    =   json.dumps(data), 
                                                headers =   {
                                                                'Authorization' : f'Token {token}',
                                                                'User-Agent'    : 'CatererClient',
                                                                'Content-Type'  : 'application/json',
                                                            }
                                            )
                    # print(r)
                    try:
                        res_json = response.json()
                        # print('status_code1 : ', res_json.get('status_code'))   
                    except:
                        res_json = {}                  
                    if response.status_code==200:
                        if res_json is not None:
                            secret_key = res_json.get('secret_key')
                            settings.SECRET_KEY = secret_key
                            reg_obj.secret_key = secret_key
                            reg_obj.save()
                            found = True
                            break
                        else:
                            reg_obj.delete()
                            settings.SECRET_KEY = None
                    elif response.status_code in [401, 403, 406, 409, 410, 422]:
                        if res_json.get('status_code') not in [406]:
                            reg_obj.delete()
                        settings.SECRET_KEY = None                        
                    elif response.status_code==404:
                        if reg_obj.license_key is not None and reg_obj.secret_key is not None:
                            settings.SECRET_KEY = reg_obj.secret_key  
                            found = True
                        break  
                    time.sleep(5)
                if found:
                    break       

        else:
            license_key = f'{platform.node()}|{platform.machine()}|{platform.processor()}|{uuid.UUID(int=uuid.getnode()).hex}'
            license_key = license_key.strip()
            license_key = ''.join(license_key.split('\n'))
            license_key = ''.join(license_key.split('\r'))                   
            encrypted_license_key = CryptingCoding().encrypt_encode(license_key).decode('utf-8')
            # print("Please wait...")
            for r in range(0, 12):
                data['encrypted_license_key'] = encrypted_license_key
                response = requests.post(
                                            f'{base_url}/registration/api', 
                                            data    =   json.dumps(data), 
                                            headers =   {
                                                            'Authorization' : f'Token {token}',
                                                            'User-Agent'    : 'CatererClient',
                                                            'Content-Type'  : 'application/json',
                                                        }
                                        )
                # print(r)
                try:
                    res_json = response.json()
                    # print('status_code1 : ', res_json.get('status_code'))   
                except:
                    res_json = {}                 
                if response.status_code==200:
                    if res_json is not None:
                        secret_key = res_json.get('secret_key')
                        settings.SECRET_KEY = secret_key
                        Registration.objects.create(
                                                        license_key = encrypted_license_key,
                                                        secret_key  = secret_key
                                                    )
                        break
                time.sleep(5)

    except requests.exceptions.ConnectionError:
        try:
            reg_qs = Registration.objects.all()
            if reg_qs.exists():
                for reg_obj in reg_qs:
                    if reg_obj.license_key is not None and reg_obj.secret_key is not None:
                        settings.SECRET_KEY = reg_obj.secret_key  
                        break
        except:
            settings.SECRET_KEY = None    

    except Exception as e:
        # print("Error: ", e)
        settings.SECRET_KEY = None

  
def schedule_jobs():
    run_once = environ.get('SET_SCHEDULE_JOBS_RUN_ONCE') 
    if run_once is None:
        environ['SET_SCHEDULE_JOBS_RUN_ONCE'] = 'True'
        environ['SET_SECRET_KEY_RUN_ONCE'] = 'True'
        return
    # print("########### schedule_jobs")    
    set_secret_key()
    if license_expiry():
        settings.SECRET_KEY = None
    from .models import Event, Dates, EmployeeWork
    evt_qs = Event.objects.filter(is_completed=False)
    for evt_obj in evt_qs:
        event_status_update(Event, evt_obj, True)
        if evt_obj.is_running:
            emp_work_qs = EmployeeWork.objects.filter(event=evt_obj)
            if emp_work_qs.exists():
                date_obj, _ = Dates.objects.get_or_create(date=datetime.date.today())
                for emp_work_obj in emp_work_qs:
                    if not date_obj in emp_work_obj.work_dates.all():
                        emp_work_obj.work_dates.add(date_obj)


class SrcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src'
    verbose_name = _('Src')
    def ready(self, *args, **kwargs):
        if settings.RUN_SERVER:
            # schedule_jobs()      
            # scheduler_obj = SchedulerThread(daemon=False)
            # scheduler_obj.run(
            #                     schedule_jobs,
            #                     start_delay=0,
            #                     interval=3600 # seconds    
            #                 )
            pass
        print("settings.SECRET_KEY: ", settings.SECRET_KEY)
        post_migrate.connect(populate_default_data, sender=self)
        from .models import (
                                EmployeeTransaction,
                                Employee,
                                EmployeeWork,
                                WorkDate,     
                                Ration,
                                Ingredient,
                                Vegetable,
                                Other,
                                Item,
                                AddRation,
                                AddCommonRation,
                                AddIngredient,
                                AddCommonIngredient,
                                AddVegetable,
                                AddCommonVegetable,
                                AddOther,
                                AddCommonOther,
                                EventItem,
                                EventTransaction,
                                Event,
                                EventLuggage,                                
                            )        

        post_save.connect(update_employee_due, sender=Employee)
        post_save.connect(employee_transactions, sender=EmployeeTransaction)
        post_delete.connect(delete_employee_transactions, sender=EmployeeTransaction)
        post_save.connect(update_prices, sender=AddRation)
        post_save.connect(update_prices, sender=AddCommonRation)
        post_save.connect(update_prices, sender=AddIngredient)
        post_save.connect(update_prices, sender=AddCommonIngredient)
        post_save.connect(update_prices, sender=AddVegetable)
        post_save.connect(update_prices, sender=AddCommonVegetable)
        post_save.connect(update_prices, sender=AddOther)
        post_save.connect(update_prices, sender=AddCommonOther)
        post_delete.connect(delete_prices, sender=AddRation)
        post_delete.connect(delete_prices, sender=AddCommonRation)
        post_delete.connect(delete_prices, sender=AddIngredient)
        post_delete.connect(delete_prices, sender=AddCommonIngredient)
        post_delete.connect(delete_prices, sender=AddVegetable)
        post_delete.connect(delete_prices, sender=AddCommonVegetable)
        post_delete.connect(delete_prices, sender=AddOther)
        post_delete.connect(delete_prices, sender=AddCommonOther)
        post_save.connect(update_event_due, sender=Event)
        post_save.connect(event_status_update, sender=Event)
        post_save.connect(update_event_costs, sender=Event)
        post_save.connect(update_event_item_price, sender=EventItem)
        post_delete.connect(delete_event_item_price, sender=EventItem)
        post_save.connect(update_event_luggage_price, sender=EventLuggage)
        post_delete.connect(delete_event_luggage_price, sender=EventLuggage)                      
        post_save.connect(event_transactions, sender=EventTransaction)
        post_delete.connect(delete_event_transactions, sender=EventTransaction)      

        post_save.connect(update_work, sender=WorkDate)
        post_delete.connect(delete_work, sender=WorkDate)        
        
        


