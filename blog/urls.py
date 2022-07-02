

from django.urls import path
from . import views
#from django.contrib import admin
admin_name = 'blog'


urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('<str:title>/',views.post_detail,name='post_detail'),
    path('<int:id>/share',views.post_share,name='post_share')
    
]
