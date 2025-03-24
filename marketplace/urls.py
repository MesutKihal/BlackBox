
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name="main"),
    path('store/', views.store, name="store"),
    path('ondemand/<str:page>', views.ondemand, name="ondemand"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('about/', views.about, name="about")
]
