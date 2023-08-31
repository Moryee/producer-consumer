# Producer - Consumer

## Description

Orders creating automatically every minute, employees can delete orders

![task_preview](https://github.com/Moryee/producer-consumer/assets/82435275/1b0e6e9d-d195-4479-996c-b34fd4001604)

## How to run
- Run project with docker compose `docker-compose up -d --build`
- You need to make manual migrations inside backend container 

`docker-compose exec backend python manage.py makemigrations --noinput`

`docker-compose exec backend python manage.py migrate --noinput`

- Program will be available on http://localhost:8000/

## Technical details

Program done with: Django, PostgreSQL, Celery, Docker

### Models

- Order model
```py
app/orders/models.py

class Order(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
```

- User model
```py
app/users/models.py

class CustomUser(AbstractUser, PermissionsMixin):
    ...

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=50)
    probation = models.IntegerField(default=0, help_text='Probation in days')

    class Position(models.TextChoices):
        MANAGER = 'manager', _('Manager')
        EMPLOYEE = 'employee', _('Employee')

    position = models.CharField(
        max_length=50,
        choices=Position.choices,
        default=Position.EMPLOYEE,
    )

    ...
```

### Orders

- Order views

```py
app/orders/views.py

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
```

- Orders creating every minute

```py
app/base/settings.py

CELERY_BEAT_SCHEDULE = {
    "create_order": {
        "task": "orders.tasks.create_order",
        "schedule": crontab(minute=1),
    },
}
```

```py
app/orders/tasks.py

@shared_task
def create_order():
    from .models import Order
    User = get_user_model()

    user = User.objects.order_by('?').first()
    Order.objects.create(
        name=f'Order for {user.email}', description=f'Description for {user.email}', employee=user)
```

- Messages appear on the order list page after deleting
