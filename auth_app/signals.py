from django.conf import settings
from django.forms.models import model_to_dict
import datetime
import traceback

def set_permissions(sender, instance, created, **kwargs):
	if created:
		if instance.is_superuser==False and instance.user_type=='admin':
			from auth_app.models import all_permissions_except_delete
			all_permissions_except_delete(instance)