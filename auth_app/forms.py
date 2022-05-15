from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	username = forms.CharField(widget=forms.TextInput(attrs={
																'class': 'form-control', 
																'placeholder': 'Username', 
															}
	))
	password = forms.CharField(widget=forms.PasswordInput(attrs={
																	'class': 'form-control',
																	'placeholder': 'Password',
																}
	))


	