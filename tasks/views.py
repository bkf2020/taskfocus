from django.shortcuts import render, redirect
from .forms import TaskForm, TaskUpdateForm
from .models import Task
from django.urls import path, include
from django.views.generic.edit import UpdateView
from django.utils import timezone

def tasks_create_list(request):
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            new_task = Task(
                info=task_form.cleaned_data.get('info'),
                start_time=task_form.cleaned_data.get('start_time'),
                end_time=task_form.cleaned_data.get('end_time')
            )
            new_task.save()
            return redirect(f'/tasks/')
    else:
        task_form = TaskForm()
    
    user_tasks = Task.objects.filter(completed=False).order_by("id")
    context = {
        'task_form': task_form,
        'user_tasks': user_tasks,
        'current_server_time': timezone.now()
    }
    return render(request, 'tasks/tasks_create_list.html', context)

def task_finished_list(request):
    user_tasks = Task.objects.filter(completed=True).order_by("-id")
    context = {
        'user_tasks': user_tasks
    }
    return render(request, 'tasks/task_finished_list.html', context)

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return f"/tasks/"