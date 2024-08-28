from django.shortcuts import render
from WellenceApp.models import *
from django.http import JsonResponse
import json

from django.db.models import *
from django.utils import timezone
from slick_reporting.views import *
from slick_reporting.fields import *

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

@login_required
def protected_page(request):
    return render(request, 'protected_page.html')


# Create your views here.
def landing_page(request):
    return render(request, 'index.html')

def data_entry(request):
    return render(request, 'DataEntry.html')

def dash_board(request):
    # try:
    #     # TasksDueReport_r = TasksDueReport.as_view()(request)
    #     # TasksPriorityDuePieChart_r = TasksPriorityDuePieChart.as_view()(request)
    #     # UrgentTasksDueReport_r = UrgentTasksDueReport.as_view()(request)
    #     # AllTasksReportView_r = AllTasksReportView.as_view()(request)

    #     context = {
    #         'TasksDueReport_r': TasksDueReport_r,
    #         'TasksPriorityDuePieChart_r': TasksPriorityDuePieChart_r,
    #         'UrgentTasksDueReport_r': UrgentTasksDueReport_r,
    #         'AllTasksReportView_r': AllTasksReportView_r
    #     }
        # return render(request, 'DashBoard.html', context)
        return render(request, 'DashBoard.html')



def password_verify_link(request):
    return render(request, 'password_verify_link.html')




def password_verify(request):
    
    print(f"password_verify: {request.POST}")
    password = request.POST.get('password')
    current_url = request.POST.get('form')

    user = authenticate(request, password=password)
    print(f"authenticate returned: {user}")
    if user is not None:
        login(request, user)
        print("logged in")
        if current_url == 'data_entry':
            data = {'redirect': 'DataEntry'}
            print("Redirecting to data entry")
            response = JsonResponse(data)
            return response
        
        elif current_url == 'dashboard':
            data = {'redirect': 'DashBoard'}
            print("Redirecting to dashboard")
            response = JsonResponse(data);
            return response
        else:
            print("invalid form")
            data = {'error': 'Invalid form'}
            return JsonResponse(data, status=401)
    else:
        print("invalid password")
        data = {'error': 'Invalid password'}
        return JsonResponse(data, status=401)

@login_required
def data_entry_add(request):
    # Retrieve the data from the request's body as a json object
    data = json.loads(request.body.decode('utf-8'))
    
    # Extract the required fields from the json object
    email = data.get('email')
    task = data.get('task')
    due_by = data.get('due_by')
    priority = data.get('priority')
    is_urgent = data.get('is_urgent')
    
    # Convert the 'is_urgent' string to a boolean
    is_urgent = True if is_urgent == 'on' else False
    
    # Print the extracted data for debugging purposes
    print("------------------" + str(email), str(task), str(due_by), str(priority), str(is_urgent))
    
    # Retrieve the latest id in the Tasks table
    latest_id = Tasks.objects.latest('id').id
    
    # Increment the latest id by 1 to get the new id
    new_id = latest_id + 1
    
    # Create a new Tasks object with the new id and the extracted data
    data_entry = Tasks(
        id=new_id,
        email=email,
        task=task,
        due_by=due_by,
        priority=priority,
        is_urgent=is_urgent
    )
    
    try:
        # Save the new Tasks object to the database
        data_entry.save()
        
        # Return a JsonResponse with a success message
        return JsonResponse({'success': True})
    except Exception as e:
        # If there is an error while saving the data, return an error message
        return JsonResponse({'error': str(e)}, status=500)



class TasksDueReport(ListReportView):
    report_model = Tasks
    columns = [
        'due_by',
        'id',
        'task',
    ]
    chart_settings = [
        Chart(
            'Tasks Due in Next 30 Days',
            Chart.BAR,
            data_source=['id'],
            title_source=['due_by'],
        )
    ]

    def get_queryset(self):
        today = timezone.now()
        next_30_days = today + timezone.timedelta(days=30)
        return super().get_queryset().filter(due_by__range=(today, next_30_days))



class TasksPriorityDuePieChart(ListReportView):
    report_model = Tasks
    columns = [
        'priority',
        'id',
        'task',
    ]
    chart_settings = [
        Chart(
            'Tasks by Priority',
            Chart.PIE,
            data_source=['id'],
            title_source=['priority'],
        )
    ]

    def get_queryset(self):
        today = timezone.now()
        next_30_days = today + timezone.timedelta(days=30)
        return super().get_queryset().filter(due_by__range=(today, next_30_days))
    
    


    
class UrgentTasksDueReport(ListReportView):
    report_model = Tasks
    report_title = "Total Urgent Tasks"
    columns = [
        'due_by',
        'id',
        'task',
        'is_urgent',
    ]

    def get_queryset(self):
        today = timezone.now()
        next_30_days = today + timezone.timedelta(days=30)
        return super().get_queryset().filter(due_by__range=(today, next_30_days), is_urgent=True)




class AllTasksReportView(ListReportView):
    report_model = Tasks
    columns = [
        'id',
        'email',
        'task',
        'due_by',
        'priority',
        'is_urgent',
    ]




