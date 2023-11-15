from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter
from .views import (GroupsListView,
                    ShopIndexView, ProductDetailsView, groups_list,
                    products_list,
                    ProductsListView,
                    OrdersListView,
                    OrderDetailView,
                    ProductCreateView,
                    ProductDeleteView,
                    ProductUpdateView,
                    ProductsDataExportView,
                    ProductViewSet,
                    )

app_name = 'shopapp'
routers = DefaultRouter()
routers.register('products', ProductViewSet)

urlpatterns = [
    # path('', cache_page(60*3)(ShopIndexView.as_view()), name='index'),
    path('', ShopIndexView.as_view(), name='index'),
    path('api/', include(routers.urls)),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductsListView.as_view(), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_form'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/confirm-delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('orders/', OrdersListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('products/export/', ProductsDataExportView.as_view(), name='products-export'),
]
