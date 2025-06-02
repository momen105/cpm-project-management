from django.views import View
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse

class TaskView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'home/list.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        return redirect('task_list')
    


def task_data(request):
    return JsonResponse({
        "name": "Sample Task",
        "description": "Example description",
        "duration": "5 days"
    })