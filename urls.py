from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.home,name = "home"),
    path('common/',views.common,name='common'),
    path('register/',views.register,name = 'register'),
    path('login/',views.login,name = 'login'),
     path('profile/', views.user_profile, name='user_profile'),
    path('greeting/<int:face_id>/', views.Greeting, name='greeting'),

]
