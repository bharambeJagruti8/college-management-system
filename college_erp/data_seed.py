import os
import django

# Django settings ko setup karein
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'college_erp.settings')
django.setup()

from accounts.models import Course, Session

def seed_data():
    print("Seeding Courses and Sessions...")

    # Courses add karein
    courses = ["MCA", "BCA", "B.Tech", "MBA"]
    for name in courses:
        course, created = Course.objects.get_or_create(course_name=name)
        if created:
            print(f"Added Course: {name}")

    # Sessions add karein
    sessions = [
        {"start": "2024-01-01", "end": "2026-01-01"},
        {"start": "2025-01-01", "end": "2027-01-01"}
    ]
    for s in sessions:
        session, created = Session.objects.get_or_create(
            session_start_year=s["start"], 
            session_end_year=s["end"]
        )
        if created:
            print(f"Added Session: {s['start']} to {s['end']}")

    print("Data Seeding Completed! ✅")

if __name__ == "__main__":
    seed_data()