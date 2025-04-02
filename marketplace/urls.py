
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # PAGES URL'S
    path('', views.main, name="main"),
    path('store/', views.store, name="store"),
    path('ondemand/<str:page>', views.ondemand, name="ondemand"),
    path('services/<str:page>', views.services, name="services"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('about/', views.about, name="about"),
    # ADMIN URL'S
    path('hq/', views.admin, name="hq"),
    path('hq/requests', views.requests, name="hq-r"),
    path('hq/request/<str:id>', views.view_request, name="hq-r-v"),
    path('hq/products', views.products, name="hq-p"),
    path('hq/stats', views.stats, name="hq-st"),
    path('hq/media', views.media, name="hq-m"),
    path('hq/users', views.users, name="hq-u"),
    path('hq/settings', views.settings, name="hq-s"),
    path('hq/logout', views.logout, name="hq-l"),
    # API'S URL's
    path('upload/', views.upload, name="upload"),
]
