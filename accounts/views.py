# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.forms import AuthenticationForm

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('profile')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})


# accounts/views.py
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.views.decorators.http import require_POST
@require_POST
def logout_view(request):
    auth_logout(request)
    next_url = request.POST.get('next', 'login')  # Default to 'login' if no 'next' parameter is provided
    return redirect(next_url)
