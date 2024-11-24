from django.shortcuts import render
from django.utils import timezone
from storage.models import Orders


def index(request):
    template_name = template_name = 'homepage/index.html'
    today = timezone.now().date()
    orders_today = Orders.objects.filter(delivery_datetime__date=today)

    context = {
        'orders_today': orders_today,
    }
    return render(request, template_name, context)
