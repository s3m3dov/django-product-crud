from django.urls import path

from .views import (
    productCreateView,
    productListView,
    productView,
    productUpdateView,
    productDeleteView,
)

urlpatterns = [
    path('', productListView, name='product-list'),
    path('create', productCreateView, name='product-create'),
    path('<uuid:pk>/', productView, name='product-edit'),
    path('update/<uuid:pk>/', productUpdateView, name='product-update'),
    path('delete/<uuid:pk>/', productDeleteView, name='product-delete'),
]
