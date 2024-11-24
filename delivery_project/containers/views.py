from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from storage.models import Containers, Employees, Orders, Clients


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
        my_orders = Orders.objects.filter(container_id=my_container).select_related('employee_id', 'customer_phone')
        context['orders'] = my_orders
        context['container'] = my_container  # Убедитесь, что объект передается в контекст
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
    paginate_by = 10