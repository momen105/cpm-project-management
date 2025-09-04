from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', logout_view, name="logout"),
    path('signup/', signup_view,name='signup'),  


    path('', ProjectView.as_view(), name='project_list'),
    path('projects/<str:id>/', ProjectView.as_view(), name='project_list_detail'),
    path('details/<str:id>/', ProjectDetailsView.as_view(), name='project_details'),
    path("task-data/", task_data, name="task-data"),
    path("network-diagram/<str:project_id>/", get_network_diagram, name="network_diagram"),
    path("schedule-diagram/<str:project_id>/", get_generate_Schedule_Diagram, name="Schedule_Diagram"),
    path("gantt-chart/<str:project_id>/", get_gantt_chart_data, name="gantt_chart"),
]