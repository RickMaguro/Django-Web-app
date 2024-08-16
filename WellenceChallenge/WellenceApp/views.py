from django.shortcuts import render
from .forms import PasswordForm
from .models import Accounts

# Create your views here.
def landing_page(request):
    return render(request, 'index.html')

def data_entry(request):
    return render(request, 'DataEntry.html')

def dash_board(request):
    return render(request, 'DashBoard.html')

def password_verification(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            account = Accounts.objects.get(id=1)  # Replace with your logic
            if account.check_password(password):
                # Password is correct
                return render(request, 'password_verification/success.html')
            else:
                # Password is incorrect
                return render(request, 'password_verification/fail.html')
        else:
            # Form is not valid
            return render(request, 'password_verification/form.html', {'form': form})
    else:
        # GET request
        form = PasswordForm()
        return render(request, 'password_verification/form.html', {'form': form})