from django.urls import path
from . import views
from .views import TaskUpdateView, WebsiteBlockUpdateView, WebsiteBlockDeleteView

urlpatterns = [
    path('', views.tasks_create_list, name='tasks-create-list'),
    path('finished/', views.task_finished_list, name='tasks-finished'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='tasks-update'),
    path('<int:pk>/websites/', views.task_website_list, name='tasks-website-list'),
    path('website/<int:pk>/delete/', WebsiteBlockDeleteView.as_view(), name='website-block-delete'),
    path('website/<int:pk>/update/', WebsiteBlockUpdateView.as_view(), name='website-block-update'),
]