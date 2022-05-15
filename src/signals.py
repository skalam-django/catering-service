from django.conf import settings
from django.forms.models import model_to_dict
import datetime
import traceback

def populate_default_data(sender, **kwargs):
	from django.contrib.auth import get_user_model
	from src.models import Unit
	auth_qs = get_user_model().objects.filter(is_superuser=True)
	if not auth_qs.exists():
		superuser_obj = get_user_model().objects.create_superuser(
													username 	= None,
													phone_number= '+918618902284',
													email 		= 'skalam.django@gmail.com',
													password 	= 'admin@123'
												)
		superuser_obj.user_password = 'admin@123'
		superuser_obj.first_name = 'Sk Khurshid'
		superuser_obj.last_name = 'Alam'
		superuser_obj.save()

	for unit in settings.UNITS:
		unit_qs = Unit.objects.filter(name=unit)
		if not unit_qs.exists():
			Unit.objects.create(name=unit)
		

def update_employee_due(sender, instance, created, **kwargs):
	save = False
	with instance.has_amount_changed() as changed:
		save = changed
		if changed:
			instance.total_amount_due  = instance.total_amount - instance.total_amount_paid
	if save:
		instance.save()

def employee_transactions(sender, instance, created, **kwargs):
	employee = instance.employee
	save = False
	with instance.has_amount_changed(created) as changed:
		save = changed
		if changed:
			if created:
				__original_amount = 0
			else:
				__original_amount = instance.__original_amount
			employee.total_amount_paid += instance.amount - __original_amount
			from .models import MyWallet
			acc_obj, _ = MyWallet.objects.get_or_create()
			acc_obj.balance -= instance.amount - __original_amount
			acc_obj.save()
	if save:
		employee.save()

def delete_employee_transactions(sender, instance, using, **kwargs):
	employee = instance.employee
	employee.total_amount_paid -= instance.amount
	employee.save()
	from .models import MyWallet
	acc_obj, _ = MyWallet.objects.get_or_create()
	acc_obj.balance += instance.amount
	acc_obj.save()

def update_event_due(sender, instance, created, **kwargs):
	save = False
	with instance.has_amount_changed() as changed:
		save = changed
		if changed:
			instance.total_amount_due  = instance.deal_amount - instance.total_amount_paid			
	if save:
		instance.save()
		

def update_event_costs(sender, instance, created, **kwargs):
	save = False
	with instance.has_cost_changed() as changed:
		save = changed
		if changed:
			if created:
				__original_total_event_cost = 0
			else:	
				__original_total_event_cost = instance.__original_total_event_cost
			total_event_cost = instance.total_item_price + instance.total_employee_charge + instance.total_luggage_charge + instance.total_other_charge
			instance.total_event_cost = total_event_cost
			net_total_event_cost =  instance.total_event_cost - __original_total_event_cost
			if net_total_event_cost!=0:
				from .models import MyWallet
				acc_obj, _ = MyWallet.objects.get_or_create()
				acc_obj.balance -= net_total_event_cost
				acc_obj.save()	
	if save:
		instance.save()


def update_event_item_price(sender, instance, created, **kwargs):
	event = instance.event
	save = False
	with instance.has_changed(created) as changed:
		save = changed
		if changed:
			total_item_price = 0
			for item in event.eventitem_set.all():
				total_item_price += item.total_price 
			event.total_item_price = total_item_price
	if save:
		event.save()	

def delete_event_item_price(sender, instance, using, **kwargs):
	event = instance.event
	total_item_price = 0
	for item in event.eventitem_set.all():
		total_item_price += item.total_price 
	event.total_item_price = total_item_price
	event.save()



def update_event_luggage_price(sender, instance, created, **kwargs):
	event = instance.event
	save = False

	with instance.has_lost(created) as changed:
		save = changed
		if changed:
			if created:
				__original_return_quantity = 0
			else:
				__original_return_quantity = instance.__original_return_quantity

			if instance.return_quantity>instance.quantity:
				instance.return_quantity = instance.quantity
			return_quantity = instance.return_quantity - __original_return_quantity
			if return_quantity>0:
				lost_quantity = instance.quantity - return_quantity
				if lost_quantity>0:
					instance.luggage.lost_quantity += lost_quantity
					instance.luggage.save()
					total_lost_charge = lost_quantity * instance.luggage.lost_charge	
					print("total_lost_charge: ", total_lost_charge)
					instance.total_lost_charge += total_lost_charge	

	with instance.has_changed(created) as changed:
		save = changed
		if changed:
			if created:
				__original_quantity = 0
				__original_total_days = 0
			else:
				__original_quantity = instance.__original_quantity	
				__original_total_days = instance.__original_total_days

			quantity = instance.quantity - __original_quantity
			total_days = instance.total_days - __original_total_days
			if quantity>0 or total_days>0:
				total_charge = instance.quantity*instance.luggage.per_day_charge*instance.total_days
				instance.total_charge = total_charge

	with instance.has_charge_changed(created) as changed:
		save = changed
		if changed:
			if created:
				__original_total_charge = 0
				__original_total_lost_charge = 0
			else:
				__original_total_charge = instance.__original_total_charge	
				__original_total_lost_charge = instance.__original_total_lost_charge
			event.total_luggage_charge += instance.total_charge - __original_total_charge + instance.total_lost_charge - __original_total_lost_charge

	if save:
		instance.save()
		event.save()	

