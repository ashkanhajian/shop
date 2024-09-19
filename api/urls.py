from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('products/', views.ProductDetailAPIView.as_view(), name='products_list_api'),
    path('products/<slug:slug>/', views.ProductDetailAPIView.as_view(), name='products_detail_api'),
]
