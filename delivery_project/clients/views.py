import psycopg2
from django.shortcuts import get_object_or_404, render, redirect
from .forms import ClientsForm
from storage.models import Clients
from .db_connection import DatabaseConnection


def detail(request, pk=None):
    db = DatabaseConnection()
    results = db.execute1('''
        SELECT
            container_volume, container_type,
            fio, customer_phone, 
            order_type, delivery_datetime, order_status,  
            employee_fio, employee_schedule
        FROM storage_view
        WHERE customer_phone = %s;
    ''', (pk,))
    column_names = [description[0] for description in db.cursor.description]
    client = [{column: value for column, value in zip(column_names, row)} for row in results][0]
    db.close()
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
        
        db = DatabaseConnection()
        if pk is not None:
            db.execute1(f'CALL update_clients( \'{fio}\', \'{address}\', \'{customer_phone}\', \'{status}\');')
        else:
            db.execute1(f'CALL insert_clients( \'{fio}\', \'{address}\', \'{customer_phone}\', \'{status}\');')
        db.commit()
        db.close()
    return render(request, 'clients/clients_form.html', context)

def delete_client(request, pk):
    instance = get_object_or_404(Clients, customer_phone=pk)
    form = ClientsForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        db = DatabaseConnection()
        db.execute1(f'CALL delete_client(%s);', (pk,))
        db.commit()
        db.close()
        return redirect('clients:list')
    return render(request, 'clients/clients_form.html', context)


def delete_client(request, pk):
    instance = get_object_or_404(Clients, customer_phone=pk)
    form = ClientsForm(instance=instance)
    context = {'form': form}
    if request.method == 'POST':
        db = DatabaseConnection()
        db.execute1(f'CALL delete_client(%s);', (pk,))
        db.commit()
        db.close()
        return redirect('clients:list')
    return render(request, 'clients/clients_form.html', context)

def list(request):
    db = DatabaseConnection()
    results = db.execute1('SELECT * FROM select_clients();')
    column_names = [description[0] for description in db.cursor.description]
    clients_list = [{column: value for column, value in zip(column_names, row)} for row in results]
    db.close()
    context = {'clients_list': clients_list}
    return render(request, 'clients/clients_list.html', context)
