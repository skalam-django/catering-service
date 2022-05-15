from django.conf.urls import url
from auth_app import views

app_name='auth_app'

urlpatterns = [
	url(r'^login/', views.Login.as_view(), name='login')
]
