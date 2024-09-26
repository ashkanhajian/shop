from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view(), name='products_list_api'),
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
    path('users/', views.UserListAPIView.as_view(), name='user_list_api'),
    path('register/', views.UserRegisterAPIView.as_view(), name='register_api')
]