def delete_event_luggage_price(sender, instance, using, **kwargs):
	event = instance.event
	luggage = instance.luggage
	event.total_luggage_charge -= instance.total_charge + instance.total_lost_charge
	if instance.return_quantity>0:
		lost_quantity = instance.return_quantity - instance.quantity 
		luggage.lost_quantity += lost_quantity 
		luggage.save()
	event.save()

def event_transactions(sender, instance, created, **kwargs):
	event = instance.event
	save = False
	with instance.has_amount_changed(created) as changed:
		save = changed
		if changed:
			if created:
				__original_amount = 0
			else:
				__original_amount = instance.__original_amount
			event.total_amount_paid += instance.amount - __original_amount
			from .models import MyWallet
			acc_obj, _ = MyWallet.objects.get_or_create()
			acc_obj.balance += instance.amount - __original_amount
			acc_obj.save()			
	if save:
		event.save()

def delete_event_transactions(sender, instance, using, **kwargs):
	event = instance.event
	event.total_amount_paid -= instance.amount
	event.save()
	from .models import MyWallet
	acc_obj, _ = MyWallet.objects.get_or_create()
	acc_obj.balance -= instance.amount
	acc_obj.save()



# def update_amount_for_workdates(sender, instance, created, **kwargs):
# 	if instance.has_changed(created):
# 		qs = instance.work_dates.all()
# 		if instance.is_working:
# 			if not qs.exists():
# 				employee = instance.employee
# 				employee.total_amount += employee.fees_per_day
# 				employee.save()
# 		else:
# 			if qs.exists():
# 				qs.delete()
# 				employee = instance.employee
# 				employee.total_amount -= employee.fees_per_day
# 				employee.save()			


def update_work(sender, instance, created, **kwargs):
	save = False
	with instance.has_changed(created) as changed:
		save = changed
		employee_work = instance.employee_work
		employee = employee_work.employee
		date = instance.work_dates.date
		event = employee_work.event
		start_date = event.start_date
		end_date = event.end_date	
		if start_date>date or end_date<date:	
			raise Exception(f"Work date must be between event start date({start_date}) and event end date({end_date})")
		employee.total_amount += employee.fees_per_day
		event.total_employee_charge += employee.fees_per_day
		print("instance.last_modified_by: ", instance.last_modified_by)
		if instance.last_modified_by is None:
			if employee_work.last_processed_date.filter(date=date).exists():
				print("update_work already executed by system!")
				save = False
				return
			employee_work.last_processed_date.add(instance.work_dates)

		if date==datetime.date.today():
			employee_work.is_working = True
		else:
			employee_work.is_working = False		
	if save:
		employee.save()
		event.save()
		employee_work.save()
			

def delete_work(sender, instance, using, **kwargs):
	employee_work = instance.employee_work
	employee = employee_work.employee
	employee.total_amount -= employee.fees_per_day
	employee.save()
	event = employee_work.event
	event.total_employee_charge -= employee.fees_per_day
	event.save()
	if instance.work_dates.date==datetime.date.today():
		employee_work.is_working = False
	employee_work.save()


def update_prices(sender, instance, created, **kwargs):
	save = False
	item = instance.item
	with instance.has_changed(created) as changed:
		save = changed
		if changed:
			if created:
				__original_quantity = 0
				__original_purchase_price = 0
				__original_selling_price = 0
			else:
				__original_quantity = instance.__original_quantity
				__original_purchase_price = instance.__original_purchase_price
				__original_selling_price = instance.__original_selling_price
			item.purchase_price +=  instance.quantity*instance.purchase_price - __original_quantity*__original_purchase_price
			item.suggested_selling_price += instance.quantity*instance.selling_price - __original_quantity*__original_selling_price
	if save:	
		item.save()

def delete_prices(sender, instance, using, **kwargs):
	item = instance.item
	item.purchase_price -=  instance.quantity*instance.purchase_price
	item.suggested_selling_price -= instance.quantity*instance.selling_price
	item.save()


def event_status_update(sender, instance, created, **kwargs):
	save = False
	from .models import EmployeeWork
	with instance.has_changed(created) as changed:
		if instance.start_date > datetime.date.today():
			if not instance.is_upcoming:
				instance.is_upcoming = True
				instance.is_running  = False
				instance.is_completed= False
				save = True
				empw_qs = EmployeeWork.objects.filter(event=instance)
				if empw_qs.exists():
					for empw_obj in empw_qs:
						empw_obj.is_working = False
						empw_obj.save()					
		elif instance.end_date < datetime.date.today():
			if not instance.is_completed:
				instance.is_upcoming  = False
				instance.is_running  = False
				instance.is_completed = True
				save = True
				empw_qs = EmployeeWork.objects.filter(event=instance)
				if empw_qs.exists():
					for empw_obj in empw_qs:
						empw_obj.is_working = False
						empw_obj.save()			
		else:
			if not instance.is_running:
				instance.is_upcoming  = False
				instance.is_completed = False
				instance.is_running  = True
				save = True
			empw_qs = EmployeeWork.objects.filter(event=instance)
			if empw_qs.exists():
				for empw_obj in empw_qs:
					if not empw_obj.work_dates.filter(date=datetime.date.today()).exists():
						empw_obj.is_working = True
						empw_obj.save()
			
	if save:
		instance.save()
