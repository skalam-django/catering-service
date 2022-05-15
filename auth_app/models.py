from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import UserManager
from catering_service.utils import validate_phonenumber
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission

def all_permissions_except_delete(user_obj):
    permissions = Permission.objects.all()
    for permission_obj in permissions:
        if 'Can delete' in permission_obj.name:
            continue 
        user_obj.user_permissions.add(permission_obj)
    user_obj.save()    


class AuthUserManager(UserManager):
    def create_superuser(self, *args, **kwargs):
        username = kwargs.get('username')
        phone_number = validate_phonenumber(kwargs.get('phone_number'))
        user_type = kwargs.get('user_type', settings.USER_TYPES[0][0]) or settings.USER_TYPES[0][0]
        kwargs['user_type'] = user_type
        if username is None: 
            kwargs['username'] = f'{phone_number.national_number}@{user_type}'     
        return super().create_superuser(*args, **kwargs)

    def create(self, *args, **kwargs):
        username = kwargs.get('username')
        phone_number = validate_phonenumber(kwargs.get('phone_number'))
        user_type = kwargs.get('user_type', settings.USER_TYPES[0][0]) or settings.USER_TYPES[0][0]
        kwargs['user_type'] = user_type
        if username is None: 
            username = f'{phone_number.national_number}@{user_type}'
        user_obj = super().create(*args, **kwargs)
        if user_obj.is_superuser==False and user_obj.user_type=='admin':
            all_permissions_except_delete(user_obj)
        return user_obj    




class AuthUser(AbstractUser):
    user_password   =   models.CharField(max_length=255, null=True, blank=True)
    phone_number 	=	PhoneNumberField(region='IN')
    email 			= 	models.EmailField(null=True, blank=True)
    email_password  =   models.CharField(max_length=500, null=True, blank=True)
    user_type       =   models.CharField(choices=settings.USER_TYPES, default=settings.USER_TYPES[0][0], max_length=255)
    address         =   models.TextField(null=True, blank=True)
    created_at		=	models.DateTimeField(auto_now_add=True)
    updated_at		=	models.DateTimeField(auto_now=True)	
    objects         =   AuthUserManager()
    class Meta:
        managed = True
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        self.username = f'{self.phone_number.national_number}@{self.user_type}'
        if self.user_type=='admin':
            self.is_staff = True
        else:
             self.is_staff = False
             self.is_superuser = False  
        if self.user_password is not None and self.user_password !='':
            self.password = make_password(self.user_password)    
        super().save(*args, **kwargs)


class SuperUser(AuthUser):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('is_superuser').default = True
        self._meta.get_field('is_staff').default = True
        self._meta.get_field('is_active').default = True
        self._meta.get_field('user_type').default = settings.USER_TYPES[0][0]
        super().__init__(*args, **kwargs)  
    class Meta:
        proxy = True    


class AdminUser(AuthUser):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('is_superuser').default = False
        self._meta.get_field('is_staff').default = True
        self._meta.get_field('is_active').default = True
        self._meta.get_field('user_type').default = settings.USER_TYPES[0][0]
        super().__init__(*args, **kwargs)  
    class Meta:
        proxy = True    

class EmployeeUser(AuthUser):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('is_superuser').default = False
        self._meta.get_field('is_staff').default = False
        self._meta.get_field('is_active').default = True
        self._meta.get_field('user_type').default = settings.USER_TYPES[1][0]
        super().__init__(*args, **kwargs)  

    class Meta:
        proxy = True 


class VendorUser(AuthUser):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('is_superuser').default = False
        self._meta.get_field('is_staff').default = False
        self._meta.get_field('is_active').default = True
        self._meta.get_field('user_type').default = settings.USER_TYPES[2][0]
        super().__init__(*args, **kwargs)  

    class Meta:
        proxy = True 


class CustomerUser(AuthUser):
    def __init__(self, *args, **kwargs):
        self._meta.get_field('is_superuser').default = False
        self._meta.get_field('is_staff').default = False
        self._meta.get_field('is_active').default = True
        self._meta.get_field('user_type').default = settings.USER_TYPES[3][0]
        super().__init__(*args, **kwargs)      
    class Meta:
        proxy = True         
