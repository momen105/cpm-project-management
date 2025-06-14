from django.db import models
from cpm.models import *

class ProjectModel(BaseModel):
    name = models.CharField(max_length=500)
    
class Task(BaseModel):
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    duration = models.PositiveIntegerField()
    start_date = models.DateField()
    finish_date = models.DateField()
    predecessors = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='dependent_tasks')

    def __str__(self):
        return self.name