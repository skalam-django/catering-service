from django.contrib import admin
from django.utils.translation import gettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db.models import Sum, F
from django.conf import settings
from itertools import chain
from .models import (
						MyWallet,
						EmployeeCategory,
						Employee, 
						EmployeeTransaction,
						VendorCategory,
						Vendor, 
						VendorTransaction,						
						Unit,
						RationCategory,
						Ration,
						CommonRation,
						EstimatedRation,
						IngredientCategory,
						Ingredient,
						CommonIngredient,
						EstimatedIngredient,
						VegetableCategory,
						Vegetable,
						CommonVegetable,
						EstimatedVegetable,
						OtherCategory,
						Other,
						CommonOther,
						EstimatedOther,
						ItemCategory,
						Item,
						AddRation,
						AddCommonRation,
						AddIngredient,
						AddCommonIngredient,
						AddVegetable,
						AddCommonVegetable,
						AddOther,
						AddCommonOther,
						Event, 
						EventRation,
						EventIngredient,
						EventVegetable,
						EventOther,						
						EventTransaction,
						EventItem,
						LuggageCategory,
						Luggage,
						EventLuggage,
						EmployeeWork, 
						Dates,
						WorkDate,						
					)

import datetime
from . utils import render_to_pdf


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


def custom_titled_filter(title):
	class Wrapper(admin.FieldListFilter):
		def __new__(cls, *args, **kwargs):
			instance = admin.FieldListFilter.create(*args, **kwargs)
			instance.title = title
			return instance
	return Wrapper



class MyWalletAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")
	list_display = ("show_balance", "show_profit_loss")

	def show_balance(self, obj):
		return str(obj)

	def show_profit_loss(self, obj):
		if obj.balance>0:
			status = "PROFIT" 
		elif obj.balance<0:
			status = "LOSS" 
		else:
			status = "NEUTRAL"
		return status 	

	show_balance.short_description = "Balance"
	show_profit_loss.short_description = "Profit / Loss"



class UnitAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	search_fields = ("name__istartswith", )


class RationCategoryAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	search_fields = ("name__istartswith", )


class RationAdmin(admin.ModelAdmin):
	list_display = ("name", "selling_price", "show_common")
	exclude = ("is_common", "created_at", "updated_at")	
	search_fields = ("name__istartswith", )
	def show_common(self, obj):
		return 'common' if obj.is_common else ''
	show_common.short_description = "Common"

	def get_queryset(self, request):    
		qs = super().get_queryset(request)
		return qs.filter(is_common=False)

class CommonRationAdmin(admin.ModelAdmin):
	exclude = ("is_common", "created_at", "updated_at")	
	search_fields = ("name__istartswith", )

	def get_queryset(self, request):    
		qs = super().get_queryset(request)
		return qs.filter(is_common=True)


class IngredientCategoryAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	search_fields = ("name__istartswith", )

class IngredientAdmin(admin.ModelAdmin):
	exclude = ("is_common", "created_at", "updated_at")	
	search_fields = ("name__istartswith", )
	def show_common(self, obj):
		return 'common' if obj.is_common else ''
	def get_queryset(self, request):    
		qs = super().get_queryset(request)
		return qs.filter(is_common=False)

class CommonIngredientAdmin(admin.ModelAdmin):
	exclude = ("is_common", "created_at", "updated_at")	
	search_fields = ("name__istartswith", )

	def get_queryset(self, request):    
		qs = super().get_queryset(request)
		return qs.filter(is_common=True)


class VegetableCategoryAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	search_fields = ("name__istartswith", )

class VegetableAdmin(admin.ModelAdmin):
	exclude = ("is_common", "created_at", "updated_at")	
	search_fields = ("name__istartswith",)
	def show_common(self, obj):
		return 'common' if obj.is_common else ''
	def get_queryset(self, request):    
		qs = super().get_queryset(request)
		return qs.filter(is_common=False)
		
class CommonVegetableAdmin(admin.ModelAdmin):
	exclude = ("is_common", "created_at", "updated_at")	
	search_fields = ("name__istartswith", )

	def get_queryset(self, request):    
		qs = super().get_queryset(request)
		return qs.filter(is_common=True)


class OtherCategoryAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	search_fields = ("name__istartswith", )

class OtherAdmin(admin.ModelAdmin):
	exclude = ("is_common", "created_at", "updated_at")	
	search_fields = ("name__istartswith",)
	def show_common(self, obj):
		return 'common' if obj.is_common else ''
	def get_queryset(self, request):    
		qs = super().get_queryset(request)
		return qs.filter(is_common=False)
		
class CommonOtherAdmin(admin.ModelAdmin):
	exclude = ("is_common", "created_at", "updated_at")	
	search_fields = ("name__istartswith", )

	def get_queryset(self, request):    
		qs = super().get_queryset(request)
		return qs.filter(is_common=True)



class AddRationInline(admin.TabularInline):
	model = AddRation
	extra = 0
	autocomplete_fields = ['ration', 'unit']
	list_per_page = 5

class AddCommonRationInline(admin.TabularInline):
	model = AddCommonRation
	extra = 0
	autocomplete_fields = ['common_ration', 'unit']
	list_per_page = 5

class AddIngredientInline(admin.TabularInline):
	model = AddIngredient
	extra = 0
	autocomplete_fields = ['ingredient', 'unit']
	list_per_page = 5

class AddCommonIngredientInline(admin.TabularInline):
	model = AddCommonIngredient
	extra = 0
	autocomplete_fields = ['common_ingredient', 'unit']
	list_per_page = 5

class AddVegetableInline(admin.TabularInline):
	model = AddVegetable
	extra = 0
	autocomplete_fields = ['vegetable', 'unit']
	list_per_page = 5

class AddCommonVegetableInline(admin.TabularInline):
	model = AddCommonVegetable
	extra = 0
	autocomplete_fields = ['common_vegetable', 'unit']
	list_per_page = 5

class AddOtherInline(admin.TabularInline):
	model = AddOther
	extra = 0
	autocomplete_fields = ['other', 'unit']
	list_per_page = 5

class AddCommonOtherInline(admin.TabularInline):
	model = AddCommonOther
	extra = 0	
	autocomplete_fields = ['common_other', 'unit']
	list_per_page = 5


class ItemCategoryAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	search_fields = ("name__istartswith", )


class ItemAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	readonly_fields = ('purchase_price', 'suggested_selling_price',)
	list_filter = (('item_category__name', custom_titled_filter('Catergoy Name')),)
	search_fields = (
						"name__istartswith", 
						"rations__name__istartswith", 
						"ingredients__name__istartswith", 
						"vegetables__name__istartswith",
						"others__name__istartswith",
					)
	inlines = (
				AddRationInline, 
				AddCommonRationInline, 
				AddIngredientInline,
				AddCommonIngredientInline,
				AddVegetableInline,
				AddCommonVegetableInline,
				AddOtherInline,
				AddCommonOtherInline,
	)



class EventStatusListFilter(admin.SimpleListFilter):
	title = _('Event Status')

	parameter_name = 'es'

	def lookups(self, request, model_admin):
		self.status = ['Upcoming', 'Running', 'Completed']      
		lookups = []	
		qs = model_admin.get_queryset(request)
		for status in self.status:
			count = None
			if status=='Upcoming':
				count = qs.filter(is_upcoming=True).count()
			elif status=='Running':
				count = qs.filter(is_running=True).count()
			elif status=='Completed':
				count = qs.filter(is_completed=True).count()
			if count:
				lookups.append((status, '{} ({})'.format(status, count)))       
		return lookups

	def queryset(self, request, queryset):
		filter_val = self.value()
		if filter_val in self.status:
			if filter_val=='Upcoming':
				return queryset.filter(is_upcoming=True)
			elif filter_val=='Running':
				return queryset.filter(is_running=True)
			elif filter_val=='Completed':
				return queryset.filter(is_completed=True)
		return queryset				


class EventItemInline(admin.TabularInline):
	model = EventItem
	extra = 0
	readonly_fields = ("selling_price", "total_price", "unit",)

class EventLuggageAdmin(admin.TabularInline):
	model = EventLuggage
	extra = 0
	readonly_fields = ("unit", "per_day_charge", "total_charge", "total_lost_charge")

