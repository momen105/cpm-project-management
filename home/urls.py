from django.urls import path
from .views import *

urlpatterns = [
    path('', ProjectView.as_view(), name='project_list'),
    path('details/<str:id>/', ProjectDetailsView.as_view(), name='project_details'),
    path("task-data/", task_data, name="task-data"),
    path("network-diagram/<str:project_id>/", get_network_diagram, name="network_diagram"),
    path("schedule-diagram/<str:project_id>/", get_generate_Schedule_Diagram, name="Schedule_Diagram"),
    path("gantt-chart/<str:project_id>/", get_gantt_chart_data, name="gantt_chart"),
]