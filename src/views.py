from django.contrib.auth.mixins import LoginRequiredMixin
from catering_service.template import BaseTemplateView, get_template, register_layout, register_sidebar
from django.views.generic.list import ListView
from src.models import Menu
from src.forms import MenuForm, ShareForm
from django.template.response import TemplateResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.contrib import messages
from . utils import send_email

class MenuView(LoginRequiredMixin, ListView, BaseTemplateView):
	login_url = 'auth_app:login'
	LOGIN_REDIRECT_URL = '/login/'
	template_name = get_template(__module__, 'menu.html')
	extra_context = {
		"site_title"    : "Menu",
		"logout_url"    : "nc_auth:logout",
		"next_url"      : "/",
		"qualname" 		:	__qualname__,
	}  

	success_url 	=	extra_context['next_url']
	model 			= 	Menu
	
	#paginate_by 	= 	5

	register_layout(__qualname__, extra_context['site_title'], True)
	register_sidebar(__qualname__, extra_context['site_title'], get_url=extra_context['next_url'], post_url=extra_context['next_url'], icon='widgets')

	def get_context_data(self, *args, **kwargs):
		secret_key = settings.SECRET_KEY
		idx_list = list(self.get_queryset().values_list('idx', flat=True).order_by('name').distinct())
		name_list = list(self.get_queryset().values_list('name', flat=True).order_by('name').distinct())
		self.object_list = zip(idx_list, name_list)
		idx = self.request.GET.get('idx')
		self.extra_context['menu_pdfs'] = None
		if idx is not None:
			menu_pdf = self.get_queryset().filter(idx=int(idx)).values('id', 'menu_pdf')
			chunks = lambda lst, size: [lst[i : i+size] for i in range(0, len(lst), size)]
			pdf_chunks = chunks(menu_pdf, 3)
			# print("pdf_chunks: ", pdf_chunks)
			self.extra_context['menu_pdfs'] = TemplateResponse(
																self.request,
																get_template(self.__module__, 'menu_pdfs.html'),
																{'pdf_chunks' : pdf_chunks}
															).rendered_content
		self.extra_context['fab_dialog_template'] = TemplateResponse(
																	self.request, 
																	get_template(self.__module__, 'fab_dialog_form.html'), 
																	{'fab_dialog_form' : MenuForm()}
																).rendered_content
		self.extra_context['share_dialog_template'] = TemplateResponse(
																	self.request, 
																	get_template(self.__module__, 'share_dialog_form.html'), 
																	{'share_dialog_form' : ShareForm()}
																).rendered_content
		url = '/'
		if idx:
			url = f'{url}?idx={idx}'			
		self.extra_context['fab_dialog_action'] =  url
		self.extra_context['share_dialog_action'] = '/share-menu'



		return super().get_context_data(*args, **kwargs)

	def post(self, request, *args, **kwargs):	
		secret_key = settings.SECRET_KEY
		form = MenuForm(request.POST, request.FILES)
		name = request.POST.get('name')
		menu_pdf = request.FILES.get('menu_pdf')
		if form.is_valid():
			instance = form.save()
			if Menu.objects.filter(name=name).count()==1:
				messages.success(request, f"Menu: {name} created successfully!")
				messages.success(request, f"{menu_pdf} added.")
			else:
				messages.success(request, f"{menu_pdf} added to Menu: {name}")	
			return redirect(f'/?idx={instance.idx}')
		messages.error(request, f"Failed to add {menu_pdf} to Menu : {name}")
		url = '/'
		idx = request.GET.get('idx')
		if idx:
			url = f'{url}?idx={idx}'
		return redirect(url)


class ShareMenu(LoginRequiredMixin, ListView, BaseTemplateView):
	login_url = 'auth_app:login'
	LOGIN_REDIRECT_URL = '/login/'
	template_name = get_template(__module__, 'menu.html')
	extra_context = {
		"site_title"    : "Menu",
		"logout_url"    : "nc_auth:logout",
		"next_url"      : "/share-menu",
		"qualname" 		:	__qualname__,
	}  

	success_url 	=	extra_context['next_url']

	def post(self, request, *args, **kwargs):
		ids = request.POST.get('ids', '')
		ids = ids.split(',')
		try:
			if ids!="":
				ids = [int(i) for i in ids]
				menu_pdfs = Menu.objects.filter(id__in=ids).values_list('menu_pdf', 'name')
				email_password = request.user.email_password
				if len(menu_pdfs)>0 and email_password is not None and email_password!='':
					attachments = [m[0] for m in menu_pdfs]
					menu_name = menu_pdfs[0][1]
					if len(attachments)>0:
						ok = send_email(
									request.user.email, 
									request.user.email_password, 
									request.POST.get('email'), 
									attachments, 
									subject="Menu PDF | Niraj Caterer", 
									body=f"Please find the attached files for <strong>{menu_name}</strong> menu.", 
									sender_name=f"{request.user.first_name} {request.user.last_name}", 
									receiver_name=request.POST.get('name')
								)
						if ok:
							messages.success(request, 'Sucess. Mail has been sent successfully.')
						else:
							messages.error(request, 'Failed to sent mail.')
					else:
						messages.error(request, 'Failed. No attachments.')
				else:
					if len(menu_pdfs)==0:
						messages.error(request, 'Failed. No attachments.')
					elif email_password is None or email_password!='':
						messages.error(request, 'Failed. Email password has not been set.')
			else:
				messages.error(request, 'Failed. No attachments.')			
		except Exception as e:
			print("ShareMenu Error: ", e)
			messages.error(request, 'Failed. Something went wrong.')	
		url = '/'
		idx = request.GET.get('idx')
		if idx:
			url = f'{url}?idx={idx}'
		return redirect(url)


