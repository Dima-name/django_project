from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Client, Project
from .forms import CustomerSignUpForm, OrderForm
from django import forms

@login_required
def dashboard(request):
    user = request.user
    
    # 1. АДМИН
    if user.is_superuser:
        projects = Project.objects.all().order_by('-created_at')
        context = {'role': 'admin', 'projects': projects}
        
    # 2. ЗАКАЗЧИК
    elif Client.objects.filter(user=user).exists():
        client = Client.objects.get(user=user)
        projects = Project.objects.filter(client=client).order_by('-created_at')
        context = {'role': 'client', 'projects': projects}
        
    # 3. РАЗРАБОТЧИК
    else:
        # Свободные заказы (у которых нет разработчика)
        available_orders = Project.objects.filter(developer__isnull=True).order_by('-created_at')
        # Заказы, которые он взял
        my_projects = Project.objects.filter(developer=user).order_by('-created_at')
        context = {
            'role': 'developer', 
            'available_orders': available_orders,
            'projects': my_projects
        }
        
    return render(request, 'core/dashboard.html', context)

# --- Вспомогательная форма для ввода цены разработчиком ---
class PriceForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['price']
        labels = {'price': 'Назначьте стоимость (руб)'}

@login_required
def take_order(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    # Если заказ еще свободен, показываем форму для ввода цены
    if project.developer is None:
        if request.method == 'POST':
            form = PriceForm(request.POST, instance=project)
            if form.is_valid():
                order = form.save(commit=False)
                order.developer = request.user # Назначаем текущего разработчика
                order.status = 'in_progress'   # Меняем статус
                order.save()
                return redirect('dashboard')
        else:
            form = PriceForm(instance=project)
            
        return render(request, 'core/take_order.html', {'form': form, 'project': project})
        
    return redirect('dashboard')

@login_required
def change_status(request, project_id, new_status):
    project = get_object_or_404(Project, id=project_id)
    # Разработчик может менять статус только своих проектов
    if project.developer == request.user:
        project.status = new_status
        project.save()
    return redirect('dashboard')

def register_customer(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = CustomerSignUpForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def create_order(request):
    if not Client.objects.filter(user=request.user).exists():
        return redirect('dashboard')
        
    client = Client.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = client
            order.status = 'new'
            order.save()
            return redirect('dashboard')
    else:
        form = OrderForm()
    
    return render(request, 'core/create_order.html', {'form': form})