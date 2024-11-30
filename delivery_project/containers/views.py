from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from storage.models import Containers, Orders
from datetime import datetime, timedelta

class ContainersMixin:
    model = Containers
    success_url = reverse_lazy('containers:list')


class ContainersCreateView(ContainersMixin, CreateView):
    # form_class = CellsForm
    fields = '__all__'
    pass


class ContainersDetailView(DetailView):
    model = Containers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_container = self.object
        my_orders = Orders.objects.select_related('employee').select_related('client').filter(container_id=my_container).order_by('-order_status')
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)
        try:
            context['active_orders_count'] = my_orders.values('order_status').filter(order_status__gt=today).count()
        except IndexError:
            context['active_orders_count'] = 0
      
        try:
            context['created_orders_all'] = my_orders.count()
        except IndexError:
            context['created_orders_all'] = 0
        return context


class ContainersUpdateView(ContainersMixin, UpdateView):
    # form_class = CellsForm
    fields = '__all__'
    pass


class ContainersDeleteView(ContainersMixin, DeleteView):
    template_name = 'storage/containers_form.html'
    pass


class ContainersListView(ListView):
    model = Containers
    ordering = 'container_id'
    #paginate_by = 10