class EventTransactionInline(admin.TabularInline):
	model = EventTransaction
	extra = 0


class EventAdmin(admin.ModelAdmin):
	change_form_template = 'admin/change_form1.html'
	list_display = ("ref_no", "name", "show_client_name", "show_phone_number", "show_status",)
	exclude = ("is_upcoming", "is_running", "is_completed", )
	readonly_fields = ("ref_no", "total_amount_paid", "total_amount_due", "total_item_price", "total_employee_charge", "total_luggage_charge", "total_event_cost", "total_event_profit",)
	list_filter = (EventStatusListFilter, )
	search_fields = ("ref_no", "name", "client__first_name__istartswith", "client__last_name__istartswith", "client__phone_number__icontains", "client__user_type__istartswith",)
	inlines = (EventItemInline, EventLuggageAdmin, EventTransactionInline,)	
	
	def show_client_name(self, obj):
		return f"{obj.client.first_name if obj.client.first_name else ''} {obj.client.last_name if obj.client.last_name else ''}"
	
	def show_phone_number(self, obj):
		return f"{obj.client.phone_number}"

	def show_status(self, obj):
		if obj.is_upcoming:
			return "Upcoming"
		elif obj.is_running:
			return "Running"	
		elif obj.is_completed:
			return "Completed"	

	show_client_name.short_description = "Client Name"
	show_phone_number.short_description = "Phone number"
	show_status.short_description = "Event Status"


	def response_change(self, request, obj):
		if "_view-estimated-rations" in request.POST:
			try:
				add_rations = chain(
					AddRation.objects.values('unit__name')\
						.annotate(ration_name=F('ration__name'), quantity=Sum('quantity')*obj.eventitem_set.filter(item=F('item')).first().quantity)\
						.distinct().filter(item__in=obj.item.all()), 			
					AddCommonRation.objects.values('unit__name')\
						.annotate(ration_name=F('common_ration__name'), quantity=Sum('quantity')*obj.eventitem_set.filter(item=F('item')).first().quantity)\
						.distinct().filter(item__in=obj.item.all())
				)
			except:
				add_rations = []	

			for add_ration in add_rations:
				ration_obj = Ration.objects.get(name=add_ration.get('ration_name'))
				unit_obj = Unit.objects.get(name=add_ration.get('unit__name'))
				estm_ration_qs = EstimatedRation.objects.filter(
																	ration=ration_obj, 
																	# unit=unit_obj
																)
				if estm_ration_qs.exists():
					estm_ration_obj = estm_ration_qs.first()
				else:
					estm_ration_obj = EstimatedRation.objects.create(
											event=obj,
											ration=ration_obj, 
											unit=unit_obj
										)
				estm_ration_obj.suggested_quantity = float(add_ration.get('quantity'))
				estm_ration_obj.quantity = estm_ration_obj.quantity or estm_ration_obj.suggested_quantity
				estm_ration_obj.save()

			return HttpResponseRedirect(f"/accounts/src/eventration/{obj.id}/change/")

		elif "_view-estimated-ingredients" in request.POST:	
			try:		
				add_ingredients = chain(
					AddIngredient.objects.values('unit__name')\
						.annotate(ingredient_name=F('ingredient__name'), quantity=Sum('quantity')*obj.eventitem_set.filter(item=F('item')).first().quantity)\
						.distinct().filter(item__in=obj.item.all()),			
					AddCommonIngredient.objects.values('unit__name')\
						.annotate(ingredient_name=F('common_ingredient__name'), quantity=Sum('quantity')*obj.eventitem_set.filter(item=F('item')).first().quantity)\
						.distinct().filter(item__in=obj.item.all())	
				)		
			except:
				add_ingredients = []

			for add_ingredient in add_ingredients:
				ingredient_obj = Ingredient.objects.get(name=add_ingredient.get('ingredient_name'))
				unit_obj = Unit.objects.get(name=add_ingredient.get('unit__name'))
				estm_ingredient_qs = EstimatedIngredient.objects.filter(
																	ingredient=ingredient_obj, 
																	# unit=unit_obj
																)
				if estm_ingredient_qs.exists():
					estm_ingredient_obj = estm_ingredient_qs.first()
				else:
					estm_ingredient_obj = EstimatedIngredient.objects.create(
											event=obj,
											ingredient=ingredient_obj, 
											unit=unit_obj
										)
				estm_ingredient_obj.suggested_quantity = float(add_ingredient.get('quantity'))
				estm_ingredient_obj.quantity = estm_ingredient_obj.quantity or estm_ingredient_obj.suggested_quantity
				estm_ingredient_obj.save()

			return HttpResponseRedirect(f"/accounts/src/eventingredient/{obj.id}/change/")

		elif "_view-estimated-vegetables" in request.POST:			
			try:
				add_vegetables = chain(
					AddVegetable.objects.values('unit__name')\
						.annotate(vegetable_name=F('vegetable__name'), quantity=Sum('quantity')*obj.eventitem_set.filter(item=F('item')).first().quantity)\
						.distinct().filter(item__in=obj.item.all()),			
					AddCommonVegetable.objects.values('unit__name')\
						.annotate(vegetable_name=F('common_vegetable__name'), quantity=Sum('quantity')*obj.eventitem_set.filter(item=F('item')).first().quantity)\
						.distinct().filter(item__in=obj.item.all())
				)		
			except:
				add_vegetables = []					

			for add_vegetable in add_vegetables:
				vegetable_obj = Vegetable.objects.get(name=add_vegetable.get('vegetable_name'))
				unit_obj = Unit.objects.get(name=add_vegetable.get('unit__name'))
				estm_vegetable_qs = EstimatedVegetable.objects.filter(
																	vegetable=vegetable_obj, 
																	# unit=unit_obj
																)
				if estm_vegetable_qs.exists():
					estm_vegetable_obj = estm_vegetable_qs.first()
				else:
					estm_vegetable_obj = EstimatedVegetable.objects.create(
											event=obj,
											vegetable=vegetable_obj, 
											unit=unit_obj
										)
				estm_vegetable_obj.suggested_quantity = float(add_vegetable.get('quantity'))
				estm_vegetable_obj.quantity = estm_vegetable_obj.quantity or estm_vegetable_obj.suggested_quantity
				estm_vegetable_obj.save()


	
			return HttpResponseRedirect(f"/accounts/src/eventvegetable/{obj.id}/change/")

		elif "_view-estimated-others" in request.POST:				
			try:
				add_others = chain(
								AddOther.objects.values('unit__name')\
								.annotate(other_name=F('other__name'), quantity=Sum('quantity')*obj.eventitem_set.filter(item=F('item')).first().quantity)\
								.distinct().filter(item__in=obj.item.all()),				
								AddCommonOther.objects.values('unit__name')\
								.annotate(other_name=F('common_other__name'), quantity=Sum('quantity')*obj.eventitem_set.filter(item=F('item')).first().quantity)\
								.distinct().filter(item__in=obj.item.all())
							)
			except:
				add_others = []					

			for add_other in add_others:
				other_obj = Other.objects.get(name=add_other.get('other_name'))
				unit_obj = Unit.objects.get(name=add_other.get('unit__name'))
				estm_other_qs = EstimatedOther.objects.filter(
																	other=other_obj, 
																	# unit=unit_obj
																)
				if estm_other_qs.exists():
					estm_other_obj = estm_other_qs.first()
				else:
					estm_other_obj = EstimatedOther.objects.create(
											event=obj,
											other=other_obj, 
											unit=unit_obj
										)
				estm_other_obj.suggested_quantity = float(add_other.get('quantity'))
				estm_other_obj.quantity = estm_other_obj.quantity or estm_other_obj.suggested_quantity
				estm_other_obj.save()

			return HttpResponseRedirect(f"/accounts/src/eventother/{obj.id}/change/")

		return super().response_change(request, obj)	


	# def save_formset(self, request, form, formset, change):
	# 	if formset.model!=EventItem:
	# 		return super().save_formset(request, form, formset, change)
	# 	instances = formset.save(commit=False)
	# 	for obj in formset.deleted_objects:
	# 		obj.delete()
	# 	for idx, instance in enumerate(instances):
	# 		if not instance.pk:
	# 			instance.selling_price = instance.item.selling_price
	# 			instance.save()
	# 	formset.save_m2m()




