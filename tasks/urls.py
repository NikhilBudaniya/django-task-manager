from django.urls import path

from . import views

urlpatterns = [
    # Task URLs
    path('tasks/get/all/', views.TaskListView.as_view(), name='all_tasks'),
    path('tasks/get/<int:task_id>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/assign/', views.TaskAssignView.as_view(), name='assign_task'),
    path('tasks/users/<int:task_id>/', views.TaskUsersView.as_view(), name='task_users'),
    path('tasks/filter/', views.TaskFilterView.as_view(), name='filter_tasks'),
    path('tasks/stats/', views.TaskStatsView.as_view(), name='task_stats'),
    path('tasks/create/', views.TaskCreateView.as_view(), name='create_task'),
    path('tasks/update/<int:task_id>/', views.TaskUpdateView.as_view(), name='update_task'),
    path('tasks/delete/<int:task_id>/', views.TaskDeleteView.as_view(), name='delete_task'),
    # User URLs
    path('users/get/all/', views.UserListView.as_view(), name='all_users'),
    path('users/get/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/tasks/<int:user_id>/', views.UserTasksView.as_view(), name='user_tasks'),
    path('users/create/', views.UserCreateView.as_view(), name='create_user'),
    path('users/update/<int:user_id>/', views.UserUpdateView.as_view(), name='update_user'),
    path('users/delete/<int:user_id>/', views.UserDeleteView.as_view(), name='delete_user')
]
