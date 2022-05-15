from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
import traceback
from catering_service.utils import loggerf, printf
import json
from catering_service.template import BaseTemplateView, get_template	
from catering_service.response_handler import CustomViewResponse
from django.http import HttpResponse


class CustomMiddleware(MiddlewareMixin):
	def __init__(self, get_response, *args, **kwargs):
		return super(CustomMiddleware, self).__init__(get_response, *args, **kwargs)
	def process_request(self, request, *args, **kwargs):
		request.META['static_version'] = settings.STATIC_VERSION
		request.META['isMobile'] = settings.IS_MOBILE
		try:
			secret_key = settings.SECRET_KEY
		except ImproperlyConfigured as e:
			return HttpResponse('<pre style="word-wrap: break-word; white-space: pre-wrap;">A server error occurred.  Please contact the administrator.</pre>')

	def process_response(self, request, response):
		return response

	def process_view(self, request, view_func, view_args, view_kwargs):
		self.func_name 		=	view_func.__name__
		self.func_module 	= 	view_func.__module__

	def process_exception(self, request, exception):
		loggerf(traceback.format_exc())
		error = f'[ERROR] {self.func_module}.{self.func_name}(): {exception}'
		loggerf(error)
		return CustomViewResponse(BaseTemplateView, request, template_name=get_template('catering_service', 'error_page.html')).response()





