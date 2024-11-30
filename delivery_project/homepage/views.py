from django.shortcuts import render
from django.utils import timezone
from storage.models import Orders
from django.shortcuts import render
import psycopg2

from storage.models import Orders


def get_client_count():
    connection = psycopg2.connect(
        host="localhost",
        database="delivery",
        user="postgres",
        password="1" 
    )
    cursor = connection.cursor()
    cursor.execute("SELECT active_clients();")
    result = cursor.fetchone()
    connection.close()
    if result:
        return result[0]
    else:
        return None


def index(request):
    client_count = get_client_count()  # Получаем количество клиентов
    template_name = 'homepage/index.html'  # Указываем имя шаблона
    today = timezone.now().date()  # Получаем текущую дату
    orders_today = Orders.objects.filter(delivery_datetime__date=today)  # Фильтруем заказы по дате

    # Объединяем данные в одном контексте
    context = {
        'orders_today': orders_today,
        'client_count': client_count,
    }
    
    return render(request, template_name, context)  # Возвращаем ответ с контекстом