from django.urls import path

# from calc import views
from .import views


#this is pass function from view
urlpatterns=[path('',views.home,name='home'),
       
             ]