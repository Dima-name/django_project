from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Главная страница (Дашборд)
    path('', views.dashboard, name='dashboard'),
    
    # Вход и выход (используем наш шаблон core/login.html)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Регистрация заказчика и создание заказа
    path('register/', views.register_customer, name='register'),
    path('create-order/', views.create_order, name='create_order'),
    
    # Действия с проектами
    path('take-order/<int:project_id>/', views.take_order, name='take_order'),
    path('change-status/<int:project_id>/<str:new_status>/', views.change_status, name='change_status'),
]