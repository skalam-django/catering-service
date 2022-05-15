from django.conf.urls import url
from src import views

app_name='src'


urlpatterns = [

	url(r'^items/$', views.items, name='items'),
	url(r'^share-menu$', views.ShareMenu.as_view(), name='share-menu'),
	url(r'^$', views.MenuView.as_view(), name='menu'),
]
