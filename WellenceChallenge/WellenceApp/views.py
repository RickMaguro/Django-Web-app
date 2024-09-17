from django.shortcuts import render
from WellenceApp.models import *
from WellenceApp.models import Accounts
from django.http import JsonResponse
import json

from django.db.models import *
from django.utils import timezone
from slick_reporting.views import *
from slick_reporting.fields import *

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from WellenceApp.services import TaskService

# Create your views here.
def landing_page(request):
    return render(request, 'index.html')

@login_required
def data_entry(request):
    return render(request, 'DataEntry.html')

@login_required
def dash_board(request):
    return render(request, 'DashBoard.html')



def password_verify_link(request):
    """
    This view is called when the user is redirected to the password verification
    page. It checks if the user has entered the correct password, and if so, it
    logs them in and redirects them to the home page.
    """
    if request.method == 'POST':
        # Get the password from the request
        password = request.POST.get('password')
        # Get the current URL from the request
        current_url = request.POST.get('form')
        # Print the password and current URL for debugging purposes
        print(f"password: {password} form: {current_url}")
        # Authenticate the user with the password
        user = authenticate(request, password=password)
        # Print the result of the authentication for debugging purposes
        print(f"authenticate returned: {user}")
        if user is not None:
            # If the user is not None, log them in
            login(request, user)
            print("logged in")
            # Create a JsonResponse with a redirect to the home page
            data = {'redirect': '/'}
            print("Redirecting to home")
            response = JsonResponse(data)
            return response
        else:
            # If the user is None, return a JsonResponse with an error message
            print("invalid password")
            data = {'message': 'Invalid password'}
            return JsonResponse(data, status=401)
    else:
        # If the request is not a POST request, render the password verification page
        return render(request, 'password_verify_link.html')


class PasswordOnlyBackend:
    """
    This is a custom Django authentication backend that does not use a username,
    but rather a single password that is stored in the database. If the password
    is correct, it will log in as the user 'NOT_admin'. If the user does not exist,
    it will create it.
    """
    def authenticate(self, request, password=None):
        """
        Authenticates a user based on the password provided. If the password
        is correct, it will log in as the user 'NOT_admin'. If the user does not
        exist, it will create it.
        """
        RealPassword = Accounts.objects.get(id=1)
        print(RealPassword)
        if RealPassword.check_password(password):
            try:
                user= User.objects.get(username='NOT_admin')
                return user
            except User.DoesNotExist:
                user = User.objects.create_user(username='NOT_admin', password=password)
                user.save()
                return user
        
    def get_user(self, user_id):
        """
        Returns a user object based on the user_id provided. If the user does not
        exist, it will return None.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        



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




