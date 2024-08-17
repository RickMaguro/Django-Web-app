from django.shortcuts import render, redirect
from .models import Accounts
from django.http import HttpResponseRedirect
from django.http import HttpResponse


# Create your views here.
def landing_page(request):
    return render(request, 'index.html')

def data_entry(request):
    return render(request, 'DataEntry.html')

def dash_board(request):
    return render(request, 'DashBoard.html')

def password_verify_link(request):
    return render(request, 'password_verify_link.html')


def password_verify(request):
    password = request.POST.get('password')
    # Check if password matches
    account = Accounts.objects.get(id=1)  # Replace with your logic

    if account.check_password(password):
        # Redirect to the right page if verification was successful
        current_url = request.META['HTTP_REFERER']
        if 'form=data_entry' in current_url:
            print("Redirecting")
            return HttpResponseRedirect('DataEntry')        
        elif 'form=dashboard' in current_url:
            print("Redirecting")
            return HttpResponseRedirect('DashBoard')
        else:
            return HttpResponse('Invalid form', status = 401)
    else:
        return HttpResponse('Invalid password', status = 401)
    