class EstimatedRationAdmin(admin.TabularInline):
	model = EstimatedRation
	extra = 0
	max_num=0
	can_delete = False
	readonly_fields = ('ration', 'suggested_quantity',)
	autocomplete_fields = ['unit']

class EstimatedIngredientAdmin(admin.TabularInline):
	model = EstimatedIngredient
	extra = 0
	max_num=0
	can_delete = False
	readonly_fields = ('ingredient', 'suggested_quantity',)
	autocomplete_fields = ['unit']

class EstimatedVegetableAdmin(admin.TabularInline):
	model = EstimatedVegetable
	extra = 0
	max_num=0
	can_delete = False
	readonly_fields = ('vegetable', 'suggested_quantity',)
	autocomplete_fields = ['unit']

class EstimatedOtherAdmin(admin.TabularInline):
	model = EstimatedOther
	extra = 0
	max_num=0
	can_delete = False
	readonly_fields = ('other', 'suggested_quantity',)
	autocomplete_fields = ['unit']

class EventEstimatedRationAdmin(admin.ModelAdmin):
	change_form_template = 'admin/change_form_estm_item.html'
	list_display = ()
	exclude = ("name", "client", "ref_no", "start_date", "end_date", "is_upcoming", "is_running",
			"is_completed", "location", "deal_amount", "total_item_price", "total_employee_charge",
			"total_luggage_charge", "total_other_charge", "total_amount_paid", "total_amount_due",
			"item", "luggage", "total_event_cost", "note", "total_event_profit",
	)
	inlines = (EstimatedRationAdmin,)	
	
	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		context.update({
			'show_save': False,
			'show_save_and_continue': True,
			'show_save_and_add_another': False,
			'show_delete': False,
			'custom_button_value' : 'Export Rations as PDF',
			'custom_button_name' : '_export-rations-as-pdf',
			'closelink' : f"/accounts/src/event/{context.get('object_id')}/change/",
		})
		return super().render_change_form(request, context, add, change, form_url, obj)

	def response_change(self, request, obj):		
		if "_export-rations-as-pdf" in request.POST:
			name = 'Ration'
			items = EstimatedRation.objects.values('unit__name', 'quantity').annotate(item_name=F('ration__name')).filter(event=obj)
			items = list(items)	
			x = [item.update({'sl_no':idx+1}) for idx, item in enumerate(items)]	

			file_response = render_to_pdf('src/items.html', {
															'request' 	: 	request, 
															'event' 	: 	obj, 
															'name' 		: 	name,
															'items' 	: 	items, 
															'filename'	: 	f'{name}.{obj.ref_no}'
														}
										)
		
			if file_response:
				# self.message_user(request, "Items exported as PDF")	
				return file_response

		return super().response_change(request, obj)	

	def has_delete_permission(self, request, obj=None):
		return False



