from django.urls import path

from apps.product.views import (
    ProductCreateView,
    ProductListView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('create', ProductCreateView.as_view(), name='product-create'),
    path('<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('update/<uuid:pk>/', ProductUpdateView.as_view(), name='product-update'),
    path('delete/<uuid:pk>/', ProductDeleteView.as_view(), name='product-delete'),
]
