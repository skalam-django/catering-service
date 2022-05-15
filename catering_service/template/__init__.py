from django.template.loader import select_template
from django.views.generic import TemplateView
from django.conf import settings
import json 
from catering_service.utils import loggerf, printf
import traceback



layout_dict = {"ErrorView" 	: 	{'title' : "Error", 'footer' : False}}
sidebar_dict = {}


def get_template(module=None, template_name=None):
	try:
		return select_template([f"{module.split('.')[0]}/{template_name}", 'catering_service/page_does_not_exist.html']).template.name
	except Exception as e:
		print(f"get_template() TemplateError: {e}")
		return select_template(['catering_service/page_does_not_exist.html']).template.name

def reorder(arr, default_idx):
	old_arr = arr.copy()
	arr[0]  = arr[default_idx]
	old_arr.pop(default_idx)
	for idx, e in enumerate(old_arr):
		arr[idx+1] =  old_arr[idx]
	return arr	


def register_layout(view_name, title, footer=True):
	global layout_dict
	layout_dict[view_name] = {"title" : title, "footer" : footer}

def register_sidebar(id, caption, get_url='/', post_url=None, icon="", open_type="_self"):
	global sidebar_dict
	if id not in sidebar_dict:
		sidebar_dict[id] = {}

	sidebar_dict[id].update({
								"caption" 	: 	caption, 
								"urls" 		: 	{
													"get": get_url, 
													"post": post_url,
													"open_type" : 	open_type or "_self",
												},
								"icon" 		:	icon,
							})


class SideBar(object):
	def get(self):
		try:		
			global sidebar_dict
			return sidebar_dict
		except:
			return []


class BaseTemplateView(TemplateView):
	template_name 	= 	get_template('catering_service')
	default_bar_idx = 	None	
	extra_context 	= 	{
		"site_title" : "Login",
		"logout_url"  : "auth_app:logout",
		"next_url" : "/",
		"dialog_template" : "",
	}
	cookies_dict = {}

	def __init__(self, *args, **kwargs):
		self.extra_context["this_app"] = self.__module__.split('.')[0]
		self.extra_context["base_template"] = get_template("catering_service", "base.html")
		self.extra_context["layout_1"] = get_template("catering_service", "layout_1.html")
		self.extra_context["layout_2"] = get_template("catering_service", "layout_2.html")
		self.extra_context["edit_profile"] = {
												"caption" : "Edit Profile", 
												"icon" 	:	"account_circle",
												"urls" : {
															"get":"",
															"post":""
														}
												}
		self.extra_context["logout"] = {
												"caption" : "Logout", 
												"icon" 	:	"exit_to_app",
												"urls" : {
															"get":"/home/",
															"post":"/auth/logout/"
														}
												}										
		# self.extra_context["footer"] = False


	def get_context_data(self, *args, **kwargs):
		try:
			printf("BaseTemplateView().get_context_data() template_name: ", self.template_name)
			user_obj = self.request.user		
			try:
				path = self.__class__.__name__
				if path	is None:
					path = "ErrorView"
			except:
				path = "ErrorView"
			if user_obj.is_authenticated == True:
				sidebar_dict = SideBar().get()
				self.extra_context['show_sidebar'] = len(sidebar_dict)>0
				self.extra_context['sidebar_dict'] = sidebar_dict
				self.extra_context['edit_profile']['urls']['get'] = f"/accounts/auth_app/{'superuser' if self.request.user.is_superuser else 'adminuser'}/{self.request.user.id}/change/"
			global layout_dict			
			self.extra_context['layout'] = layout_dict.get(path)
			context = super(BaseTemplateView, self).get_context_data(*args, **kwargs)    
			context.update(self.extra_context)
			# print("context: ",context, context.get('site_title'))
			return context
		except Exception as e:
			print("BaseTemplateView().get_context_data()", e)
			raise e	
	def dispatch(self, request, *args, **kwargs):
		printf("BaseTemplateView().dispatch()")
		try:
			response = super(BaseTemplateView, self).dispatch(request, *args, **kwargs)
			for key, value in self.cookies_dict.items():
				response.set_cookie(key, value)
			return response
		except Exception as e:
			print(traceback.format_exc())
			print("BaseTemplateView().dispatch()", e)
			raise e	


class ErrorView(BaseTemplateView):
	template_name = get_template('catering_service', 'error_page.html')
	extra_context 	= 	{
		"site_title" : "Error",
		"get_url" : "/",
		"back_btn" : False,
	}	
	register_layout(__qualname__, extra_context['site_title'], False)

	def get_context_data(self, *args, **kwargs):
		class_name = kwargs.get('class_name')
		if class_name is not None:
			__class__.__name__ = class_name
		return super().get_context_data(*args, **kwargs)
