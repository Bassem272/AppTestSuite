# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from AppTestSuite import settings

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
    from django.utils import translation
    return render(request, 'profile.html')

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.contrib.auth.forms import AuthenticationForm
from django.utils import translation

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

from django.shortcuts import redirect
from django.utils import translation

# def switch_language(request, lang_code):
#     if lang_code in dict(settings.LANGUAGES):
#         translation.activate(lang_code)
#         request.session["django-language"] = lang_code
#         print("Switched to language:", lang_code)  # Debug line
#     return redirect(request.META.get('HTTP_REFERER', '/'))

from django.shortcuts import redirect
from django.utils import translation

from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings

# def switch_language(request, lang_code):
#     # Print current language
#     print("Before switch:", translation.get_language())
    
#     # Activate the selected language
#     if lang_code in dict(settings.LANGUAGES):
#         translation.activate(lang_code)
#         print("After switch:", translation.get_language())
        
#         if hasattr(request, 'session'):
#             request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
        
#         response = redirect(request.META.get('HTTP_REFERER', '/'))
#         response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
#         return response
#     else:
#         return redirect('account/login')

from django.shortcuts import redirect
from django.utils import translation
from django.conf import settings
import re

import re
from django.utils import translation
from django.shortcuts import redirect
from django.conf import settings

# def switch_language(request, lang_code):
#     # Activate the selected language
#     print(f"Before switch: {translation.get_language()}")  # Debug line
#     translation.activate(lang_code)
#     print(f"After switch: {translation.get_language()}")  # Debug line

#     # Store the language in the session
#     if hasattr(request, 'session'):
#         request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
#         print(f"session_language_cookie_name {request.session[settings.LANGUAGE_COOKIE_NAME]}")  # Debug line

#     # Get the current URL and replace the language code
#     current_url = request.META.get('HTTP_REFERER', '/')
#     print(f"Current URL: {current_url}")  # Debug line
#     # Replace the language code in the URL
#     new_url = re.sub(r'^/(\w{2})/', f'/{lang_code}/', current_url)
#     print(f"New URL: {new_url}")  # Debug line

#     # Optionally, set a language cookie
#     response = redirect(new_url)
#     response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)

#     return response
import re
from django.utils import translation
from django.shortcuts import redirect
from django.conf import settings

def switch_language(request, lang_code):
    print(f'Before switch: {translation.get_language()}')
    
    # Activate the selected language
    translation.activate(lang_code)
    request.session[settings.LANGUAGE_COOKIE_NAME] = lang_code
    
    print(f'After switch: {translation.get_language()}')
    print(f'session_language_cookie_name {request.session.get(settings.LANGUAGE_COOKIE_NAME)}')

    # Get the referer URL and replace the language code
    current_url = request.META.get('HTTP_REFERER', '/')
    if not current_url:
        current_url = '/'
    
    # Replace the language code in the URL
    new_url = re.sub(r'^/(\w{2})/', f'/{lang_code}/', current_url)
    
    print(f'Current URL: {current_url}')
    print(f'New URL: {new_url}')

    # Redirect to the new URL with the updated language
    response = redirect(new_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code)
    
    return response

