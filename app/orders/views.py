from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order
from users.models import CustomUser
from django.contrib import messages
from datetime import datetime


class OrderList(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(employee=self.request.user)


class OrderDelete(DeleteView):
    model = Order
    template_name = 'orders/order_confirm_delete.html'
    success_url = reverse_lazy('orders:order-list')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        order: Order = self.get_object()
        employee: CustomUser = order.employee
        response = super().post(request, *args, **kwargs)

        if response.status_code < 400:
            message = f'Task #{order.pk} {order.name} was processed by {employee.username}({employee.position}) at {datetime.now()}'
            messages.success(request, message, extra_tags='alert alert-success')

        return response