class EventEstimatedIngredientAdmin(admin.ModelAdmin):
	change_form_template = 'admin/change_form_estm_item.html'
	list_display = ()
	exclude = ("name", "client", "ref_no", "start_date", "end_date", "is_upcoming", "is_running",
			"is_completed", "location", "deal_amount", "total_item_price", "total_employee_charge",
			"total_luggage_charge", "total_other_charge", "total_amount_paid", "total_amount_due",
			"item", "luggage", "total_event_cost", "note", "total_event_profit",
	)
	inlines = (EstimatedIngredientAdmin,)	
	
	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		context.update({
			'show_save': False,
			'show_save_and_continue': True,
			'show_save_and_add_another': False,
			'show_delete': False,
			'custom_button_value' : 'Export Ingredients as PDF',
			'custom_button_name' : '_export-ingredients-as-pdf',
			'closelink' : f"/accounts/src/event/{context.get('object_id')}/change/",
		})
		return super().render_change_form(request, context, add, change, form_url, obj)

	def response_change(self, request, obj):
		if "_export-ingredients-as-pdf" in request.POST:
			name = 'Ingredients'
			items = EstimatedIngredient.objects.values('unit__name', 'quantity').annotate(item_name=F('ingredient__name')).filter(event=obj)
			items = list(items)	
			x = [item.update({'sl_no':idx+1}) for idx, item in enumerate(items)]	

			file_response = render_to_pdf('src/items.html', {
															'request' 	: 	request, 
															'event' 	: 	obj, 
															'name' 		: 	name,
															'items' 	: 	items, 
															'filename'	: 	f'{name}.{obj.ref_no}'
														}
										)
		
			if file_response:
				# self.message_user(request, "Items exported as PDF")	
				return file_response
		return super().response_change(request, obj)	

	def has_delete_permission(self, request, obj=None):
		return False



