from django.urls import path
from market.views import IndexView, AddView, detailed_view, update_view, delete_view, CategoryView

urlpatterns = [
    path("", IndexView.as_view(), name='index'),
    path('product/add/', AddView.as_view(), name='product_add'),
    path('product/<int:pk>', detailed_view, name='product_detail'),
    path('product/<int:pk>/edit/', update_view, name='product_update'),
    path('product/<int:pk>/delete/', delete_view, name='product_delete'),
    path('products/<str:category_code>/', CategoryView.as_view(), name='products_by_category'),
]