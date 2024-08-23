# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class App(models.Model):
    name = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    apk_file = models.FileField(upload_to='apk_files/')
    first_screen_screenshot = models.ImageField(upload_to='screenshots/', null=True, blank=True)
    second_screen_screenshot = models.ImageField(upload_to='screenshots/', null=True, blank=True)
    video_recording = models.FileField(upload_to='videos/', null=True, blank=True)
    ui_hierarchy = models.TextField(null=True, blank=True)
    screen_changed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
