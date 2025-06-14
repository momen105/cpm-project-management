from django import forms
from .models import *

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