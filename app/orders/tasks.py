from celery import shared_task
from django.contrib.auth import get_user_model


@shared_task
def create_order():
    from .models import Order
    User = get_user_model()

    user = User.objects.order_by('?').first()
    Order.objects.create(
        name=f'Order for {user.email}', description=f'Description for {user.email}', employee=user)
