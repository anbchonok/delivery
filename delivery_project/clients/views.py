import psycopg2
from django.shortcuts import get_object_or_404, render, redirect

from .forms import ClientsForm
from storage.models import Clients


def detail(request, pk=None):
    connection = psycopg2.connect(
        host="localhost",
        database="delivery",
        user="postgres",
        password="1" #меняю на свой пароль на пгадмина
    )
    cursor = connection.cursor()
    cursor.execute(f'SELECT c."fio", c."address", c."customer_phone", c."status" FROM storage_clients c WHERE c.customer_phone = \'{pk}\';')
    results = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    client = [{column: value for column, value in zip(column_names, row)} for row in results][0]
    connection.close()

    context = {'client': client}
    template_name = 'clients/clients_detail.html'
    return render(request, template_name, context)


def client(request, pk=None):
    if pk is not None:
        instance = get_object_or_404(Clients, pk=pk)
    else:
        instance = None
    form = ClientsForm(request.POST or None, instance=instance)
    context = {'form': form}
    if form.is_valid():
        fio = form.cleaned_data['fio']
        address = form.cleaned_data['address']
        customer_phone = form.cleaned_data['customer_phone']
        status = form.cleaned_data['status']
        # form.save()  # Здесь должен быть вызов функции из БД
        connection = psycopg2.connect(
            host="localhost",
            database="delivery",
            user="postgres",
            password="1"
        )
        cursor = connection.cursor()
        cursor.execute(f'CALL update_clients( \'{fio}\', \'{address}\', \'{customer_phone}\', \'{status}\');')
        connection.commit()
        connection.close()
    return render(request, 'clients/clients_form.html', context)


def delete_client(request, pk):
    instance = get_object_or_404(Clients, pk=pk)
    form = ClientsForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        instance.delete()  # Здесь должен быть вызов функции из БД
        return redirect('clients:list')
    return render(request, 'clients/clients_form.html', context)


def list(request):
    clients_list = Clients.objects.order_by('fio')  # Здесь должен быть вызов функции из БД
    context = {'clients_list': clients_list}
    return render(request, 'clients/clients_list.html', context)


def client_RewSQL(request):
    template_name = 'homepage/index.html'
    connection = psycopg2.connect(
        host="localhost",
        database="delivery",
        user="postgres",
        password="1"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT all_clients();")
    result = cursor.fetchone()
    connection.close()
    if result:
        return render(request, template_name, result[0])
    else:
        return render(request, template_name)
