from django.urls import path
from market.views import ProductIndex, ProductAdd, ProductDetail, ProductUpdate, ProductDelete, CategoryIndex, \
    AddToCart, CartView, RemoveFromCartView

urlpatterns = [
    path("", ProductIndex.as_view(), name='index'),
    path('product/add/', ProductAdd.as_view(), name='product_add'),
    path('product/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('product/<int:pk>/edit/', ProductUpdate.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('products/<str:category_code>/', CategoryIndex.as_view(), name='products_by_category'),
    path('add_to_cart/<int:product_pk>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('remove_from_cart/<int:item_pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]