class EventEstimatedVegetableAdmin(admin.ModelAdmin):
	change_form_template = 'admin/change_form_estm_item.html'
	list_display = ()
	exclude = ("name", "client", "ref_no", "start_date", "end_date", "is_upcoming", "is_running",
			"is_completed", "location", "deal_amount", "total_item_price", "total_employee_charge",
			"total_luggage_charge", "total_other_charge", "total_amount_paid", "total_amount_due",
			"item", "luggage", "total_event_cost", "note", "total_event_profit",
	)
	inlines = (EstimatedVegetableAdmin,)	
	
	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		context.update({
			'show_save': False,
			'show_save_and_continue': True,
			'show_save_and_add_another': False,
			'show_delete': False,
			'custom_button_value' : 'Export Vegetables as PDF',
			'custom_button_name' : '_export-vegetables-as-pdf',
			'closelink' : f"/accounts/src/event/{context.get('object_id')}/change/",
		})
		return super().render_change_form(request, context, add, change, form_url, obj)

	def response_change(self, request, obj):			
		if "_export-vegetables-as-pdf" in request.POST:
			name = 'Vegetables'
			items = EstimatedVegetable.objects.values('unit__name', 'quantity').annotate(item_name=F('vegetable__name')).filter(event=obj)
			items = list(items)	
			x = [item.update({'sl_no':idx+1}) for idx, item in enumerate(items)]	

			file_response = render_to_pdf('src/items.html', {
															'request' 	: 	request, 
															'event' 	: 	obj, 
															'name' 		: 	name,
															'items' 	: 	items, 
															'filename'	: 	f'{name}.{obj.ref_no}'
														}
										)
		
			if file_response:
				# self.message_user(request, "Items exported as PDF")	
				return file_response

		return super().response_change(request, obj)	

	def has_delete_permission(self, request, obj=None):
		return False


class EventEstimatedOtherAdmin(admin.ModelAdmin):
	change_form_template = 'admin/change_form_estm_item.html'
	list_display = ()
	exclude = ("name", "client", "ref_no", "start_date", "end_date", "is_upcoming", "is_running",
			"is_completed", "location", "deal_amount", "total_item_price", "total_employee_charge",
			"total_luggage_charge", "total_other_charge", "total_amount_paid", "total_amount_due",
			"item", "luggage", "total_event_cost", "note", "total_event_profit",
	)
	inlines = (EstimatedOtherAdmin,)	
	
	def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
		context.update({
			'show_save': False,
			'show_save_and_continue': True,
			'show_save_and_add_another': False,
			'show_delete': False,
			'custom_button_value' : 'Export Others as PDF',
			'custom_button_name' : '_export-others-as-pdf',
			'closelink' : f"/accounts/src/event/{context.get('object_id')}/change/",
		})
		return super().render_change_form(request, context, add, change, form_url, obj)

	def response_change(self, request, obj):
		if "_export-others-as-pdf" in request.POST:
			name = 'Others'
			items = EstimatedOther.objects.values('unit__name', 'quantity').annotate(item_name=F('other__name')).filter(event=obj)
			items = list(items)	
			x = [item.update({'sl_no':idx+1}) for idx, item in enumerate(items)]	

			file_response = render_to_pdf('src/items.html', {
															'request' 	: 	request, 
															'event' 	: 	obj, 
															'name' 		: 	name,
															'items' 	: 	items, 
															'filename'	: 	f'{name}.{obj.ref_no}'
														}
										)
		
			if file_response:
				# self.message_user(request, "Items exported as PDF")	
				return file_response

		return super().response_change(request, obj)	

	def has_delete_permission(self, request, obj=None):
		return False


class DateAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	search_fields = ("date__istartswith", )

class WorkDateInline(admin.TabularInline):
	model = WorkDate
	extra = 0
	exclude = ("created_at", "updated_at")
	readonly_fields = ("last_modified_by", )
	autocomplete_fields = ['work_dates']
	
	# def save_model(self, request, obj, form, change):
	# 	print(obj, request.user.username)
	# 	obj.last_modified_by = request.user.username
	# 	super().save_model(request, obj, form, change)


class EmployeeCategoryAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")


class EmployeeTransactionInline(admin.TabularInline):
	model = EmployeeTransaction
	extra = 0
	# readonly_fields = ('amount', 'payment_mode')


class EmployeeAdmin(admin.ModelAdmin):
	list_display = ("show_names", "show_category", "show_phone_numbers", )
	exclude = ("email_password", "transactions", "password", "last_login", "groups", "user_permissions", "date_joined", "is_superuser", "is_staff")
	readonly_fields = ("username", "user_type", "total_amount", "total_amount_paid", "total_amount_due",)
	list_filter = (FirstAreaCodeListFilter, )
	search_fields = ("authuser_ptr__username__istartswith", "authuser_ptr__first_name__istartswith", "authuser_ptr__last_name__istartswith", "authuser_ptr__phone_number__icontains", "employee_category__name__istartswith",)
	inlines = (EmployeeTransactionInline, )

	def show_names(self, obj):
		return f"{obj.first_name if obj.first_name else ''} {obj.last_name if obj.last_name else ''}" 
	
	def show_category(self, obj):
		return obj.employee_category			
	
	def show_phone_numbers(self, obj):
		return str(obj.phone_number)

	show_names.short_description = "Employee name"
	show_category.short_description = "Employee category"
	show_phone_numbers.short_description = "Phone numbers"


class EmployeeWorkAdmin(admin.ModelAdmin):
	list_display = ("show_employee_name", "show_status",)
	exclude = ("last_processed_date", "created_at", "updated_at")		
	# readonly_fields = ("work_dates", )
	inlines = (WorkDateInline, )	
	def show_employee_name(self, obj):
		return f"{obj.employee.first_name if obj.employee.first_name else ''} {obj.employee.last_name if obj.employee.last_name else ''}"
	show_employee_name.short_description = "Employee name"
	def show_status(self, obj):
		return 'Working' if obj.is_working else 'Not Working'
	show_status.short_description = "Status"

	def save_formset(self, request, form, formset, change):
		if formset.model!=WorkDate:
			return super().save_formset(request, form, formset, change)		
		instances = formset.save(commit=False)
		for obj in formset.deleted_objects:
			obj.delete()
		for idx, instance in enumerate(instances):
			if not instance.pk:
				instance.last_modified_by = request.user.username
			start_date = instance.employee_work.event.start_date
			end_date = instance.employee_work.event.end_date	
			if start_date<=instance.work_dates.date<=end_date:	
				instance.save()
			else:
				self.message_user(request, f"Work date must be between event start date({start_date}) and event end date({end_date})", level=messages.ERROR)
		formset.save_m2m()




class VendorCategoryAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")


class VendorTransactionInline(admin.TabularInline):
	model = VendorTransaction
	extra = 0
	# readonly_fields = ('amount', 'payment_mode')


class VendorAdmin(admin.ModelAdmin):
	list_display = ("show_names", "show_category", "show_phone_numbers", )
	exclude = ("email_password", "transactions", "password", "last_login", "groups", "user_permissions", "date_joined", "is_superuser", "is_staff")
	readonly_fields = ("username", "user_type", "total_amount", "total_amount_paid", "total_amount_due",)
	list_filter = (FirstAreaCodeListFilter, )
	search_fields = ("authuser_ptr__username__istartswith", "authuser_ptr__first_name__istartswith", "authuser_ptr__last_name__istartswith", "authuser_ptr__phone_number__icontains", "vendor_category__name__istartswith",)
	inlines = (VendorTransactionInline, )

	def show_names(self, obj):
		return f"{obj.first_name if obj.first_name else ''} {obj.last_name if obj.last_name else ''}" 
	
	def show_category(self, obj):
		return obj.vendor_category			
	
	def show_phone_numbers(self, obj):
		return str(obj.phone_number)

	show_names.short_description = "Vendor name"
	show_category.short_description = "Vendor category"
	show_phone_numbers.short_description = "Phone numbers"



class LuggageCategoryAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	search_fields = ("name__istartswith", )


class LuggageAdmin(admin.ModelAdmin):
	exclude = ("created_at", "updated_at")	
	readonly_fields = ('total_quantity', )
	list_filter = (('luggage_category__name', custom_titled_filter('Catergoy Name')),)
	search_fields = ("name__istartswith",)



# class VendorWorkAdmin(admin.ModelAdmin):
# 	list_display = ("show_vendor_name", "show_status",)
# 	exclude = ("last_processed_date", "created_at", "updated_at")		
# 	# readonly_fields = ("work_dates", )
# 	inlines = (WorkDateInline, )	
# 	def show_vendor_name(self, obj):
# 		return f"{obj.vendor.first_name if obj.vendor.first_name else ''} {obj.vendor.last_name if obj.vendor.last_name else ''}"
# 	show_vendor_name.short_description = "Vendor name"
# 	def show_status(self, obj):
# 		return 'Working' if obj.is_working else 'Not Working'
# 	show_status.short_description = "Status"

# 	def save_formset(self, request, form, formset, change):
# 		if formset.model!=WorkDate:
# 			return super().save_formset(request, form, formset, change)		
# 		instances = formset.save(commit=False)
# 		for obj in formset.deleted_objects:
# 			obj.delete()
# 		for idx, instance in enumerate(instances):
# 			if not instance.pk:
# 				instance.last_modified_by = request.user.username
# 			start_date = instance.vendor_work.event.start_date
# 			end_date = instance.vendor_work.event.end_date	
# 			if start_date<=instance.work_dates.date<=end_date:	
# 				instance.save()
# 			else:
# 				self.message_user(request, f"Work date must be between event start date({start_date}) and event end date({end_date})", level=messages.ERROR)
# 		formset.save_m2m()




admin.site.register(MyWallet, MyWalletAdmin)	

admin.site.register(Dates, DateAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventRation, EventEstimatedRationAdmin)
admin.site.register(EventIngredient, EventEstimatedIngredientAdmin)
admin.site.register(EventVegetable, EventEstimatedVegetableAdmin)
admin.site.register(EventOther, EventEstimatedOtherAdmin)

admin.site.register(EmployeeCategory, EmployeeCategoryAdmin)	
admin.site.register(Employee, EmployeeAdmin)		
admin.site.register(EmployeeWork, EmployeeWorkAdmin)	

admin.site.register(VendorCategory, VendorCategoryAdmin)	
admin.site.register(Vendor, VendorAdmin)		
# admin.site.register(VendorWork, VendorWorkAdmin)	

admin.site.register(Unit, UnitAdmin)

admin.site.register(RationCategory, RationCategoryAdmin)	
admin.site.register(Ration, RationAdmin)	
admin.site.register(CommonRation, CommonRationAdmin)

admin.site.register(IngredientCategory, IngredientCategoryAdmin)	
admin.site.register(Ingredient, IngredientAdmin)	
admin.site.register(CommonIngredient, CommonIngredientAdmin)	

admin.site.register(VegetableCategory, VegetableCategoryAdmin)	
admin.site.register(Vegetable, VegetableAdmin)	
admin.site.register(CommonVegetable, CommonVegetableAdmin)	

admin.site.register(OtherCategory, OtherCategoryAdmin)	
admin.site.register(Other, OtherAdmin)	
admin.site.register(CommonOther, CommonOtherAdmin)

admin.site.register(ItemCategory, ItemCategoryAdmin)

admin.site.register(Item, ItemAdmin)

admin.site.register(LuggageCategory, LuggageCategoryAdmin)	
admin.site.register(Luggage, LuggageAdmin)	
# admin.site.register(EventLuggage, EventLuggageAdmin)


