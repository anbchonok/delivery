from django.db import models
from django.core.validators import RegexValidator


class Clients(models.Model):
    fio = models.CharField(
        'ФИО клиента',
        max_length=100,
        null=False
    )
    address = models.CharField(
        'Адрес клиента',
        max_length=200,
        null=False
    )
    customer_phone = models.CharField(
        'Телефон клиента',
        max_length=20,
        primary_key=True,
        validators=[
            RegexValidator(
                regex='^\+?[0-9]*$',
                message='''
                Телефон должен содержать только цифры и может начинаться с +'''
            )
        ]
    )
    status = models.CharField(
        'Статус клиента',
        max_length=20,
        choices=[
            ('активный', 'Активный'),
            ('ушедший', 'Ушедший'),
        ],
        null=False
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.fio


class Containers(models.Model):
    container_id = models.AutoField(
        primary_key=True
    )
    container_volume = models.IntegerField(
        'Объем тары',
        null=False
    )
    container_type = models.CharField(
        'Тип тары',
        max_length=100,
        null=False
    )
    container_availability = models.BooleanField(
        'Доступность тары',
        default=True
    )

    class Meta:
        verbose_name = 'тара'
        verbose_name_plural = 'Тары'

    def __str__(self):
        return f"{self.container_type} (ID: {self.container_id})"


class Employees(models.Model):
    employee_id = models.AutoField(
        primary_key=True
    )
    employee_fio = models.CharField(
        'ФИО сотрудника',
        max_length=100,
        null=False
    )
    employee_position = models.CharField(
        'Должность сотрудника',
        max_length=50,
        null=False
    )
    employee_schedule = models.CharField(
        'График работы',
        max_length=255,
        null=False
    )

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.employee_fio


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_datetime = models.DateTimeField('Дата и время доставки')
    order_status = models.CharField(
        'Статус заказа',
        max_length=20,
        choices=[
            ('новый', 'Новый'),
            ('завершенный', 'Завершенный'),
            ('отмененный', 'Отмененный'),
        ],
        null=False
    )
    order_type = models.CharField(
        'Тип заказа',
        max_length=50,
        choices=[
            ('разовый', 'Разовый'),
            ('абонемент на 30 дней', 'Абонемент на 30 дней'),
            ('абонемент на полгода', 'Абонемент на полгода'),
            ('абонемент на год', 'Абонемент на год'),
        ],
        null=False
    )
    customer_phone = models.ForeignKey(
        Clients,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Телефон клиента'
    )
    employee_id = models.ForeignKey(
        Employees,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Сотрудник'
    )
    container_id = models.ForeignKey(
        Containers,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Тара'
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ от {self.delivery_datetime} для {self.customer_phone}"
