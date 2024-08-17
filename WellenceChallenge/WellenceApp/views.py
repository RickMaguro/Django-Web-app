from django.shortcuts import render
from .models import Accounts, Tasks
from django.http import JsonResponse
import datetime
import json

# Create your views here.
def landing_page(request):
    return render(request, 'index.html')

def data_entry(request):
    return render(request, 'DataEntry.html')

def dash_board(request):
    return render(request, 'DashBoard.html')

def password_verify_link(request):
    return render(request, 'password_verify_link.html')


from django.http import JsonResponse

def password_verify(request):
    password = request.POST.get('password')
    current_url = request.POST.get('form')

    # Check if password matches
    account = Accounts.objects.get(id=1)

    if account.check_password(password):
        # Redirect to the right page if verification was successful
        if current_url == 'data_entry':
            data = {'redirect': 'DataEntry'}
            print("Redirecting")
            response = JsonResponse(data)
            response.set_cookie('signed_in', 'True')
            return response
        

        elif current_url == 'dashboard':
            data = {'redirect': 'DashBoard'}
            print("Redirecting")
            response = JsonResponse(data);
            response.set_cookie('signed_in', 'True')
            return response
        else:
            data = {'error': 'Invalid form'}
            return JsonResponse(data, status=401)
    else:
        data = {'error': 'Invalid password'}
        return JsonResponse(data, status=401)


def data_entry_add(request):
    # Get the data from the request's body as a json object
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    task = data.get('task')
    due_by = data.get('due_by')
    priority = data.get('priority')
    is_urgent = data.get('is_urgent')
    is_urgent = True if is_urgent == 'on' else False
    print("------------------" + str(email), str(task), str(due_by), str(priority), str(is_urgent))
    # Get the latest id
    latest_id = Tasks.objects.latest('id').id
    # Increment the id by 1
    new_id = latest_id + 1
    
    # Save the new data entry with the new id
    data_entry = Tasks(id=new_id, email=email, task=task, due_by=due_by, priority=priority, is_urgent=is_urgent)
    data_entry.save()
    return JsonResponse({'success': True})



