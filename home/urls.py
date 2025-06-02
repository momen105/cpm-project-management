from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskView.as_view(), name='task_list'),
    path("task-data/", task_data, name="task-data"),
    
]