class AllViews:

	register_layout('MyWalletView', 'My Wallet', True)
	register_sidebar('MyWalletView', 'My Wallet', get_url='/accounts/src/mywallet/', post_url='/accounts/src/mywallet/', icon='widgets', open_type="_blank")

	
	register_layout('AdminView', 'Admin', True)
	register_sidebar('AdminView', 'Admin', get_url='/accounts/auth_app/adminuser/', post_url='/accounts/auth_app/adminuser/', icon='widgets', open_type="_blank")

	register_layout('EmployeeView', 'Employee', True)
	register_sidebar('EmployeeView', 'Employee', get_url='/accounts/src/employee/', post_url='/accounts/src/employee/', icon='widgets', open_type="_blank")

	register_layout('VendorView', 'Vendor', True)
	register_sidebar('VendorView', 'Vendor', get_url='/accounts/src/vendor/', post_url='/accounts/src/vendor/', icon='widgets', open_type="_blank")

	register_layout('LuggageView', 'Luggage', True)
	register_sidebar('LuggageView', 'Luggage', get_url='/accounts/src/luggage/', post_url='/accounts/src/luggage/', icon='widgets', open_type="_blank")
		
	register_layout('ItemView', 'Item', True)
	register_sidebar('ItemView', 'Item', get_url='/accounts/src/item/', post_url='/accounts/src/item/', icon='widgets', open_type="_blank")

	register_layout('EventView', 'Event', True)
	register_sidebar('EventView', 'Event', get_url='/accounts/src/event/', post_url='/accounts/src/event/', icon='widgets', open_type="_blank")

	register_layout('EmployeeWorkView', 'Employee Work', True)
	register_sidebar('EmployeeWorkView', 'Employee Work', get_url='/accounts/src/employeework/', post_url='/accounts/src/employeework/', icon='widgets', open_type="_blank")

	# register_layout('TransactionsView', 'Transactions', True)
	# register_sidebar('TransactionsView', 'Transactions', get_url='/accounts/src/transactions/', post_url='/accounts/src/transactions/', icon='widgets', open_type="_blank")


	# register_layout('RationView', 'Ration', True)
	# register_sidebar('RationView', 'Ration', get_url='/accounts/src/ration/', post_url='/accounts/src/ration/', icon='widgets', open_type="_blank")

	# register_layout('IngredientView', 'Ingredient', True)
	# register_sidebar('IngredientView', 'Ingredient', get_url='/accounts/src/ingredient/', post_url='/accounts/src/ingredient/', icon='widgets', open_type="_blank")

	# register_layout('VegetableView', 'Vegetable', True)
	# register_sidebar('VegetableView', 'Vegetable', get_url='/accounts/src/vegetable/', post_url='/accounts/src/vegetable/', icon='widgets', open_type="_blank")

	# register_layout('OtherView', 'Other', True)
	# register_sidebar('OtherView', 'Other', get_url='/accounts/src/other/', post_url='/accounts/src/other/', icon='widgets', open_type="_blank")





def items(request, *args, **kwargs):
	from .models import Event
	event_qs = Event.objects.filter(id=1)
	qs = []
	rations = []
	if event_qs.exists():
		event_obj = event_qs.first()
		item_qs = event_obj.item.all()
		from . models import AddRation, AddCommonRation, CommonRation
		from django.db.models import Sum, F
		from django.conf import settings
		from itertools import chain
		from . utils import render_to_pdf
		name = 'Ration'
		items = chain(
			AddRation.objects.values('unit')\
			.annotate(item_name=F('ration__name'), quantity=Sum('quantity'))\
			.distinct().filter(item__in=item_qs), 			
			AddCommonRation.objects.values('unit')\
			.annotate(item_name=F('common_ration__name'), quantity=Sum('quantity'))\
			.distinct().filter(item__in=item_qs)
		)
	items = list(items)					
	x = [item.update({'sl_no':idx+1}) for idx, item in enumerate(items)]
	n = len(items)
	chunk_items = [items[i:i + n] for i in range(0, len(items), n)] 		
	return render_to_pdf('src/items.html', {
																'request' 	: 	request, 
																'event' 	: 	event_obj, 
																'name' 		: 	name,
																'chunk_items': 	chunk_items, 
																'units' 	: 	settings.UNITS, 
																'filename'	: 	f'{name}.{event_obj.ref_no}'
															})
