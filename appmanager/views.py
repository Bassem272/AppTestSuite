# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import App
from .forms import AppForm

@login_required
def app_list(request):
    apps = App.objects.filter(uploaded_by=request.user)
    return render(request, 'app_list.html', {'apps': apps})

@login_required
def app_create(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.uploaded_by = request.user
            app.save()
            return redirect('app_list')
    else:
        form = AppForm()
    return render(request, 'app_form.html', {'form': form})

@login_required
def app_update(request, pk):
    app = get_object_or_404(App, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('app_list')
    else:
        form = AppForm(instance=app)
    return render(request, 'app_form.html', {'form': form})

@login_required
def app_delete(request, pk):
    app = get_object_or_404(App, pk=pk, uploaded_by=request.user)
    if request.method == 'POST':
        app.delete()
        return redirect('app_list')
    return render(request, 'app_confirm_delete.html', {'app': app})
