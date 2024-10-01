from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def landing_page(request):
    return render(request, "index.html")


@login_required
def data_entry(request):
    return render(request, "DataEntry.html")


@login_required
def dash_board(request):
    return render(request, "DashBoard.html")


def password_verify_link(request):
    # Handle POST request (form submission)
    if request.method == "POST":
        # Retrieve username and password from the form
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Get the 'next' parameter, defaulting to '/' if not provided
        next_page = request.POST.get("next", "/")

        # Attempt to authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful and the user is a superuser
        if user is not None and user.is_superuser:
            # Log the user in
            login(request, user)
            # Redirect to the next page (or home if not specified)
            return redirect(next_page)
        else:
            # Authentication failed, render the login page with an error message
            return render(
                request,
                "password_verify_link.html",
                {"error_message": "Invalid username or password", "next": next_page},
            )
    else:
        # Handle GET request (initial page load)
        # Get the 'next' parameter from the URL, defaulting to '/' if not provided
        next_page = request.GET.get("next", "/")
        # Render the login page
        return render(request, "password_verify_link.html", {"next": next_page})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("landing_page")
    return redirect("landing_page")
