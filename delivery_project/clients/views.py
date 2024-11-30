import psycopg2
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ClientsForm
from storage.models import Clients

def detail(request, pk=None):
    connection = psycopg2.connect(
        host="localhost",
        database="delivery",
        user="postgres",
        password="1"
    )
    cursor = connection.cursor()
    
    # Обновленный SQL-запрос, использующий представление storage_view
    cursor.execute('''
        SELECT
            container_volume, container_type,
            fio, customer_phone, 
            order_type, delivery_datetime, order_status,  
            employee_fio, employee_schedule
        FROM storage_view
        WHERE customer_phone = %s;
    ''', (pk,))  # Используем параметризацию для предотвращения SQL-инъекций

    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    
    # Обработка результатов
    client = [{column: value for column, value in zip(column_names, row)} for row in results][0]
    
    connection.close()

    context = {'client': client}
    template_name = 'clients/clients_detail.html'
    return render(request, template_name, context)

def client(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Clients, customer_phone=pk)
    else:
        instance = None
    form = ClientsForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        fio = form.cleaned_data['fio']
        address = form.cleaned_data['address']
        customer_phone = form.cleaned_data['customer_phone']
        status = form.cleaned_data['status']
        connection = psycopg2.connect(
            host="localhost",
            database="delivery",
            user="postgres",
            password="1"
        )
        cursor = connection.cursor()
        if pk is not None:
            cursor.execute(f'CALL update_clients( \'{fio}\', \'{address}\', \'{customer_phone}\', \'{status}\');')
        else:
            cursor.execute(f'CALL insert_clients( \'{fio}\', \'{address}\', \'{customer_phone}\', \'{status}\');')
        connection.commit()
        connection.close()
    return render(request, 'clients/clients_form.html', context)


def delete_client(request, pk):
    instance = get_object_or_404(Clients, customer_phone=pk)
    form = ClientsForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        connection = psycopg2.connect(
            host="localhost",
            database="delivery",
            user="postgres",
            password="1"
        )
        cursor = connection.cursor()
        cursor.execute(f'CALL delete_client(%s);', (pk,))
        connection.commit()
        connection.close()
        return redirect('clients:list')
    return render(request, 'clients/clients_form.html', context)

def list(request):
    connection = psycopg2.connect(
        host="localhost",
        database="delivery",
        user="postgres",
        password="1"
    )
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM select_clients();')
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    clients_list = [{column: value for column, value in zip(column_names, row)} for row in results]
    connection.close()
    context = {'clients_list': clients_list}
    return render(request, 'clients/clients_list.html', context)
