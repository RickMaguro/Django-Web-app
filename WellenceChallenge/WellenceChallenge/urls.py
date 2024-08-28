from django.contrib import admin
from django.urls import path
from WellenceApp import views
from WellenceApp.views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing_page'),
    path('DataEntry', views.data_entry, name='data_entry'),
    path('DashBoard', views.dash_board, name='dash_board'),
    path('password_verify_link', views.password_verify_link, name='password_verify_link'),
    path('password_verify', views.password_verify, name='password_verify'),
    path('DataEntry_add', views.data_entry_add, name='data_entry_add'),


    path('tasks-due-report/', TasksDueReport.as_view(), name='tasks_due_report'),
    path('tasks_priority_due_pie_chart/',TasksPriorityDuePieChart.as_view(), name='tasks_priority_due_pie_chart'),
    path('tasks-urgent-report/', UrgentTasksDueReport.as_view(), name='tasks_urgent_report'),
    path('all_tasks_report/', AllTasksReportView.as_view(),name='all_tasks_report'),
]
