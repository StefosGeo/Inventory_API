from django.urls import path
from .views import ProductListView, OrderCreateListView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product'),
    path('orders/', OrderCreateListView.as_view(), name='order'),
]
