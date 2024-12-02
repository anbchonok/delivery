# Generated by Django 4.2.16 on 2024-11-27 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0002_alter_containers_container_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='employee_position',
            field=models.CharField(choices=[('менеджер', 'Менеджер'), ('курьер', 'Курьер'), ('оператор', 'Оператор')], max_length=50, verbose_name='Должность сотрудника'),
        ),
        migrations.AlterField(
            model_name='employees',
            name='employee_schedule',
            field=models.CharField(choices=[('Пн-Пт, 9:00-18:00', 'Пн-Пт, 9:00-18:00'), ('Пн-Вс', '9:00-22:00'), ('Пн-Вс', '8:00-20:00')], max_length=255, verbose_name='График работы'),
        ),
    ]
