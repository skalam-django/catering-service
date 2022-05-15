from django.forms import ModelForm, TextInput, FileInput, EmailInput, HiddenInput, ValidationError
from django.core import validators
from src.models import Menu, Share


class MenuForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.Meta.fields:
			if field in self.Meta.required:
				self.fields[field].required = True
			else:	
				self.fields[field].required = False

	class Meta:
		model = Menu
		fields = ['name', 'menu_pdf']
		widgets = {
			'name' 		: TextInput(attrs={'placeholder': 'Menu Name', 'maxlength':255 }),
			'menu_pdf' 	: FileInput(attrs={'accept': 'application/pdf'}),
		}

		required = ['name', 'menu_pdf']



class ShareForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.Meta.fields:
			if field in self.Meta.required:
				self.fields[field].required = True
			else:	
				self.fields[field].required = False

	class Meta:
		model = Share
		fields = ['name', 'email', 'ids']
		widgets = {
			'name' 		: TextInput(attrs={'placeholder': 'Menu Name', 'maxlength':255, 'icon': 'widgets'}),
			'email' 	: EmailInput(attrs={'placeholder': 'To (Email)', 'maxlength':500, 'icon': 'email' }),
			'ids' 		: HiddenInput(attrs={'type':'hidden'}),
		}

		required = ['name', 'email']
