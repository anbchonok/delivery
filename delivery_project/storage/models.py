from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class Clients(models.Model):
    fio = models.CharField(
        'ФИО клиента',
        max_length=100,
        null=False,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё\s]+$',
                message='ФИО должно содержать только буквы и пробелы.'
            )
        ]
    )
    address = models.CharField(
        'Адрес клиента',
        max_length=200,
        null=False,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё\s]+$',
                message='Адрес должен содержать только буквы и пробелы.'
            )
        ]
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
        return self.customer_phone


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
        choices=[
            ('пластиковая бутылка', 'Пластиковая бутылка'),
            ('стеклянная бутылка', 'Стеклянная бутылка'),
            ('канистра', 'Канистра'),
            ('ёмкость для куллера', 'Ёмкость для куллера'),
        ],
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
    
    def clean(self):
        super().clean()
        # Устанавливаем ограничения по объему для каждого типа контейнера
        volume_limits = {
            'пластиковая бутылка': (500, 2000),  # Объем в миллилитрах
            'стеклянная бутылка': (250, 1500),
            'канистра': (1000, 20000),
            'ёмкость для куллера': (5000, 20000),
        }

        min_volume, max_volume = volume_limits.get(self.container_type, (0, float('inf')))
        
        if self.container_volume < min_volume or self.container_volume > max_volume:
            raise ValidationError(f"Объем для типа '{self.container_type}' должен быть в диапазоне от {min_volume} до {max_volume}.")


class Employees(models.Model):
    employee_id = models.AutoField(
        primary_key=True
    )
    employee_fio = models.CharField(
        'ФИО сотрудника',
        max_length=100,
        null=False,
        validators=[
            RegexValidator(
                regex='^[А-Яа-яЁё\s]+$',
                message='ФИО должно содержать только буквы и пробелы.'
            )
        ]
    )
    employee_position = models.CharField(
        'Должность сотрудника',
        max_length=50,
        choices=[
            ('менеджер', 'Менеджер'),
            ('курьер', 'Курьер'),
            ('оператор', 'Оператор'),
        ],
        null=False
    )
    employee_schedule = models.CharField(
        'График работы',
        max_length=255,
        choices=[
            ('Пн-Пт, 9:00-18:00', 'Пн-Пт, 9:00-18:00'),
            ('Пн-Вс, 9:00-22:00', 'Пн-Вс, 9:00-22:00'),
            ('Пн-Вс, 8:00-20:00', 'Пн-Вс, 8:00-20:00'),
        ],
        null=False
    )

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.employee_fio


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    delivery_datetime = models.DateTimeField('Дата и время доставки', default=timezone.now)
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
        models.SET_NULL,
        null=True,
        verbose_name='Телефон клиента'
    )
    employee_id = models.ForeignKey(
        Employees,
        models.SET_NULL,
        null=True,
        verbose_name='Сотрудник'
    )
    container_id = models.ForeignKey(
        Containers,
        models.SET_NULL,
        null=True,
        verbose_name='Тара'
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ от {self.delivery_datetime} для {self.customer_phone}"
        
    def clean(self):
        super().clean()  # Вызов метода родительского класса для выполнения стандартной валидации
        now = timezone.now()  # Получаем текущее время
        one_month_later = now + timedelta(days=30)  # Вычисляем дату через месяц
        # Проверка, что дата доставки не в прошлом
        if self.delivery_datetime < now:
            raise ValidationError('Дата и время доставки не могут быть в прошлом.')
        # Проверка, что дата доставки не более чем через месяц
        if self.delivery_datetime > one_month_later:
            raise ValidationError('Нельзя оформить заказ на месяц и больше вперед.')
