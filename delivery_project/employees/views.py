from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from storage.models import Employees


class EmployeesMixin:
    model = Employees
    success_url = reverse_lazy('employees:list')


class EmployeesCreateView(EmployeesMixin, CreateView):
    # form_class = TariffsForm
    fields = '__all__'
    pass


class EmployeesDetailView(DetailView):
    model = Employees
    template_name = 'storage/employees_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employee'] = self.object
        return context


class EmployeesUpdateView(EmployeesMixin, UpdateView):
    # form_class = TariffsForm
    
    fields = '__all__'
    pass


class EmployeesDeleteView(EmployeesMixin, DeleteView):
    template_name = 'storage/employees_confirm_delete.html'  # Создайте отдельный шаблон для подтверждения удаления
    success_url = reverse_lazy('employees:list')  # Перенаправление после удаления



class EmployeesListView(ListView):
    model = Employees
    ordering = 'employee_id'
    paginate_by = 10
