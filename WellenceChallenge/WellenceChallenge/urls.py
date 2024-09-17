from django.contrib import admin
from django.urls import path, include
from WellenceApp import views
from WellenceApp.api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs for page rendering
    path('', views.landing_page, name='landing_page'),
    path('DataEntry', views.data_entry, name='data_entry'),
    path('DashBoard', views.dash_board, name='dash_board'),
    path('password_verify_link', views.password_verify_link, name='password_verify_link'),
    
    # New API URL
    path('api/', api.urls),
    
    # Report URLs (can be kept or moved to the API)
    path('tasks-due-report/', views.TasksDueReport.as_view(), name='tasks_due_report'),
    path('tasks_priority_due_pie_chart/', views.TasksPriorityDuePieChart.as_view(), name='tasks_priority_due_pie_chart'),
    path('tasks-urgent-report/', views.UrgentTasksDueReport.as_view(), name='tasks_urgent_report'),
    path('all_tasks_report/', views.AllTasksReportView.as_view(), name='all_tasks_report'),
]
