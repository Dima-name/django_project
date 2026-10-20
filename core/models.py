from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Аккаунт заказчика")
    name = models.CharField(max_length=200, verbose_name="Название компании")
    contact_person = models.CharField(max_length=100, verbose_name="Контактное лицо")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

class Project(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новый (Ожидает исполнителя)'),
        ('in_progress', 'В разработке'),
        ('review', 'На проверке у заказчика'),
        ('done', 'Сдан'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Название проекта")
    description = models.TextField(verbose_name="Описание задачи", default="")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Заказчик")
    
    # Разработчик и цена появляются, когда он берет заказ
    developer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Разработчик")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Цена")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"