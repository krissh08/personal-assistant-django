# scheduler/tasks.py

from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Event
from gtts import gTTS
import os
from django.core.mail import EmailMessage # Import the EmailMessage class

@shared_task
def process_reminders():
    now = timezone.now()
    reminder_window_end = now + timedelta(minutes=5)

    upcoming_events = Event.objects.filter(
        event_time__gte=now,
        event_time__lte=reminder_window_end
    )
    
    if not upcoming_events.exists():
        print("No upcoming events found.")
        return "No upcoming events."

    print(f"Found {upcoming_events.count()} events to remind for.")
    
    for event in upcoming_events:
        reminder_message = f"Reminder for {event.user.username}: You have '{event.title}' scheduled now."
        print(f"Generating voice note for: {event.title}")
        
        tts = gTTS(text=reminder_message, lang='en')
        filename = f'reminder_{event.id}.mp3'
        tts.save(filename)
        print(f"Saved voice note as {filename}")

        # --- NEW: Email Logic ---
        try:
            email = EmailMessage(
                subject=f"Reminder: {event.title}",
                body=f"Hi {event.user.username},\n\nThis is a reminder for your event: '{event.title}'.\nThe voice note is attached.",
                from_email='reminders@yourassistant.com',
                to=[event.user.email] # Assumes user has an email in their profile
            )
            email.attach_file(filename) # Attach the generated mp3 file
            email.send()
            print(f"Successfully sent email reminder for event {event.id}")
        except Exception as e:
            print(f"Failed to send email for event {event.id}: {e}")
        finally:
            # --- Clean up the created mp3 file ---
            if os.path.exists(filename):
                os.remove(filename)
                print(f"Deleted temporary file: {filename}")


    return f"Processed {upcoming_events.count()} reminders."