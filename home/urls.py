from django.urls import path
from .views import *

urlpatterns = [
    path('', ProjectView.as_view(), name='project_list'),
    path('details/<str:id>/', ProjectDetailsView.as_view(), name='project_details'),
    path("task-data/", task_data, name="task-data"),
]