from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import App
from .forms import AppForm

class AppListView(ListView):
    model = App
    template_name = 'appmanager/app_list.html'
    context_object_name = 'apps'

class AppCreateView(CreateView):
    model = App
    form_class = AppForm
    template_name = 'appmanager/app_form.html'
    success_url = reverse_lazy('app_list')

    def form_valid(self, form):
        form.instance.uploaded_by = self.request.user
        return super().form_valid(form)

class AppUpdateView(UpdateView):
    model = App
    form_class = AppForm
    template_name = 'appmanager/app_form.html'
    success_url = reverse_lazy('app_list')

class AppDeleteView(DeleteView):
    model = App
    template_name = 'appmanager/app_confirm_delete.html'
    success_url = reverse_lazy('app_list')
