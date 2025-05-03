
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    # PAGES URL'S
    path('', views.main, name="main"),
    path('store/', views.store, name="store"),
    path('single/<int:id>', views.single, name="single"),
    path('ondemand/<str:page>', views.ondemand, name="ondemand"),
    path('services/<str:page>', views.services, name="services"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('about/', views.about, name="about"),
     path('logout/', views.logout, name="logout"),
    # ADMIN URL'S
    path('hq/', views.admin, name="hq"),
    path('hq/orders', views.orders, name="hq-o"),
    path('hq/requests', views.requests, name="hq-r"),
    path('hq/products', views.view_products, name="hq-p"),
    path('hq/add_product', views.add_product, name="hq-p-a"),
    path('hq/edit_product/<str:id>', views.edit_product, name="hq-p-e"),
    path('hq/stats', views.stats, name="hq-st"),
    path('hq/media', views.media, name="hq-m"),
    path('hq/users', views.users, name="hq-u"),
    path('hq/settings', views.settings, name="hq-s"),
    path('hq/logout', views.logout, name="hq-l"),
    # API'S URL's
    path('upload/', views.upload, name="upload"),
    path('api/update_product_img/<str:id>', views.update_product_img, name="update_product_img"),
    path('api/remove_product_img/', views.remove_product_img, name="remove_product_img"),
    path('api/update-request-status/', views.update_request_status, name='update-request-status'),
    path('api/update-order-status/', views.update_order_status, name='update-order-status'),
    path('api/get-product-images/<str:id>', views.get_product_images, name='get_product_images'),
    path('store/get_products', views.products, name="products"),
    path('store/get_categories', views.get_categories, name="categories"),
] + staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
