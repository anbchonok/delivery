from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy
from storage.models import Orders


class OrdersMixin:
    model = Orders
    success_url = reverse_lazy('orders:list')


class OrdersCreateView(OrdersMixin, CreateView):
    # form_class = OrdersForm
    fields = '__all__'
    pass


class OrdersDetailView(DetailView):
    model = Orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_order = self.object
        context['employee'] = my_order.employee_id  
        context['client'] = my_order.customer_phone  
        context['containers'] = my_order.container_id  

        return context


class OrdersUpdateView(OrdersMixin, UpdateView):
    model = Orders
    fields = ['employee_id', 'customer_phone', 'container_id', 'delivery_datetime', 'order_status', 'order_type']
    template_name = 'storage/orders_form.html'



class OrdersDeleteView(OrdersMixin, DeleteView):
    template_name = 'storage/orders_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.get_object()  # Передаем объект в контекст
        return context


class OrdersListView(ListView):
    model = Orders
    ordering = 'id'
    #paginate_by = 10
    