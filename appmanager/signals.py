# appmanager/signals.py

from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import App
import os

@receiver(post_delete, sender=App)
def delete_related_files(sender, instance, **kwargs):
    try:
        # Delete files associated with the app
        for field in [instance.apk_file, instance.first_screen_screenshot, instance.second_screen_screenshot, instance.video_recording]:
            if field and os.path.isfile(field.path):
                print(f"Deleting file: {field.path}")
                os.remove(field.path)
            else:
                print(f"File not found: {field.path}")
    except Exception as e:
        print(f"Error deleting file: {e}")

