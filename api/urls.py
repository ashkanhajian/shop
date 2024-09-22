from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='products_list_api'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
]
