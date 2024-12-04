from django.shortcuts import render
from django.utils import timezone
from storage.models import Orders
from django.shortcuts import render
from clients.db_connection import DatabaseConnection
from storage.models import Orders


def get_client_count():
    # Создаем экземпляр класса DatabaseConnection
    db_connection = DatabaseConnection()
    
    try:
        # Выполняем запрос к базе данных
        result = db_connection.execute("SELECT active_clients();")
        
        # Проверяем, есть ли результат и возвращаем его
        if result:
            return result[0][0]  # Возвращаем значение первого столбца первой строки
        else:
            return None
    finally:
        # Закрываем соединение с базой данных
        db_connection.close()


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