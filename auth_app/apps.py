from django.apps import AppConfig
from auth_app.signals import set_permissions
from django.db.models.signals import post_save

class AuthAppConfig(AppConfig):
	name = 'auth_app'
	def ready(self, *args, **kwargs):
		from auth_app.models import AdminUser
		post_save.connect(set_permissions, sender=AdminUser)