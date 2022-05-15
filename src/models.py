from django.db import models
from .extra import ContentTypeRestrictedFileField
from auth_app.models import EmployeeUser
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.conf import settings
from contextlib import contextmanager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import CheckConstraint, Q
from . utils import random_with_N_digits
from auth_app.models import AdminUser, EmployeeUser, VendorUser, CustomerUser


class Registration(models.Model):
	license_key 	= 	models.CharField(max_length=255, unique=True)
	secret_key  	=	models.CharField(max_length=255, null=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'registration'

	def __str__(self):
		return F"{self.id}" 

class MyWallet(models.Model):
	balance   		=  	models.FloatField(default=0.0, null=True, blank=True)
	bank_account  	=	models.TextField(null=True, blank=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'my_wallet'
	def __str__(self):
		return F"Rs. {self.balance}" 	

class EmployeeCategory(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'employee_category'

	def __str__(self):
		return F"{self.name}" 	


class Employee(EmployeeUser):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['total_amount', 'total_amount_paid']
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_amount_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	employee_category 	= 	models.ForeignKey(EmployeeCategory, on_delete=models.CASCADE)
	fees_per_day  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	bank_account  		=	models.TextField(null=True, blank=True)
	total_amount   		=  	models.FloatField(default=0.0, null=True, blank=True)
	total_amount_paid  	=	models.FloatField(default=0.0, null=True, blank=True)
	total_amount_due  	=	models.FloatField(default=0.0, null=True, blank=True)
	class Meta:
		managed = True
		db_table = 'employee'

	def __str__(self):
		return f"{self.username} : {self.employee_category}"    


class EmployeeTransaction(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['amount', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_amount_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	employee 			= 	models.ForeignKey(Employee, on_delete=models.CASCADE)
	amount    			=  	models.FloatField(default=0.0, null=True, blank=True)
	payment_mode  		=	models.CharField(max_length=255, null=True, blank=True)
	note    			=  	models.CharField(max_length=512, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   	
	class Meta:
		managed = True
		db_table = 'employee_transaction'

	def __str__(self):
		return f"Rs. {self.amount} by {self.payment_mode if self.payment_mode else 'Unknown mode'} on {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"    



class VendorCategory(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'vendor_category'

	def __str__(self):
		return F"{self.name}" 


class Vendor(VendorUser):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['total_amount', 'total_amount_paid']
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_amount_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	vendor_category 	= 	models.ForeignKey(VendorCategory, on_delete=models.CASCADE)
	bank_account  		=	models.TextField(null=True, blank=True)
	total_amount   		=  	models.FloatField(default=0.0, null=True, blank=True)
	total_amount_paid  	=	models.FloatField(default=0.0, null=True, blank=True)
	total_amount_due  	=	models.FloatField(default=0.0, null=True, blank=True)
	class Meta:
		managed = True
		db_table = 'vendor'

	def __str__(self):
		return f"{self.username} : {self.vendor_category}"    


class VendorTransaction(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['amount', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_amount_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	vendor 				= 	models.ForeignKey(Vendor, on_delete=models.CASCADE)
	amount    			=  	models.FloatField(default=0.0, null=True, blank=True)
	payment_mode  		=	models.CharField(max_length=255, null=True, blank=True)
	note    			=  	models.CharField(max_length=512, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   	
	class Meta:
		managed = True
		db_table = 'vendor_transaction'

	def __str__(self):
		return f"Rs. {self.amount} by {self.payment_mode if self.payment_mode else 'Unknown mode'} on {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"    



class Share(models.Model):
	name 	= 	models.CharField(max_length=255)
	email 	=  	models.EmailField(max_length=500)
	ids 	= 	models.CharField(max_length=255)
	class Meta:
		managed = False 



class Menu(models.Model):
	idx  			=	models.IntegerField(null=True, blank=True, default=0)
	name 			= 	models.CharField(max_length=255)
	menu_pdf 		= 	ContentTypeRestrictedFileField(upload_to='menu-pdfs/', content_types = ['application/pdf'])
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'menu'
		unique_together = (('name', 'menu_pdf'), )

	def __str__(self):
		menu_pdf = self.menu_pdf
		if self.menu_pdf:
			menu_pdf = str(self.menu_pdf).replace('menu-pdfs/', '')
		return F"{self.name} : {menu_pdf}" 

	def save(self, *args, **kwargs):
		if self.pk is None: 
			all_qs = Menu.objects.all()
			qs = all_qs.filter(name=self.name)
			if qs.exists():
				self.idx = qs.first().idx
			else:
				if all_qs.exists():
					idx_list = list(all_qs.distinct().values_list('idx', flat=True))
					self.idx = max(idx_list) + 1
				else:
					self.idx = 1
		super().save(*args, **kwargs)	
		
class Unit(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'unit'
	def __str__(self):
		return F"{self.name}"


class RationCategory(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'ration_category'

	def __str__(self):
		return F"{self.name}" 	


class Ration(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	ration_category  =	models.ForeignKey(RationCategory, on_delete=models.CASCADE, null=True, blank=True)
	purchase_price  =	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  			=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	is_common  		=	models.BooleanField(default=False)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'ration'
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_ration'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_ration'),
		)
		
	def __str__(self):
		return F"{self.name} : {self.selling_price}" 	


class CommonRation(Ration):
	class Meta:
		proxy = True
	def save(self, *args, **kwargs):
		self.is_common = True
		super().save(*args, **kwargs)

class IngredientCategory(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'ingredient_category'

	def __str__(self):
		return F"{self.name}" 	


class Ingredient(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	ingredient_category    	=	models.ForeignKey(IngredientCategory, on_delete=models.CASCADE, null=True, blank=True)
	purchase_price  =	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  			=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	is_common  		=	models.BooleanField(default=False)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'ingredient'
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_ingredient'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_ingredient'),
		)
		
	def __str__(self):
		return F"{self.name} : {self.selling_price}" 	


class CommonIngredient(Ingredient):
	class Meta:
		proxy = True
	def save(self, *args, **kwargs):
		self.is_common = True
		super().save(*args, **kwargs)		


class VegetableCategory(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'vegetable_category'

	def __str__(self):
		return F"{self.name}" 	


class Vegetable(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	vegetable_category =	models.ForeignKey(VegetableCategory, on_delete=models.CASCADE, null=True, blank=True)
	purchase_price  =	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  			=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	is_common  		=	models.BooleanField(default=False)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'vegetable'
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_vegetable'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_vegetable'),
		)
		
	def __str__(self):
		return F"{self.name} : {self.selling_price}" 	


class CommonVegetable(Vegetable):
	class Meta:
		proxy = True
	def save(self, *args, **kwargs):
		self.is_common = True
		super().save(*args, **kwargs)


class OtherCategory(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'other_category'

	def __str__(self):
		return F"{self.name}" 	


class Other(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	other_category  =	models.ForeignKey(OtherCategory, on_delete=models.CASCADE, null=True, blank=True)
	purchase_price  =	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  			=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	is_common  		=	models.BooleanField(default=False)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'other'
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_other'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_other'),
		)

	def __str__(self):
		return F"{self.name} : {self.selling_price}" 	


class CommonOther(Other):
	class Meta:
		proxy = True
	def save(self, *args, **kwargs):
		self.is_common = True
		super().save(*args, **kwargs)

class ItemCategory(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'item_category'

	def __str__(self):
		return F"{self.name}" 	


class Item(models.Model):
	name 				=	models.CharField(max_length=255, unique=True)
	item_category   	=	models.ForeignKey(ItemCategory, on_delete=models.CASCADE, null=True, blank=True)
	rations  			=	models.ManyToManyField(Ration, related_name="item_ration", through='AddRation', blank=True)
	common_rations 		= 	models.ManyToManyField(CommonRation, related_name="item_common_ration", through='AddCommonRation', blank=True)
	ingredients			=	models.ManyToManyField(Ingredient, related_name="item_ingredient", through='AddIngredient', blank=True)
	common_ingredients 	=  	models.ManyToManyField(CommonIngredient, related_name="item_common_ingredient", through='AddCommonIngredient', blank=True)
	vegetables  		=	models.ManyToManyField(Vegetable, related_name="item_vegetable", through='AddVegetable', blank=True)
	common_vegetables 	=  	models.ManyToManyField(CommonVegetable, related_name="item_common_vegetable", through='AddCommonVegetable', blank=True)
	others  			=	models.ManyToManyField(Other, related_name="item_other", through='AddOther', blank=True)
	common_others 		= 	models.ManyToManyField(CommonOther, related_name="item_common_other", through='AddCommonOther', blank=True)
	purchase_price 		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	suggested_selling_price = models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'item'
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_item'),
			CheckConstraint(
				check=Q(suggested_selling_price__gte=0.0),
				name='suggested_selling_price_limit_item'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_item'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_item'),
		)

	def __str__(self):
		return F"{self.name} : {self.item_category} : {self.unit if self.unit else 'per unit'}" 	


class AddRation(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'selling_price', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	item 				= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	ration  			= 	models.ForeignKey(Ration, on_delete=models.CASCADE)	
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'add_ration'
		unique_together = (('item', 'ration', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_add_ration'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_add_ration'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_add_ration'),
		)

	def __str__(self):
		return F"{self.item.name} : {self.ration.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.ration is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.ration.purchase_price
			if self.selling_price==0.0:
				self.selling_price = self.ration.selling_price	
			if self.unit is None or self.unit=='':
				self.unit = self.ration.unit
		super().save(*args, **kwargs)	


class AddCommonRation(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'selling_price', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	item 				= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	common_ration  		= 	models.ForeignKey(CommonRation, on_delete=models.CASCADE)	
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'add_common_ration'
		unique_together = (('item', 'common_ration', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_add_common_ration'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_add_common_ration'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_add_common_ration'),
		)

	def __str__(self):
		return F"{self.item.name} : {self.common_ration.name}" 	

	def save(self, *args, **kwargs):
		if self.pk is None and self.common_ration is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.common_ration.purchase_price
			if self.selling_price==0.0:
				self.selling_price = self.common_ration.selling_price	
			if self.unit is None or self.unit=='':
				self.unit = self.common_ration.unit
		super().save(*args, **kwargs)	



class AddIngredient(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'selling_price', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	item 				= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	ingredient  		= 	models.ForeignKey(Ingredient, on_delete=models.CASCADE)	
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'add_ingredient'
		unique_together = (('item', 'ingredient', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_add_ingredient'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_add_ingredient'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_add_ingredient'),	
		)

	def __str__(self):
		return F"{self.item.name} : {self.ingredient.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.ingredient is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.ingredient.purchase_price
			if self.selling_price==0.0:
				self.selling_price = self.ingredient.selling_price	
			if self.unit is None or self.unit=='':
				self.unit = self.ingredient.unit
		super().save(*args, **kwargs)	


class AddCommonIngredient(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'selling_price', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	item 				= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	common_ingredient  	= 	models.ForeignKey(CommonIngredient, on_delete=models.CASCADE)	
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'add_common_ingredient'
		unique_together = (('item', 'common_ingredient', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_add_common_ingredient'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_add_common_ingredient'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_add_common_ingredient'),
		)

	def __str__(self):
		return F"{self.item.name} : {self.common_ingredient.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.common_ingredient is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.common_ingredient.purchase_price
			if self.selling_price==0.0:
				self.selling_price = self.common_ingredient.selling_price	
			if self.unit is None or self.unit=='':
				self.unit = self.common_ingredient.unit
		super().save(*args, **kwargs)	



class AddVegetable(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'selling_price', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	item 				= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	vegetable  			= 	models.ForeignKey(Vegetable, on_delete=models.CASCADE)	
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'add_vegetable'
		unique_together = (('item', 'vegetable', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_add_vegetable'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_add_vegetable'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_add_vegetable'),
		)

	def __str__(self):
		return F"{self.item.name} : {self.vegetable.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.vegetable is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.vegetable.purchase_price
			if self.selling_price==0.0:
				self.selling_price = self.vegetable.selling_price	
			if self.unit is None or self.unit=='':
				self.unit = self.vegetable.unit
		super().save(*args, **kwargs)	


class AddCommonVegetable(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'selling_price', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	item 				= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	common_vegetable  	= 	models.ForeignKey(CommonVegetable, on_delete=models.CASCADE)	
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'add_common_vegetable'
		unique_together = (('item', 'common_vegetable', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_add_common_vegetable'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_add_common_vegetable'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_add_common_vegetable'),
		)

	def __str__(self):
		return F"{self.item.name} : {self.common_vegetable.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.common_vegetable is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.common_vegetable.purchase_price
			if self.selling_price==0.0:
				self.selling_price = self.common_vegetable.selling_price	
			if self.unit is None or self.unit=='':
				self.unit = self.common_vegetable.unit
		super().save(*args, **kwargs)	



class AddOther(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'selling_price', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	item 				= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	other  				= 	models.ForeignKey(Other, on_delete=models.CASCADE)	
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'add_other'
		unique_together = (('item', 'other', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_add_other'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_add_other'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_add_other'),
		)

	def __str__(self):
		return F"{self.item.name} : {self.other.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.other is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.other.purchase_price
			if self.selling_price==0.0:
				self.selling_price = self.other.selling_price	
			if self.unit is None or self.unit=='':
				self.unit = self.other.unit
		super().save(*args, **kwargs)	


class AddCommonOther(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'selling_price', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	item 				= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	common_other  		= 	models.ForeignKey(CommonOther, on_delete=models.CASCADE)	
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	selling_price  		=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'add_common_other'
		unique_together = (('item', 'common_other', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_add_common_other'),
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_add_common_other'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_add_common_other'),
		)

	def __str__(self):
		return F"{self.item.name} : {self.common_other.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.common_other is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.common_other.purchase_price
			if self.selling_price==0.0:
				self.selling_price = self.common_other.selling_price	
			if self.unit is None or self.unit=='':
				self.unit = self.common_other.unit
		super().save(*args, **kwargs)	




class LuggageCategory(models.Model):
	name 			=	models.CharField(max_length=255, unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'luggage_category'

	def __str__(self):
		return F"{self.name}" 



class Luggage(models.Model):		
	name 				=	models.CharField(max_length=255, unique=True)
	luggage_category   	=	models.ForeignKey(LuggageCategory, on_delete=models.CASCADE, null=True, blank=True)
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)	
	lost_quantity   	=  	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_quantity   	=  	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	lost_charge 		=	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	per_day_charge 		= 	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'luggage'
		constraints = (
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_luggage'),
			CheckConstraint(
				check=Q(lost_quantity__gte=0.0),
				name='lost_quantity_limit_luggage'),
			CheckConstraint(
				check=Q(total_quantity__gte=0.0),
				name='total_quantity_limit_luggage'),
			CheckConstraint(
				check=Q(lost_charge__gte=1.0),
				name='lost_charge_limit_luggage'),
			CheckConstraint(
				check=Q(per_day_charge__gte=1.0),
				name='per_day_charge_limit_luggage'),			
		)

	def __str__(self):
		return F"{self.name} : {self.luggage_category} : {self.unit if self.unit else 'per unit'}" 	

	def save(self, *args, **kwargs):
		self.total_quantity = self.quantity - self.lost_quantity
		super().save(*args, **kwargs)	



class Event(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields1 = ['start_date', 'end_date', ]
		self.__important_fields2 = ['deal_amount', 'total_amount_paid']
		self.__important_fields3 = ['total_item_price', 'total_employee_charge', 'total_luggage_charge', 'total_other_charge', 'total_event_cost']
		for field in self.__important_fields1:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
		for field in self.__important_fields2:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
		for field in self.__important_fields3:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))

	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields1:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields1:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))	

	@contextmanager		
	def has_amount_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields2:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields2:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	@contextmanager		
	def has_cost_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields3:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields3:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))


	name 				=	models.CharField(max_length=512)
	client  			=  	models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
	ref_no  			=  	models.CharField(max_length=6, blank=True)
	start_date  		=  	models.DateField()
	end_date  			=  	models.DateField()
	is_upcoming  		= 	models.BooleanField(default=True)
	is_running  		= 	models.BooleanField(default=False)
	is_completed  		= 	models.BooleanField(default=False)
	location  			=  	models.TextField(null=True, blank=True)
	deal_amount   		=  	models.FloatField(default=0.0, null=True, blank=True)
	total_item_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_employee_charge  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_luggage_charge  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_other_charge  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_event_cost  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_event_profit  =	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_amount_paid  	=	models.FloatField(default=0.0, null=True, blank=True)
	total_amount_due  	=	models.FloatField(default=0.0, null=True, blank=True)	
	item  				=  	models.ManyToManyField(Item, related_name="event_item", through='EventItem')
	luggage  			=  	models.ManyToManyField(Luggage, related_name="event_luggage", through='EventLuggage')
	note 				=  	models.TextField(null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   	
	class Meta:
		managed = True
		db_table = 'event'
		unique_together = (('name', 'client', 'start_date'), ('name', 'client', 'end_date'),)
		constraints = (
			CheckConstraint(
				check=Q(total_item_price__gte=0.0),
				name='total_item_price_limit_event'),
			CheckConstraint(
				check=Q(total_employee_charge__gte=0.0),
				name='total_employee_charge_limit_event'),		
			CheckConstraint(
				check=Q(total_luggage_charge__gte=0.0),
				name='total_luggage_charge_limit_event'),
			CheckConstraint(
				check=Q(total_event_cost__gte=0.0),
				name='total_event_cost_limit_event'),
			CheckConstraint(
				check=Q(total_event_profit__gte=0.0),
				name='total_event_profit_limit_event'),										
		)

	def __str__(self):
		status = ""
		if self.is_upcoming:
			status = "Upcoming"
		elif self.is_running:
			status = "Running"
		elif self.is_completed:
			status = "Completed"
		return f"{self.ref_no} : {self.name} : {status}"

	def save(self, *args, **kwargs):
		if self.ref_no is None or self.ref_no=="": 
			while True:
				ref_no = random_with_N_digits(6)
				if not Event.objects.filter(ref_no=ref_no).exists():
					self.ref_no = ref_no
					break
		self.total_event_profit = self.deal_amount - self.total_event_cost			
		super().save(*args, **kwargs)	



class EventItem(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['item_id', 'total_price', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))	
	event 			= 	models.ForeignKey(Event, on_delete=models.CASCADE)
	item 			= 	models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity   		=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	unit  			=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	selling_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =	models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'event_item'
		unique_together = (('event', 'item', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(selling_price__gte=0.0),
				name='selling_price_limit_event_item'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_event_item'),		
			CheckConstraint(
				check=Q(total_price__gte=0.0),
				name='total_price_limit_event_item'),
		)		
	def __str__(self):
		return f'{self.item}'

	def save(self, *args, **kwargs):
		if self.item is not None: 
			if self.selling_price==0.0:
				self.selling_price = self.item.selling_price
			if self.unit is None or self.unit=='':
				self.unit = self.item.unit	
		self.total_price = self.quantity * self.selling_price		
		super().save(*args, **kwargs)	


class EventRation(Event):
	class Meta:
		proxy = True


class EstimatedRation(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'suggested_quantity', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	event 				= 	models.ForeignKey(EventRation, on_delete=models.CASCADE)
	ration  			= 	models.ForeignKey(Ration, on_delete=models.CASCADE)	
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	suggested_quantity  =  	models.FloatField(validators=[MinValueValidator(0.0),], default=1.0, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'estimated_ration'
		unique_together = (('event', 'ration',),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_estimated_ration'),
			CheckConstraint(
				check=Q(suggested_quantity__gte=0.0),
				name='suggested_quantity_limit_estimated_ration'),
			CheckConstraint(
				check=Q(quantity__gte=0.0),
				name='quantity_limit_estimated_ration'),			
		)

	def __str__(self):
		return F"{self.event.ref_no} : {self.ration.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.ration is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.ration.purchase_price
			if self.unit is None or self.unit=='':
				self.unit = self.ration.unit
		super().save(*args, **kwargs)	


class EventIngredient(Event):
	class Meta:
		proxy = True


class EstimatedIngredient(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'suggested_quantity', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	event 				= 	models.ForeignKey(EventIngredient, on_delete=models.CASCADE)
	ingredient  		= 	models.ForeignKey(Ingredient, on_delete=models.CASCADE)	
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	suggested_quantity  =  	models.FloatField(validators=[MinValueValidator(0.0),], default=1.0, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'estimated_ingredient'
		unique_together = (('event', 'ingredient',),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_estimated_ingredient'),
			CheckConstraint(
				check=Q(suggested_quantity__gte=0.0),
				name='suggested_quantity_limit_estimated_ingredient'),	
			CheckConstraint(
				check=Q(quantity__gte=0.0),
				name='quantity_limit_estimated_ingredient'),						
		)

	def __str__(self):
		return F"{self.event.ref_no} : {self.ingredient.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.ingredient is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.ingredient.purchase_price
			if self.unit is None or self.unit=='':
				self.unit = self.ingredient.unit
		super().save(*args, **kwargs)	



class EventVegetable(Event):
	class Meta:
		proxy = True


class EstimatedVegetable(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'suggested_quantity', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	event 				= 	models.ForeignKey(EventVegetable, on_delete=models.CASCADE)
	vegetable  			= 	models.ForeignKey(Vegetable, on_delete=models.CASCADE)	
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	suggested_quantity  =  	models.FloatField(validators=[MinValueValidator(0.0),], default=1.0, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'estimated_vegetable'
		unique_together = (('event', 'vegetable',),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_estimated_vegetable'),
			CheckConstraint(
				check=Q(suggested_quantity__gte=0.0),
				name='suggested_quantity_limit_estimated_vegetable'),
			CheckConstraint(
				check=Q(quantity__gte=0.0),
				name='quantity_limit_estimated_vegetable'),						
		)

	def __str__(self):
		return F"{self.event.ref_no} : {self.vegetable.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.vegetable is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.vegetable.purchase_price
			if self.unit is None or self.unit=='':
				self.unit = self.vegetable.unit
		super().save(*args, **kwargs)	


class EventOther(Event):
	class Meta:
		proxy = True

class EstimatedOther(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['purchase_price', 'suggested_quantity', 'quantity', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	event 				= 	models.ForeignKey(EventOther, on_delete=models.CASCADE)
	other  				= 	models.ForeignKey(Other, on_delete=models.CASCADE)	
	unit  				=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	suggested_quantity  =  	models.FloatField(validators=[MinValueValidator(0.0),], default=1.0, null=True, blank=True)
	quantity   			=  	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	purchase_price  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'estimated_other'
		unique_together = (('event', 'other',),)
		constraints = (
			CheckConstraint(
				check=Q(purchase_price__gte=0.0),
				name='purchase_price_limit_estimated_other'),
			CheckConstraint(
				check=Q(suggested_quantity__gte=0.0),
				name='suggested_quantity_limit_estimated_other'),
			CheckConstraint(
				check=Q(quantity__gte=0.0),
				name='quantity_limit_estimated_other'),						
		)

	def __str__(self):
		return F"{self.event.ref_no} : {self.other.name}" 

	def save(self, *args, **kwargs):
		if self.pk is None and self.other is not None: 
			if self.purchase_price==0.0:
				self.purchase_price = self.other.purchase_price
			if self.unit is None or self.unit=='':
				self.unit = self.other.unit
		super().save(*args, **kwargs)	



class EventLuggage(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields1 = ['luggage_id', 'quantity', 'total_days']
		self.__important_fields2 = ['return_quantity']
		self.__important_fields3 = ['total_charge', 'total_lost_charge']
		for field in self.__important_fields1:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
		for field in self.__important_fields2:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
		for field in self.__important_fields3:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))

	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields1:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields1:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))	
	@contextmanager			
	def has_lost(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields2:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields2:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))	

	@contextmanager			
	def has_charge_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields3:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields3:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))	


	event 			= 	models.ForeignKey(Event, on_delete=models.CASCADE)
	luggage 		= 	models.ForeignKey(Luggage, on_delete=models.CASCADE)
	quantity   		=  	models.FloatField(validators=[MinValueValidator(1.0),], default=1.0, null=True, blank=True)
	return_quantity =  	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	unit  			=	models.ForeignKey(Unit, on_delete=models.CASCADE, default=1, null=True, blank=True)
	per_day_charge  =	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_days  	=	models.IntegerField(validators=[MinValueValidator(1),], default=1, null=True, blank=True)
	total_charge  	=	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	total_lost_charge=  	models.FloatField(validators=[MinValueValidator(0.0),], default=0.0, null=True, blank=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =	models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'event_luggage'
		unique_together = (('event', 'luggage', 'unit'),)
		constraints = (
			CheckConstraint(
				check=Q(per_day_charge__gte=0.0),
				name='per_day_charge_limit_event_luggage'),
			CheckConstraint(
				check=Q(quantity__gte=1.0),
				name='quantity_limit_event_luggage'),	
			CheckConstraint(
				check=Q(return_quantity__gte=0.0),
				name='return_quantity_limit_event_luggage'),						
			CheckConstraint(
				check=Q(total_days__gte=1),
				name='total_days_limit_event_luggage'),
			CheckConstraint(
				check=Q(total_charge__gte=0.0),
				name='total_charge_limit_event_luggage'),
			CheckConstraint(
				check=Q(total_lost_charge__gte=0.0),
				name='total_lost_charge_limit_event_luggage'),			
		)	

	def __str__(self):
		return f'{self.luggage}'

	def save(self, *args, **kwargs):
		if self.luggage is not None: 
			if self.per_day_charge==0.0:
				self.per_day_charge = self.luggage.per_day_charge
			if self.unit is None or self.unit=='':
				self.unit = self.luggage.unit
		super().save(*args, **kwargs)	



class EventTransaction(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['amount', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_amount_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))

	event 				= 	models.ForeignKey(Event, on_delete=models.CASCADE)
	amount    			=  	models.FloatField(default=0.0, null=True, blank=True)
	payment_mode  		=	models.CharField(max_length=255, null=True, blank=True)
	note    			=  	models.CharField(max_length=512, null=True, blank=True)
	created_at      	=   models.DateTimeField(auto_now_add=True)
	updated_at      	=   models.DateTimeField(auto_now=True)   	
	class Meta:
		managed = True
		db_table = 'event_transaction'

	def __str__(self):
		return f"Rs. {self.amount} by {self.payment_mode if self.payment_mode else 'Unknown mode'} on {self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"    



class Dates(models.Model):
	date    		=  	models.DateField(unique=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True) 
	class Meta:
		managed = True
		db_table = 'dates'

	def __str__(self):
		return f"{self.date}"  


class EmployeeWork(models.Model):
	employee 		=	models.ForeignKey(Employee, on_delete=models.CASCADE)
	event 			=	models.ForeignKey(Event, on_delete=models.CASCADE)
	is_working  	=	models.BooleanField(default=False)
	work_dates  	=  	models.ManyToManyField(Dates, related_name="work_date_dates", through='WorkDate')
	last_processed_date = models.ManyToManyField(Dates, related_name="work_date_last_processed_date")
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =   models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'employee_work'
		unique_together = (('employee', 'event'), )

	def __str__(self):
		return f"{self.employee.username} : {'Working' if self.is_working else 'Not Working'} : {self.event.name}"    


class WorkDate(models.Model):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.__important_fields = ['work_dates_id', ]
		for field in self.__important_fields:
			orig = '__original_%s' % field
			setattr(self, orig, getattr(self, field))
	@contextmanager		
	def has_changed(self, created=False):
		changed = created
		if not created:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				if getattr(self, orig) != getattr(self, field):
					changed = True
					break
		yield changed
		if changed:
			for field in self.__important_fields:
				orig = '__original_%s' % field
				setattr(self, orig, getattr(self, field))	
	employee_work 	= 	models.ForeignKey(EmployeeWork, on_delete=models.CASCADE)
	work_dates 		= 	models.ForeignKey(Dates, on_delete=models.CASCADE)
	last_modified_by= 	models.CharField(max_length=255, null=True, blank=True)
	created_at      =   models.DateTimeField(auto_now_add=True)
	updated_at      =	models.DateTimeField(auto_now=True)   
	class Meta:
		managed = True
		db_table = 'work_date'
		unique_together = (('employee_work', 'work_dates',),)
	def __str__(self):
		return f'{self.employee_work}'












# # ItemCommonRation
# # ItemIngredient
# # ItemCommonIngredient
# # ItemVegetable
# # ItemCommonVegetable
# # ItemOther
# # ItemCommonOther
# @receiver(m2m_changed, sender=Item.rations.through)
# def item_rations_change(sender, instance, action, **kwargs):
# 	total_purchase_price = 0
# 	total_selling_price = 0
# 	rations 	= 	instance.rations.all()
# 	for ration in rations:
# 		total_purchase_price += ration.purchase_price
# 		total_selling_price+= ration.selling_price
# 	save = False	
# 	if action == 'post_add':
# 		instance.purchase_price += total_purchase_price	
# 		instance.suggested_selling_price += total_selling_price
# 		save = True
# 		instance.save()
# 	elif action in ['post_remove', 'post_clear']:
# 		instance.purchase_price -= total_purchase_price	
# 		instance.suggested_selling_price -= total_selling_price
# 		save = True
# 	if save:
# 		instance.save()		


# @receiver(m2m_changed, sender=Item.common_rations.through)
# def item_common_rations_change(sender, instance, action, **kwargs):
# 	total_purchase_price = 0
# 	total_selling_price = 0
# 	common_rations 	= 	instance.common_rations.all()
# 	for common_ration in common_rations:
# 		total_purchase_price += common_ration.purchase_price
# 		total_selling_price+= common_ration.selling_price
# 	save = False	
# 	if action == 'post_add':
# 		instance.purchase_price += total_purchase_price	
# 		instance.suggested_selling_price += total_selling_price
# 		save = True
# 		instance.save()
# 	elif action in ['post_remove', 'post_clear']:
# 		instance.purchase_price -= total_purchase_price	
# 		instance.suggested_selling_price -= total_selling_price
# 		save = True
# 	if save:
# 		instance.save()		


# @receiver(m2m_changed, sender=Item.ingredients.through)
# def item_ingredients_change(sender, instance, action, **kwargs):
# 	total_purchase_price = 0
# 	total_selling_price = 0
# 	ingredients 	= 	instance.ingredients.all()
# 	for ingredient in ingredients:
# 		total_purchase_price += ingredient.purchase_price
# 		total_selling_price+= ingredient.selling_price
# 	save = False	
# 	if action == 'post_add':
# 		instance.purchase_price += total_purchase_price	
# 		instance.suggested_selling_price += total_selling_price
# 		save = True
# 		instance.save()
# 	elif action in ['post_remove', 'post_clear']:
# 		instance.purchase_price -= total_purchase_price	
# 		instance.suggested_selling_price -= total_selling_price
# 		save = True
# 	if save:
# 		instance.save()		


# @receiver(m2m_changed, sender=Item.common_ingredients.through)
# def item_common_ingredients_change(sender, instance, action, **kwargs):
# 	total_purchase_price = 0
# 	total_selling_price = 0
# 	common_ingredients 	= 	instance.common_ingredients.all()
# 	for common_ingredient in common_ingredients:
# 		total_purchase_price += common_ingredient.purchase_price
# 		total_selling_price+= common_ingredient.selling_price
# 	save = False	
# 	if action == 'post_add':
# 		instance.purchase_price += total_purchase_price	
# 		instance.suggested_selling_price += total_selling_price
# 		save = True
# 		instance.save()
# 	elif action in ['post_remove', 'post_clear']:
# 		instance.purchase_price -= total_purchase_price	
# 		instance.suggested_selling_price -= total_selling_price
# 		save = True
# 	if save:
# 		instance.save()		


# @receiver(m2m_changed, sender=Item.vegetables.through)
# def item_vegetables_change(sender, instance, action, **kwargs):
# 	total_purchase_price = 0
# 	total_selling_price = 0
# 	vegetables 	= 	instance.vegetables.all()
# 	for vegetable in vegetables:
# 		total_purchase_price += vegetable.purchase_price
# 		total_selling_price+= vegetable.selling_price
# 	save = False	
# 	if action == 'post_add':
# 		instance.purchase_price += total_purchase_price	
# 		instance.suggested_selling_price += total_selling_price
# 		save = True
# 		instance.save()
# 	elif action in ['post_remove', 'post_clear']:
# 		instance.purchase_price -= total_purchase_price	
# 		instance.suggested_selling_price -= total_selling_price
# 		save = True
# 	if save:
# 		instance.save()		


# @receiver(m2m_changed, sender=Item.common_vegetables.through)
# def item_common_vegetables_change(sender, instance, action, **kwargs):
# 	total_purchase_price = 0
# 	total_selling_price = 0
# 	common_vegetables 	= 	instance.common_vegetables.all()
# 	for common_vegetable in common_vegetables:
# 		total_purchase_price += common_vegetable.purchase_price
# 		total_selling_price+= common_vegetable.selling_price
# 	save = False	
# 	if action == 'post_add':
# 		instance.purchase_price += total_purchase_price	
# 		instance.suggested_selling_price += total_selling_price
# 		save = True
# 		instance.save()
# 	elif action in ['post_remove', 'post_clear']:
# 		instance.purchase_price -= total_purchase_price	
# 		instance.suggested_selling_price -= total_selling_price
# 		save = True
# 	if save:
# 		instance.save()		


# @receiver(m2m_changed, sender=Item.others.through)
# def item_others_change(sender, instance, action, **kwargs):
# 	total_purchase_price = 0
# 	total_selling_price = 0
# 	others 	= 	instance.others.all()
# 	for other in others:
# 		total_purchase_price += other.purchase_price
# 		total_selling_price+= other.selling_price
# 	save = False	
# 	if action == 'post_add':
# 		instance.purchase_price += total_purchase_price	
# 		instance.suggested_selling_price += total_selling_price
# 		save = True
# 		instance.save()
# 	elif action in ['post_remove', 'post_clear']:
# 		instance.purchase_price -= total_purchase_price	
# 		instance.suggested_selling_price -= total_selling_price
# 		save = True
# 	if save:
# 		instance.save()		


# @receiver(m2m_changed, sender=Item.common_others.through)
# def item_common_others_change(sender, instance, action, **kwargs):
# 	total_purchase_price = 0
# 	total_selling_price = 0
# 	common_others 	= 	instance.common_others.all()
# 	for common_other in common_others:
# 		total_purchase_price += common_other.purchase_price
# 		total_selling_price+= common_other.selling_price
# 	save = False	
# 	if action == 'post_add':
# 		instance.purchase_price += total_purchase_price	
# 		instance.suggested_selling_price += total_selling_price
# 		save = True
# 		instance.save()
# 	elif action in ['post_remove', 'post_clear']:
# 		instance.purchase_price -= total_purchase_price	
# 		instance.suggested_selling_price -= total_selling_price
# 		save = True
# 	if save:
# 		instance.save()		

































