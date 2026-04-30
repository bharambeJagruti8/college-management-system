from django.shortcuts import render
from django.shortcuts import render
from dashboard.models import StudentProfile, FeeRecord  # ✅ Sahi Addressfrom departments.models import Department


def ai_dashboard(request):

    answer = ""

    if request.method == "POST":

        question = request.POST.get("question").lower()

        if "student" in question:
            total = StudentProfile.objects.count()
            answer = f"Total registered students are {total}"

        elif "department" in question:
            total = Department.objects.count()
            answer = f"Total departments are {total}"

        elif "pending fee" in question:
            total = FeeRecord.objects.filter(status="Pending").count()
            answer = f"{total} students have pending fees"

        else:
            answer = "Sorry, I couldn't understand the question."

    return render(request, "ai/assistant.html", {"answer": answer})
# Create your views here.
