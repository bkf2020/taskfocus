from django.urls import path
from . import views
from .views import TaskUpdateView

urlpatterns = [
    path('', views.tasks_create_list, name='tasks-create-list'),
    path('finished/', views.task_finished_list, name='tasks-finished'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='tasks-update'),
]