from django.shortcuts import render, redirect
from .forms import TaskForm, TaskUpdateForm, WebsiteBlockForm, WebsiteBlockUpdateForm
from .models import Task, WebsiteBlock
from django.urls import path, include
from django.views.generic.edit import UpdateView, DeleteView
from django.utils import timezone
from django.http import JsonResponse

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

def task_website_list(request, pk):
    if Task.objects.filter(id=pk).all().count() == 0:
        return redirect('/tasks/')
    current_task = Task.objects.filter(id=pk).first()
    if request.method == 'POST':
        website_block_form = WebsiteBlockForm(request.POST)
        if website_block_form.is_valid():
            new_website = WebsiteBlock(
                website_regex=website_block_form.cleaned_data.get('website_regex'),
                task_id=pk
            )
            new_website.save()
            return redirect(f'/tasks/{pk}/websites/')
    else:
        website_block_form = WebsiteBlockForm()
    website_list = WebsiteBlock.objects.filter(task_id=pk).order_by("id")
    context = {
        'website_block_form': website_block_form,
        'website_list': website_list,
        'current_task': current_task
    }
    return render(request, 'tasks/task_website_list.html', context)

def task_finished_list(request):
    user_tasks = Task.objects.filter(completed=True).order_by("-id")
    context = {
        'user_tasks': user_tasks
    }
    return render(request, 'tasks/task_finished_list.html', context)

def get_tasks_and_websites_json(request):
    tasks_and_websites = {}
    user_tasks = Task.objects.filter(completed=False).order_by("id")
    for task in user_tasks:
        tasks_and_websites[task.id] = {
            "info": task.info,
            "start_time": task.start_time.timestamp(),
            "end_time": task.end_time.timestamp(),
            "completed": task.completed,
            "whitelist": task.whitelist
        }
        website_list = WebsiteBlock.objects.filter(task_id=task.id).order_by("id")
        tasks_and_websites[task.id]["websites"] = []
        for website in website_list:
            tasks_and_websites[task.id]["websites"].append(website.website_regex)
    return JsonResponse(tasks_and_websites)

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return f"/tasks/"

class WebsiteBlockDeleteView(DeleteView):
    model = WebsiteBlock
    template_name_suffix = '_confirm_delete'
    def get_success_url(self):
        return f"/tasks/{self.get_object().task_id}/websites/"

class WebsiteBlockUpdateView(UpdateView):
    model = WebsiteBlock
    form_class = WebsiteBlockUpdateForm
    template_name_suffix = '_update_form'
    def get_success_url(self):
        return f"/tasks/{self.get_object().task_id}/websites/"