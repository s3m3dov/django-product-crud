from django.urls import path

from apps.product.views import (
    ProductCreateView,
    ProductListView,
    ProductView,
    ProductUpdateView,
    productDeleteView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('create', ProductCreateView.as_view(), name='product-create'),
    path('<uuid:pk>/', ProductView.as_view(), name='product-edit'),
    path('update/<uuid:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('delete/<uuid:pk>/', productDeleteView, name='product-delete'),
]
