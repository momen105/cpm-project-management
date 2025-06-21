from django.views import View
from django.shortcuts import render, redirect,get_object_or_404
from .models import Task
from .forms import *
from django.http import JsonResponse
from home.diagram import *
class ProjectDetailsView(View):
    def get(self, request, id):
        project = get_object_or_404(ProjectModel, pk=id)
        form = TaskForm(instance=project)
        tasks = Task.objects.filter(project=project)
        activities = generate_Schedule_Diagram(id)
        return render(request, 'home/list.html', {'form': form, 'project': project,'tasks':tasks,'activities':activities[0]})

    def  post(self, request, *args, **kwargs):
        project_id = kwargs.get('id')
        data = request.POST.copy()
        data['project'] = project_id
        if data.get("predecessors") == "":
            data.pop("predecessors")
            
        form = TaskForm(data)
        if form.is_valid():
            form.save()
            return redirect('project_details', id=project_id)
        else:
            print(form.errors)
        return redirect('project_details', id=project_id)
    

class ProjectView(View):
    def get(self, request):
        form = ProjectForm()
        data = ProjectModel.objects.all()
        return render(request, 'home/project.html', {'form': form,'data':data})

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
        return redirect('project_list')
    

def task_data(request):
    return JsonResponse({
        "name": "Sample Task",
        "description": "Example description",
        "duration": "5 days"
    })



def get_network_diagram(request, project_id):

    diagram, node_data = generate_network_diagram(project_id)

    return JsonResponse({
        "diagram": diagram,
        "nodes": node_data
    })

def get_generate_Schedule_Diagram(request, project_id):

    activities,connections,critical_path_duration, critical_tasks,node_data = generate_Schedule_Diagram(project_id)
 
    return JsonResponse({
        "activities": activities,
        "connections": connections,
        "critical_path_duration":critical_path_duration,
        "critical_tasks":critical_tasks,
        "node_data":node_data
    })

def get_gantt_chart_data(request, project_id):

    labels,data = gantt_chart_data(project_id)

    return JsonResponse({
        "labels": labels,
        "data": data
    })
