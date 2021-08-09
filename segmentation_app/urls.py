from django.urls import path, include
from . import views
urlpatterns = [
	path('',views.home,name='sg_home'),
	path('fetalhc',views.hchome,name='hc_home'),
]
