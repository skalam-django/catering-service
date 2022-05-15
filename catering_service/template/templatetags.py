import os
import datetime
from django import template
from django.contrib.staticfiles.finders import find
from django.templatetags.static import static
from urllib.parse import unquote


register = template.Library()

@register.simple_tag
def nc_static(app_name, filename):
	static_type = os.path.splitext(filename)[1][1:].strip().lower()
	static_type = ('images' if static_type in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'] else 'media') if static_type not in ['js', 'css'] else static_type
	static_type += '/'
	if app_name in ['', 'node_modules']:
		static_type = ''
	return unquote(static(f"{app_name}/{static_type}{filename}"))

@register.simple_tag
def nc_assets(app_name, filename):
	static_type = os.path.splitext(filename)[1][1:].strip().lower()
	static_type = ('images' if static_type in ['png', 'jpg', 'jpeg', 'tiff', 'bmp', 'gif'] else 'media') if static_type not in ['js', 'css'] else static_type
	static_type += '/'
	if app_name in ['', 'node_modules']:
		static_type = ''
	return unquote(f"/assets/{app_name}/{static_type}{filename}")



@register.simple_tag	
def date_formater(date, dt_format='%Y-%m-%d'):
	return str(datetime.datetime.strftime(date, dt_format))


@register.filter	
def get_item(dict_obj, key):
	try:
		return dict_obj.get(key)
	except Exception as e:
		print(e)
		return dict_obj
			

