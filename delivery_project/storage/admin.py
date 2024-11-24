from django.contrib import admin
from .models import Employees, Containers, Clients, Orders


admin.site.register(Employees)
admin.site.register(Containers)
admin.site.register(Clients)
admin.site.register(Orders)
