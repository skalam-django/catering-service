from django.shortcuts import redirect
from django.views import View
import urllib
from django.contrib.admin.sites import AdminSite
from django.conf import settings


class Login(View):
	def get(self, request, *args, **kwargs):
		secret_key = settings.SECRET_KEY
		response = AdminSite().login(request, extra_context={
																'site_header':'Niraj Caterer administration',
																'site_title' : 'Niraj Caterer'
															})
		return response

	def post(self, request, *args, **kwargs):
		secret_key = settings.SECRET_KEY
		response = AdminSite().login(request, extra_context={
																'site_header':'Niraj Caterer administration',
																'site_title' : 'Niraj Caterer'
															})
		return response

