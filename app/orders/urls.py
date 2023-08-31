from django.urls import path
from .views import OrderList, OrderDelete


app_name = 'orders'
urlpatterns = [
    path('', OrderList.as_view(), name='order-list'),
    path('<int:pk>/delete/', OrderDelete.as_view(), name='order-delete'),
]
