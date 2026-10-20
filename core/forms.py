from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Client, Project

class CustomerSignUpForm(UserCreationForm):
    company_name = forms.CharField(max_length=200, label="Название вашей компании")
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'company_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Client.objects.create(
                user=user,
                name=self.cleaned_data['company_name'],
                contact_person=user.username,
                email=self.cleaned_data['email'],
                phone="Не указан"
            )
        return user

class OrderForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'description') # <-- Оставили только название и описание
        labels = {
            'title': 'Тема проекта (Кратко)',
            'description': 'Опишите, какой сайт вам нужен',
        }