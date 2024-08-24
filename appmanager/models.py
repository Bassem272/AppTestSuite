# accounts/models.py
import os
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

def delete(self, *args, **kwargs):
    try:
        # Delete files associated with the app
        for field in [self.apk_file, self.first_screen_screenshot, self.second_screen_screenshot, self.video_recording]:
            if field and os.path.isfile(field.path):
                print(f"Deleting file: {field.path}")
                os.remove(field.path)
            else:
                print(f"File not found: {field.path}")
    except Exception as e:
        print(f"Error deleting file: {e}")
    finally:
        super().delete(*args, **kwargs)


    def __str__(self):
        return self.name
