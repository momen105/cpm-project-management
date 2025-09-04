from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'predecessors': forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'Predecessors'})
        }
class ProjectForm(forms.ModelForm):
    class Meta:
        model = ProjectModel
        fields = '__all__'



class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {
            "username": None,  
        }