from django.contrib import admin
from django.utils.translation import gettext_lazy
from django.utils.translation import ugettext_lazy as _
from .models import SuperUser, AdminUser, EmployeeUser, VendorUser, CustomerUser
from django.conf import settings

admin.site._wrapped.site_title = gettext_lazy('Niraj Caterer')
admin.site._wrapped.site_header = gettext_lazy('Niraj Caterer administration')


class FirstAreaCodeListFilter(admin.SimpleListFilter):
    title = _('Country Code + Area Code')

    parameter_name = 'ac'

    def lookups(self, request, model_admin):
        lookups = []
        all_qs = model_admin.model.objects.all()
        self.digits = []
        for obj in all_qs:
            country_code = obj.phone_number.country_code
            if country_code and len(str(country_code))>0:
                country_code = f'+{country_code}'
            else:
                country_code = ''
            self.digits.append(f"{country_code}{str(obj.phone_number.national_number)[:2]}")
        self.digits = list(set(self.digits))    
        qs = model_admin.get_queryset(request)
        for digit in self.digits:
            count = qs.filter(phone_number__istartswith=digit).count()
            if count:
                lookups.append((digit, '{} ({})'.format(digit, count)))       
        return lookups

    def queryset(self, request, queryset):
        filter_val = self.value()
        if filter_val in self.digits:
            return queryset.filter(phone_number__istartswith=self.value())


class SuperUserAdmin(admin.ModelAdmin):
    exclude = ("password", "last_login", "groups", "user_permissions", "date_joined")
    list_display = ("username", "name", "phone_number", )
    list_filter = (FirstAreaCodeListFilter, )
    readonly_fields = ("username", "is_staff", "is_superuser", "user_type")
    search_fields = ("username__istartswith", "first_name__istartswith", "last_name__istartswith", "phone_number__icontains", )

    def name(self, obj):
        return f"{obj.first_name if obj.first_name else ''} {obj.last_name if obj.last_name else ''}" 
    
    def user_type(self, obj):
        return (list(filter(None, [(user_types[1] if obj.user_type == user_types[0] else None) for user_types in settings.USER_TYPES])) or ['Unknown'])[0]  

    def get_queryset(self, request):    
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(user_type='admin')
        return qs.none()  


class AdminUserAdmin(admin.ModelAdmin):
    exclude = ("password", "last_login", "groups", "user_permissions", "date_joined", )
    list_display = ("username", "name", "phone_number", )
    list_filter = (FirstAreaCodeListFilter, )
    readonly_fields = ("username", "is_staff", "user_type")
    search_fields = ("username__istartswith", "first_name__istartswith", "last_name__istartswith", "phone_number__icontains", )

    def name(self, obj):
        return f"{obj.first_name if obj.first_name else ''} {obj.last_name if obj.last_name else ''}" 
    
    def user_type(self, obj):
        return (list(filter(None, [(user_types[1] if obj.user_type == user_types[0] else None) for user_types in settings.USER_TYPES])) or ['Unknown'])[0]  
    
    def get_queryset(self, request):    
        qs = super().get_queryset(request)

        if request.user.is_superuser==False:
            self.readonly_fields = ("username", "is_staff", "user_type", "is_superuser",)
            if request.user.is_staff:
                self.exclude = ("user_password", "password", "last_login", "groups", "user_permissions", "date_joined", )
                return qs.filter(username=request.user.username)        

        if request.user.is_staff:
            return qs.filter(user_type='admin')
        return qs.none()    


class EmployeeUserAdmin(admin.ModelAdmin):
    exclude = ("user_password", "password", "email_password", "last_login", "groups", "user_permissions", "date_joined", "is_superuser", "is_staff",)
    list_display = ("username", "name", "phone_number", )
    list_filter = (FirstAreaCodeListFilter, )
    readonly_fields = ("username", "user_type")
    search_fields = ("username__istartswith", "first_name__istartswith", "last_name__istartswith", "phone_number__icontains", )

    def name(self, obj):
        return f"{obj.first_name if obj.first_name else ''} {obj.last_name if obj.last_name else ''}" 
    
    def user_type(self, obj):
        return (list(filter(None, [(user_types[1] if obj.user_type == user_types[0] else None) for user_types in settings.USER_TYPES])) or ['Unknown'])[0]  
    
    def get_queryset(self, request):    
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs.filter(user_type="employee")
        return qs.none()    


class VendorUserAdmin(admin.ModelAdmin):
    exclude = ("user_password", "password", "email_password", "last_login", "groups", "user_permissions", "date_joined", "is_superuser", "is_staff",)
    list_display = ("username", "name", "phone_number", )
    list_filter = (FirstAreaCodeListFilter, )
    readonly_fields = ("username", "user_type")
    search_fields = ("username__istartswith", "first_name__istartswith", "last_name__istartswith", "phone_number__icontains", )

    def name(self, obj):
        return f"{obj.first_name if obj.first_name else ''} {obj.last_name if obj.last_name else ''}" 
    
    def user_type(self, obj):
        return (list(filter(None, [(user_types[1] if obj.user_type == user_types[0] else None) for user_types in settings.USER_TYPES])) or ['Unknown'])[0]  
    
    def get_queryset(self, request):    
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs.filter(user_type="vendor")
        return qs.none()    


class CustomerUserAdmin(admin.ModelAdmin):
    exclude = ("user_password", "password", "email_password", "last_login", "groups", "user_permissions", "date_joined", "is_superuser", "is_staff",)
    list_display = ("username", "name", "phone_number", )
    list_filter = (FirstAreaCodeListFilter, )
    readonly_fields = ("username", "user_type")
    search_fields = ("username__istartswith", "first_name__istartswith", "last_name__istartswith", "phone_number__icontains", )

    def name(self, obj):
        return f"{obj.first_name if obj.first_name else ''} {obj.last_name if obj.last_name else ''}" 
    
    def user_type(self, obj):
        return (list(filter(None, [(user_types[1] if obj.user_type == user_types[0] else None) for user_types in settings.USER_TYPES])) or ['Unknown'])[0]  
    
    def get_queryset(self, request):    
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs.filter(user_type="customer")
        return qs.none() 

admin.site.register(SuperUser, SuperUserAdmin)   
admin.site.register(AdminUser, AdminUserAdmin)   
admin.site.register(EmployeeUser, EmployeeUserAdmin) 
admin.site.register(VendorUser, VendorUserAdmin) 
admin.site.register(CustomerUser, CustomerUserAdmin)    

