from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from students.models import Student

def students_pdf(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="students.pdf"'

    p = canvas.Canvas(response)

    students = Student.objects.all()

    y = 800

    for s in students:
        p.drawString(100,y,f"{s.student_name} - {s.email}")
        y -= 30

    p.save()

    return response
# Create your views here.
