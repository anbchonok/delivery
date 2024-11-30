from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from django.urls import reverse_lazy

from storage.models import Employees, Orders


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
        my_employee = self.object
        my_orders = Orders.objects.select_related('customer_phone', 'employee_id').filter(employee_id=my_employee).order_by('-order_status')
        context['order'] = my_orders
        context['employee'] = my_employee  # Добавляем объект сотрудника в контекст
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
    #ordering = 'employee_id'
    #paginate_by = 10
