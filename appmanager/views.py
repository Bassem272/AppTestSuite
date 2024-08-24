# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import App
from .forms import AppForm
from .utils import test_apk

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


            # Run Appium tests after saving the APK
            results = test_apk(app.apk_file.path)

            # Save test results to the model
            app.first_screen_screenshot = results['first_screenshot']
            app.second_screen_screenshot = results['second_screenshot']
            app.ui_hierarchy = results['ui_hierarchy']
            app.screen_changed = results['screen_changed']
            app.video_recording = results['video_path']
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

            # Run the Appium test if the APK file is updated
            if 'apk_file' in form.changed_data:
                
                # Run Appium tests after saving the APK
                results = test_apk(app.apk_file.path)

                # Save test results to the model
                app.first_screen_screenshot = results['first_screenshot']
                app.second_screen_screenshot = results['second_screenshot']
                app.ui_hierarchy = results['ui_hierarchy']
                app.screen_changed = results['screen_changed']
                app.video_recording = results['video_path']
                app.save()

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
