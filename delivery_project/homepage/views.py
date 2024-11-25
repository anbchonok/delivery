from django.shortcuts import render
from django.utils import timezone
from storage.models import Orders
from datetime import datetime, timedelta
from django.db.models import Count, Sum
from django.shortcuts import render
import psycopg2

from storage.models import Orders, Clients


def get_client_count():
    connection = psycopg2.connect(
        host="localhost",
        database="delivery",
        user="postgres",
        password="1" #меняю на свой пароль на пгадмина
    )
    cursor = connection.cursor()
    cursor.execute("SELECT all_clients();")
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return None


def index(request):
    template_name = template_name = 'homepage/index.html'
    today = timezone.now().date()
    orders_today = Orders.objects.filter(delivery_datetime__date=today)

    context = {
        'orders_today': orders_today,
    }
    return render(request, template_name, context)
