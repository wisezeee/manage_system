from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import main_page, menu_list, supplier_list, order_list, order_create, order_detail, MenuListAPIView, \
    SupplierListAPIView, OrderListCreateAPIView, OrderDetailAPIView, OrderDeleteAPIView
from .views import register
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('', main_page, name='main_page'),
    path('menu/', menu_list, name='menu_list'),
    path('vendors/', supplier_list, name='supplier_list'),
    path('orders/', order_list, name='order_list'),
    path('orders/create/', order_create, name='order_create'),
    path('orders/<uuid:order_id>/', order_detail, name='order_detail'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('api/orders/', OrderListCreateAPIView.as_view(), name='order_list_api'),
    path('api/orders/<uuid:order_id>/', OrderDetailAPIView.as_view(), name='order_detail_api'),
    path('api/orders/<uuid:order_id>/delete', OrderDeleteAPIView.as_view(), name='order_delete_api'),
    path('api/menu/', MenuListAPIView.as_view(), name='menu_list_api'),
    path('api/vendors/', SupplierListAPIView.as_view(), name='supplier_list_api'),
]
